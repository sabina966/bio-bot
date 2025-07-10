# bot.py
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
from dotenv import load_dotenv

# Включаем логирование, чтобы видеть ошибки в консоли PyCharm
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- НОВОЕ: Загружаем факты из файла в память при старте бота ---
try:
    with open('facts.txt', 'r', encoding='utf-8') as f:
        facts_list = [line.strip() for line in f if line.strip()]
    print(f"Загружено {len(facts_list)} фактов.")
except FileNotFoundError:
    print("Ошибка: файл facts.txt не найден! Создайте его.")
    facts_list = ["К сожалению, файл с фактами не найден."]

# Это функция-обработчик. Она будет вызываться каждый раз,
# когда пользователь присылает команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Я бот, который знает факты о биофизике. Отправь мне команду /fact, чтобы узнать что-то новое!"
    )

# --- НОВОЕ: Функция-обработчик для команды /fact ---
async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Выбираем случайный факт из нашего списка
    random_fact = random.choice(facts_list)
    # Отправляем его пользователю
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=random_fact
    )

load_dotenv() # Загружает переменные из .env файла
TOKEN = os.getenv("TOKEN") # Получаем токен

# Основная часть программы
if __name__ == '__main__':
    # API токен от @BotFather
    application = ApplicationBuilder().token(TOKEN).build()

    # "Регистрируем" нашу команду /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # --- НОВОЕ: Регистрируем обработчик для команды /fact ---
    fact_handler = CommandHandler('fact', fact)
    application.add_handler(fact_handler)

    # Запускаем бота
    print("Бот запущен и готов к работе...")
    application.run_polling()