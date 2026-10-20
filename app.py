import io
import threading
import time
from urllib.parse import unquote
from playwright.sync_api import sync_playwright
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Put the bot token here
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

users_data = {}


def get_user(chat_id):
  if chat_id not in users_data:
    users_data[chat_id] = {
        "session_id": None,
        "is_running": False,
        "deleted_count": 0,
        "batch_count": 0,
        "batch_size": 10,
        "status_text": "Waiting for Session ID...",
        "panel_msg_id": None,
        "request_screenshot": False,
    }
  return users_data[chat_id]


def build_panel_text(u):
  state_icon = "Running at max speed" if u["is_running"] else "Stopped"
  session_state = "Saved" if u["session_id"] else "Not found"
  return (
      f"**A tool for deleting Instagram comments**\n"
      f"━━━━━━━━━━━━━━━━━━\n"
      f"• **Bot Status:** {state_icon}\n"
      f"• **Session ID:** {session_state}\n"
      f"• **Actual Deleted:** `{u['deleted_count']}` comments\n"
      f"• **Completed Batches:** `{u['batch_count']}`\n"
      f"━━━━━━━━━━━━━━━━━━\n"
      f"**Current Settings:**\n"
      f"• Batch Size: `{u['batch_size']}` comments (no breaks)\n"
      f"━━━━━━━━━━━━━━━━━━\n"
      f"**Live Operations:**\n"
      f"`{u['status_text']}`"
  )


def build_panel_markup(u):
  markup = InlineKeyboardMarkup(row_width=2)
  if u["is_running"]:
    markup.add(
        InlineKeyboardButton("Stop immediately", callback_data="toggle_run")
    )
  else:
    markup.add(
        InlineKeyboardButton("Start fast cleaning", callback_data="toggle_run")
    )

  markup.row(
      InlineKeyboardButton("Set Session ID", callback_data="set_session"),
      InlineKeyboardButton("Live Screenshot", callback_data="take_shot"),
  )
  markup.row(
      InlineKeyboardButton(
          f"Batch size ({u['batch_size']})", callback_data="change_batch"
      ),
      InlineKeyboardButton("Refresh Panel", callback_data="refresh_panel"),
  )
  return markup


def update_panel(chat_id, status_msg=None):
  u = get_user(chat_id)
  if status_msg:
    u["status_text"] = status_msg
  if not u["panel_msg_id"]:
    return
  try:
    bot.edit_message_text(
        text=build_panel_text(u),
        chat_id=chat_id,
        message_id=u["panel_msg_id"],
        parse_mode="Markdown",
        reply_markup=build_panel_markup(u),
    )
  except Exception:
    pass


