from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from server_start import start_minecraft_server
from server_status import check_server_status
import asyncio

# Directly set the token for testing
TOKEN = '6649079349:AAHNkUhbRdcaJ2G9_wUtz3VVZjMNzS1z1YA'


async def start(update: Update, context: CallbackContext) -> None:
    await send_menu(update)


async def send_menu(update):
    keyboard = [
        [InlineKeyboardButton("Запустить сервер", callback_data='start_server')],
        [InlineKeyboardButton("Проверить статус сервера", callback_data='check_status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if isinstance(update, Update):
        await update.message.reply_text('Привет! Выберите опцию ниже.', reply_markup=reply_markup)
    else:
        await update.reply_text('Выберите опцию ниже.', reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'start_server':
        await query.edit_message_text(text='Запуск сервера...')

        async def send_status_updates():
            for status in start_minecraft_server():
                await query.message.reply_text(status)
                await asyncio.sleep(10)  # Ensure the loop yields control to the event loop

        await send_status_updates()

    elif query.data == 'check_status':
        status = check_server_status()
        await query.edit_message_text(text=f'Текущий статус сервера: {status}')

    await send_menu(query.message)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='start_server'))
    application.add_handler(CallbackQueryHandler(button, pattern='check_status'))

    application.run_polling()


if __name__ == '__main__':
    main()
