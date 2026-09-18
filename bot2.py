import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ----------------- НАСТРОЙКИ -----------------
TOKEN = "8899617219:AAFrrfoxUA6N8NjVds4WFVFJTNsEpm_W2po"
CHANNEL_ID = "@CheatsMinecraft141"  # Название канала (например, @my_channel) или его ID
CHANNEL_URL = "https://t.me/CheatsMinecraft141"  # Ссылка на твой канал

# Ссылки на файлы (замени на свои реальные ссылки)
DOWNLOAD_LINKS = {
    "hack_1": "https://example.com/cheat1",
    "hack_2": "https://example.com/cheat2",
    "hack_3": "https://example.com/cheat3",
}
# ----------------------------------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Клавиатура проверки подписки
def get_sub_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="?? Подписаться на канал", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="? Проверить подписку", callback_data="check_sub")],
        ]
    )


# Главное меню после проверки
def get_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="?? Скачать читы Майнкрафт", callback_data="mc_cheats")]
        ]
    )


# Меню выбора читов
def get_cheats_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Venus", callback_data="select_cheat_1")],
            [InlineKeyboardButton(text="Haruka", callback_data="select_cheat_2")],
            [InlineKeyboardButton(text="Читы 3", callback_data="select_cheat_3")],
            [InlineKeyboardButton(text="?? Назад", callback_data="back_to_main")],
        ]
    )


# Проверка подписки пользователя на канал
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception:
        return False


# Старт бота
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)

    if is_subscribed:
        await message.answer(
            "? Вы подписаны! Выберите действие:", reply_markup=get_main_menu()
        )
    else:
        await message.answer(
            "Для использования бота необходимо подписаться на наш канал!",
            reply_markup=get_sub_keyboard(),
        )


# Обработка кнопки "Проверить подписку"
@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback: types.CallbackQuery):
    is_subscribed = await check_subscription(callback.from_user.id)

    if is_subscribed:
        await callback.message.edit_text(
            "? Подписка подтверждена! Доступ открыт:", reply_markup=get_main_menu()
        )
    else:
        await callback.answer(
            "? Вы всё ещё не подписались на канал!", show_alert=True
        )


# Переход в меню читов
@dp.callback_query(F.data == "mc_cheats")
async def process_mc_cheats(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите нужную версию или сборку:", reply_markup=get_cheats_menu()
    )


# Выбор конкретного чита -> ОТПРАВКА НОВОГО СООБЩЕНИЯ
@dp.callback_query(F.data.startswith("select_cheat_"))
async def process_select_cheat(callback: types.CallbackQuery):
    cheat_id = callback.data.replace("select_cheat_", "hack_")
    download_url = DOWNLOAD_LINKS.get(cheat_id, "https://example.com")

    # Создаём кнопку со ссылкой для отдельного сообщения
    link_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="?? Скачать", url=download_url)]
        ]
    )

    await callback.answer()

    # Отправляем новое сообщение
    await callback.message.answer(
        "Вот ваша ссылка на скачивание:", reply_markup=link_keyboard
    )


# Назад в главное меню
@dp.callback_query(F.data == "back_to_main")
async def process_back(callback: types.CallbackQuery):
    await callback.message.edit_text("Главное меню:", reply_markup=get_main_menu())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())