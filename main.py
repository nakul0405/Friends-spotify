import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from spotify import get_access_token, get_friend_activity
from dotenv import load_dotenv
import os
from helpers import time_player

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
user_cookies = {}  # In-memory per-user storage

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 Welcome to *Spotify Friends Activity Bot*!\n\n"
        "1️⃣ Use /setcookie <your_sp_dc_cookie> to get started.\n"
        "2️⃣ Then use /friends to view your friends' activity.\n\n"
        "_Your cookie is kept only during your session._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def setcookie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide your `sp_dc` cookie.\nUsage: /setcookie <cookie>")
        return
    cookie = context.args[0]
    user_cookies[update.effective_user.id] = cookie
    await update.message.reply_text("✅ Cookie saved! Use /friends to fetch data.")

async def friends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_cookies:
        await update.message.reply_text("❗ You haven't set your cookie. Use /setcookie <cookie> first.")
        return
    try:
        token = get_access_token(user_cookies[uid])
        friends = get_friend_activity(token)
        if not friends:
            await update.message.reply_text("🕵️ No friend activity found.")
            return
        msg = ""
        for f in friends:
            name = f['user']['name']
            track = f['track']['name']
            artist = f['track']['artist']['name']
            timestamp = f['timestamp']
            time_str, _ = time_player(timestamp)
            msg += f"🎧 *{name}* is listening to _{track}_ by _{artist}_ ({time_str} ago)\n\n"
        await update.message.reply_text(msg.strip(), parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setcookie", setcookie))
app.add_handler(CommandHandler("friends", friends))
app.run_polling()
