from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from spotify import get_access_token, get_friend_activity
from dotenv import load_dotenv
import os
from helpers import time_player

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Railway app url like https://your-bot.up.railway.app

user_cookies = {}

async def start(update, context):
    await update.message.reply_text("Bot is live! Use /setcookie <cookie> and then /friends")

async def setcookie(update, context):
    if not context.args:
        await update.message.reply_text("❌ Usage: /setcookie <sp_dc>")
        return
    user_cookies[update.effective_user.id] = context.args[0]
    await update.message.reply_text("✅ Cookie saved!")

async def friends(update, context):
    uid = update.effective_user.id
    if uid not in user_cookies:
        await update.message.reply_text("Set your cookie first using /setcookie")
        return
    try:
        token = get_access_token(user_cookies[uid])
        friends = get_friend_activity(token)
        if not friends:
            await update.message.reply_text("No friends found.")
            return
        msg = ""
        for f in friends:
            name = f["user"]["name"]
            track = f["track"]["name"]
            artist = f["track"]["artist"]["name"]
            timestamp = f["timestamp"]
            readable, _ = time_player(timestamp)
            msg += f"🎧 *{name}* is listening to _{track}_ by _{artist}_ ({readable} ago)\n\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setcookie", setcookie))
    app.add_handler(CommandHandler("friends", friends))

    # Run with webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=f"{APP_URL}/webhook"
    )
