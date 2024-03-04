from typing import Final
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

API_TOKEN: Final = "6992266110:AAGv1gt5U9obxZLT8an7E5F6lJEpUtVMoC8"
BOT_NAME: Final = "@antony_life_ios_bot"

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Это бот помощник для канала Антон Добрынин и Antony o Life & iOS')

# Responses

def handle_response(text: str) -> str:
    if "Привет" in text:
        return "Привет!"
    return "Давай выберем команду"

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Updated {update} error {context.error}')


if __name__ == '__main__':
    print('starting bot')
    app = Application.builder().token(API_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Error
    app.add_error_handler(error)

    # Polling
    print('Polling')
    app.run_polling(poll_interval=5)