# ---------------- Direct cleaner engine without breaks ---------------- #
def ig_cleaner_worker(chat_id):
  u = get_user(chat_id)
  clean_session = unquote(u["session_id"].strip())

  with sync_playwright() as p:
    update_panel(chat_id, "Launching headless browser...")
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 850},
    )

    context.add_cookies([{
        "name": "sessionid",
        "value": clean_session,
        "domain": ".instagram.com",
        "path": "/",
        "httpOnly": True,
        "secure": True,
    }])

    page = context.new_page()
    update_panel(chat_id, "Opening comments page...")

    try:
      page.goto(
          "https://www.instagram.com/your_activity/interactions/comments/",
          timeout=60000,
      )
      time.sleep(5)

      if "login" in page.url:
        u["is_running"] = False
        update_panel(chat_id, "Session ID is invalid or expired!")
        browser.close()
        return

      while u["is_running"]:
        if u["request_screenshot"]:
          u["request_screenshot"] = False
          shot = page.screenshot()
          bot.send_photo(
              chat_id, io.BytesIO(shot), caption="Live browser screenshot"
          )

        # 1. Activate Select mode if not activated
        is_select_mode = page.evaluate("""() => {
                    const spans = Array.from(document.querySelectorAll('span'));
                    const hasCancel = spans.some(s => s.textContent.trim() === 'Cancel');
                    if (hasCancel) return true;

                    for (const s of spans) {
                        const txt = s.textContent.trim();
                        if (txt === 'Select') {
                            const btn = s.closest('[role="button"], button') || s;
                            btn.click();
                            return 'clicked';
                        }
                    }
                    return false;
                }""")

        if is_select_mode == "clicked":
          update_panel(chat_id, "Select mode activated...")
          time.sleep(1.2)

        # Clear temp markers before starting new batch
        page.evaluate(
            "() => document.querySelectorAll('[data-ig-tried]').forEach(el =>"
            " el.removeAttribute('data-ig-tried'))"
        )

        # 2. Select a batch of comments quickly
        batch_size = u["batch_size"]
        selected_now = 0
        update_panel(chat_id, f"Selecting {batch_size} comments...")

        for _ in range(batch_size):
          if not u["is_running"]:
            break

          box_info = page.evaluate("""() => {
                        const icons = Array.from(document.querySelectorAll('[data-bloks-name="ig.components.Icon"], [aria-label="Toggle checkbox"]'));
                        for (const el of icons) {
                            if (el.getAttribute('data-ig-tried') === '1') continue;

                            const style = el.getAttribute('style') || '';
                            const inner = el.innerHTML || '';

                            const isUncheckedIcon = (style.includes('circle__outline') && !style.includes('__circle__outline')) ||
                                                    (inner.includes('circle__outline') && !inner.includes('__circle__outline'));

                            if (!isUncheckedIcon) continue;

                            el.scrollIntoView({ behavior: 'instant', block: 'center' });
                            const rect = el.getBoundingClientRect();
                            if (rect.width > 0 && rect.height > 0 && rect.top > 80) {
                                el.setAttribute('data-ig-tried', '1');
                                return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
                            }
                        }
                        return null;
                    }""")

          if not box_info:
            break

          page.mouse.click(box_info["x"], box_info["y"])
          time.sleep(0.2)

          page.evaluate("""(coords) => {
                        const el = document.elementFromPoint(coords.x, coords.y);
                        if (el) {
                            const style = el.getAttribute('style') || '';
                            if (style.includes('circle__outline')) {
                                const btn = el.closest('[role="button"], [tabindex="0"]') || el;
                                btn.click();
                            }
                        }
                    }""", box_info)

          selected_now += 1
          time.sleep(0.2)

        if selected_now == 0:
          update_panel(chat_id, "Scrolling to load more comments...")
          page.evaluate("""() => {
                        window.scrollBy(0, 800);
                        const divs = Array.from(document.querySelectorAll('div'));
                        for (const d of divs) {
                            if (d.scrollHeight > d.clientHeight + 100 && d.clientWidth > 300) {
                                d.scrollTop += 800;
                            }
                        }
                    }""")
          time.sleep(2.0)
          continue

        # 3. Press the first Delete button <span>Delete</span>
        time.sleep(0.5)
        del_btn_info = page.evaluate("""() => {
                    const spans = Array.from(document.querySelectorAll('span'));
                    for (const s of spans) {
                        const txt = s.textContent.trim();
                        if (txt === 'Delete') {
                            const style = s.getAttribute('style') || '';
                            if (!style.includes('0.3')) {
                                const rect = s.getBoundingClientRect();
                                if (rect.width > 0 && rect.height > 0) {
                                    const btn = s.closest('[role="button"], button') || s;
                                    btn.click();
                                    return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
                                }
                            }
                        }
                    }
                    return null;
                }""")

        if not del_btn_info:
          update_panel(
              chat_id, "Delete button not activated, scrolling and trying another batch..."
          )
          page.mouse.wheel(0, 500)
          time.sleep(1.0)
          continue

        time.sleep(0.3)
        if page.locator('div._ap3a, div[role="dialog"]').count() == 0:
          page.mouse.click(del_btn_info["x"], del_btn_info["y"])

        update_panel(chat_id, "Confirming direct deletion...")
        time.sleep(1.2)

        # 4. Immediate click on the confirmation popup button <div class="_ap3a ...">Delete</div>
        confirmed = page.evaluate("""() => {
                    const confirmDivs = Array.from(document.querySelectorAll('div._ap3a, div[role="dialog"] button, div[role="dialog"] div[role="button"]'));
                    for (const el of confirmDivs) {
                        const txt = el.textContent.trim();
                        if (txt === 'Delete') {
                            const clickable = el.closest('button, [role="button"]') || el;
                            const rect = clickable.getBoundingClientRect();
                            clickable.click();
                            return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
                        }
                    }
                    return null;
                }""")

        if confirmed:
          time.sleep(0.2)
          page.mouse.click(confirmed["x"], confirmed["y"])
          time.sleep(2.0)  # Short wait for comments to disappear from page

          u["deleted_count"] += selected_now
          u["batch_count"] += 1
          update_panel(
              chat_id,
              f"Deleted {selected_now} comments! Moving to next batch immediately...",
          )
        else:
          update_panel(
              chat_id, "Confirmation popup not found, retrying immediately..."
          )
          time.sleep(1.0)

    except Exception as e:
      update_panel(chat_id, f"❌ Stopped due to error: {str(e)[:40]}")
    finally:
      u["is_running"] = False
      update_panel(chat_id, "Session stopped and browser closed.")
      browser.close()


