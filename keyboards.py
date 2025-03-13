from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


say_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Voice 🎤", callback_data="Озвучить"),
        ],
        [
            InlineKeyboardButton(
                text="Stop answering questions",
                callback_data="Остановить ответы на вопросы",
            )
        ],
    ]
)

say_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Озвучить 🎤", callback_data="Озвучить"),
        ],
        [
            InlineKeyboardButton(
                text="Остановить ответы на вопросы",
                callback_data="Остановить ответы на вопросы",
            )
        ],
    ]
)

# say_and_translate = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Озвучить 🎤", callback_data="Озвучить"),
#             InlineKeyboardButton(text="Перевести 🌐", callback_data="Перевести"),
#         ],
#         [
#             InlineKeyboardButton(
#                 text="Остановить ответы на вопросы",
#                 callback_data="Остановить ответы на вопросы",
#             )
#         ],
#     ]
# )


commands = [
    "start",
    "answer_question",
    "add_deadline",
    "add_task",
    "my_nearest_deadlines",
    "my_tasks_for_date",
    "update_deadline",
    "update_task",
]


def show_commands_ru():
    # вывод команд бота
    bot_commands = "У бота есть команды:\n"
    for command in commands:
        bot_commands += "/" + command + "\n"
    return bot_commands

def show_commands_en():
    # вывод команд бота
    bot_commands = "Bot has commands:\n"
    for command in commands:
        bot_commands += "/" + command + "\n"
    return bot_commands
