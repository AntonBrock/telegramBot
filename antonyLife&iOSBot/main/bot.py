import json
from typing import Final
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, ConversationHandler, CallbackQueryHandler

import re
import telegram.ext.filters as filters
import requests

API_TOKEN: Final = "6992266110:AAFk_o80XlXiF5mq1rszkx3IKu7RvICQXFQ"
BOT_NAME: Final = "@antony_life_ios_bot"
MY_TELEGRAM_ID = 222943251

CHOOSE_BUTTON, GET_ANSWER, GET_USER_FILE = range(3)
buttons = [
        ['Задать вопрос Антону'],
        ['Отправить файл для МОК-собеса в телегам канале 📁'],
        ['Забрать промокод -40% на ВСЕ продукты 🛍', 'БЕСПЛАТНЫЕ и полезные работы 🛒']
    ]

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = buttons

    await update.message.reply_text(
        "Привет! Это бот - помощник для канала Antony o Life & iOS 👋 "
        "Что тебя интересует сейчас?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False
        ),
    )
    return CHOOSE_BUTTON
async def user_did_choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text

    if text == buttons[0][0]:
        await update.message.reply_text(
            "Я рад, что у тебя есть вопрос и жду его 👀"
        )
        return GET_ANSWER
    elif text == buttons[1][0]:
        await update.message.reply_text(
            "Отлично, теперь тебе нужно прикрепить файл формата - PDF 📁, ссылки НЕ нужны 🔗"
        )
        return GET_USER_FILE
    elif text == buttons[2][0]:
        await update.message.reply_text("Конечно, вот промокод для ВСЕХ продуктов: SECRET_PROMO_BOT")
    else:
        await update.message.reply_text("Сейчас доступен 1 бесплатный WorkBook в рамках телеграмма канала")
        await context.bot.send_photo(chat_id=f"{update.message.chat_id}", photo=open('classVSStrucrsPreview.png', 'rb'), caption="Более 220 скачиваний, 37+ позитивных отзывов, задачи и практика, отличный дизайн и легкая подача теории! \n\n🔥Ты можешь забрать мой первый продукт - Workbook \"Struct vs classes in Swift: Отличия и как их использовать\" совершенно бесплатно 🚀")

        list_of_buttons = ['Забрать']
        list_of_urls = ["https://drive.google.com/file/d/1x03HusFQOW_Vs5_SSZcz6GBuOc7bneoW/view"]

        button_list = []
        for index, each in enumerate(list_of_buttons):
            button_list.append(InlineKeyboardButton(each, callback_data=each, url=list_of_urls[index]))
        reply_markup = InlineKeyboardMarkup(build_menu_for_free_product(button_list, n_cols=1))
        invisible_space = u'\u200B'
        await context.bot.send_message(chat_id=update.message.chat_id, text="При нажатие на кнопку - будет открыт GoogleDrive,\nгде ты можешь скачать продукт или поделиться им 🙌 ", reply_markup=reply_markup)

def build_menu_for_free_product(buttons,n_cols,header_buttons=None,footer_buttons=None):
      menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
      if header_buttons:
        menu.insert(0, header_buttons)
      if footer_buttons:
        menu.append(footer_buttons)
      return menu

async def send_text_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_text
    user_input_text = update.message.text

    # info
    user_name = update.message.from_user.name
    user_full_name = update.message.from_user.full_name
    user_message_date = update.message.date
    user_chat_id = update.message.chat_id
    url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={MY_TELEGRAM_ID}&text=\n\nНОВОЕ СОБЫТИЕ\n\nНикнейм - {user_name},\nИмя - {user_full_name},\nСообщение: \"{user_input_text}\",\n\nДата - {user_message_date},\nЧАТ-ID: {user_chat_id}"

    await update.message.reply_text("Большое спасибо за вопрос, я его получил и отвечу напрямую в ТГ 💪")
    await requests.get(url).json()

async def send_file_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_data
    user_input_text = update.message.text
    user_name = update.message.from_user.name
    user_full_name = update.message.from_user.full_name
    user_message_date = update.message.date
    user_chat_id = update.message.chat_id

    url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={MY_TELEGRAM_ID}&text=\n\nНОВОЕ СОБЫТИЕ\n\nНикнейм - {user_name},\nИмя - {user_full_name},\n\nДата - {user_message_date},\nЧАТ-ID: {user_chat_id}"

    # Download file
    fileName = update.message.document.file_name
    new_file_id = update.message.document.file_id

    # Send file to admin
    await context.bot.send_document(chat_id=MY_TELEGRAM_ID, document=new_file_id)
    await update.message.reply_text("Большое спасибо, я разберу твое резюме и вернусь с ответом по поводу МОК-собеседования")

    # Send user info to admin
    await requests.get(url).json()
async def send_free_promo_code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Держи промокод для ВСЕХ продуктов: SECRET_PROMO_BOT')

async def send_message_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_string = update.message.text

    # Паттерн для извлечения chat_id и message
    pattern = re.compile(r'chatID="(\d+)", message="([^"]+)"')

    # Ищем совпадения
    match = pattern.search(message_string)

    chatID = 0
    messageToUser = ""
    if match:
        chat_id = match.group(1)
        chatID = chat_id

        message = match.group(2)
        messageToUser = message
    else:
        print("Совпадения не найдены")

    await context.bot.send_message(chat_id=chatID, text=messageToUser)
    await update.message.reply_text(f'Отправил сообщение \"{messageToUser}\" пользователю с его ID{chatID} ')

# Responses
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Updated {update} error {context.error}')

async def cancel(update: Update):
    await update.message.reply_text(
        "Чтобы начать заного, просто введи /start команду ", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


## START
if __name__ == '__main__':
    print('starting bot')
    app = Application.builder().token(API_TOKEN).build()

    # Commands
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSE_BUTTON: [
                MessageHandler(filters.ALL, user_did_choose),
            ],
            GET_ANSWER: [
                MessageHandler(filters.ALL, send_text_to_admin)
            ],
            GET_USER_FILE: [
                MessageHandler(filters.ALL, send_file_to_admin)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('send_answer', send_message_to_user))

    # Создать команду /note чтобы она показывала все доступные команды для admin

    # app.add_handler(CommandHandler('sendquestion', send_question_command))
    # app.add_handler(CommandHandler('sendrequest', send_request_command))
    # app.add_handler(CommandHandler('getfreepromocode', send_free_promo_code_command))

    # Error
    app.add_error_handler(error)

    # Polling
    app.run_polling(allowed_updates=Update.ALL_TYPES)

    ### Это нужно для будущих обработок кнопок


    # app.add_handler(CallbackQueryHandler(free_product_button_didTap))

    # async def free_product_button_didTap(update:Update, context:ContextTypes.DEFAULT_TYPE):
    #     query = update.callback_query
    #     await query.answer()
    #
    #     print(f"Пользователь выбрал: {query.data}")
    #     await context.bot.send_document(chat_id=update.callback_query.message.chat.id, document=open('structVsClassesWorkBookFile.pdf', 'rb'))