# ---------------- Bot commands and buttons ---------------- #
@bot.message_handler(commands=["start"])
def send_welcome(message):
  chat_id = message.chat.id
  u = get_user(chat_id)
  msg = bot.send_message(
      chat_id,
      build_panel_text(u),
      parse_mode="Markdown",
      reply_markup=build_panel_markup(u),
  )
  u["panel_msg_id"] = msg.message_id


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
  chat_id = call.message.chat.id
  u = get_user(chat_id)
  u["panel_msg_id"] = call.message.message_id

  if call.data == "set_session":
    msg = bot.send_message(
        chat_id,
        "Send your account's `sessionid` code now (your message will be deleted immediately for security):",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(msg, save_session_step)
    bot.answer_callback_query(call.id)

  elif call.data == "toggle_run":
    if not u["session_id"]:
      bot.answer_callback_query(
          call.id, "Please set Session ID first!", show_alert=True
      )
      return

    if u["is_running"]:
      u["is_running"] = False
      bot.answer_callback_query(call.id, "Stopping operation...")
      update_panel(chat_id, "Stopping and closing browser...")
    else:
      u["is_running"] = True
      bot.answer_callback_query(call.id, "Fast cleaning started!")
      update_panel(chat_id, "Preparing to start...")
      threading.Thread(
          target=ig_cleaner_worker, args=(chat_id,), daemon=True
      ).start()

  elif call.data == "take_shot":
    if not u["is_running"]:
      bot.answer_callback_query(
          call.id, "Start the tool first to take a screenshot.", show_alert=True
      )
    else:
      u["request_screenshot"] = True
      bot.answer_callback_query(
          call.id, "Screenshot request sent, you'll receive it in seconds..."
      )

  elif call.data == "change_batch":
    sizes = [5, 10, 15, 20, 25]
    curr_idx = (
        sizes.index(u["batch_size"]) if u["batch_size"] in sizes else 1
    )
    u["batch_size"] = sizes[(curr_idx + 1) % len(sizes)]
    bot.answer_callback_query(
        call.id, f"Batch size changed to {u['batch_size']}"
    )
    update_panel(chat_id)

  elif call.data == "refresh_panel":
    bot.answer_callback_query(call.id, "Updated")
    update_panel(chat_id)


def save_session_step(message):
  chat_id = message.chat.id
  u = get_user(chat_id)
  u["session_id"] = message.text.strip()
  try:
    bot.delete_message(chat_id, message.message_id)
  except Exception:
    pass
  update_panel(chat_id, "Session ID saved! Ready to start.")


if __name__ == "__main__":
  print("Canceling any old Webhook...")
  bot.remove_webhook()
  time.sleep(1)
  print("Bot is running now...")
  bot.infinity_polling(skip_pending=True)