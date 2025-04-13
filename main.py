
import os
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALERT_USER = os.getenv("ALERT_USER", "@Banky664")
WALLET_FILE = "wallets.json"

# Load wallet data
def load_wallets():
    try:
        with open(WALLET_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_wallets(wallets):
    with open(WALLET_FILE, "w") as f:
        json.dump(wallets, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Welcome to Pi Wallet Monitor Bot!
Use /manual to see commands.")

async def manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 *Bot Manual*
"
        "💠 /addwallet <wallet> - Add wallet to monitor
"
        "💠 /removewallet <wallet> - Remove wallet
"
        "💠 /listwallets - View all tracked wallets
"
        "💠 /history - View balance history
"
        "💠 /manual - Show this help message",
        parse_mode="Markdown"
    )

async def add_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        return await update.message.reply_text("❌ Usage: /addwallet <wallet>")
    wallet = context.args[0]
    wallets = load_wallets()
    user_id = str(update.message.from_user.id)
    wallets.setdefault(user_id, [])
    if wallet not in wallets[user_id]:
        wallets[user_id].append(wallet)
        save_wallets(wallets)
        await update.message.reply_text(f"✅ Wallet {wallet} added.")
    else:
        await update.message.reply_text("⚠️ Wallet already tracked.")

async def remove_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        return await update.message.reply_text("❌ Usage: /removewallet <wallet>")
    wallet = context.args[0]
    wallets = load_wallets()
    user_id = str(update.message.from_user.id)
    if wallet in wallets.get(user_id, []):
        wallets[user_id].remove(wallet)
        save_wallets(wallets)
        await update.message.reply_text(f"🗑️ Wallet {wallet} removed.")
    else:
        await update.message.reply_text("❌ Wallet not found.")

async def list_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    wallets = load_wallets().get(user_id, [])
    if wallets:
        await update.message.reply_text("📦 Your wallets:
" + "
".join(wallets))
    else:
        await update.message.reply_text("📭 No wallets being tracked.")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 Balance history coming soon!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("manual", manual))
app.add_handler(CommandHandler("addwallet", add_wallet))
app.add_handler(CommandHandler("removewallet", remove_wallet))
app.add_handler(CommandHandler("listwallets", list_wallets))
app.add_handler(CommandHandler("history", history))

if __name__ == "__main__":
    app.run_polling()
