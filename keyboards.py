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
    "my_tasks_for_today",
    "update_deadline",
    "update_task",
    "notifications_on",
    "notifications_off",
    "edit_profile"
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

setNotifications_ru = InlineKeyboardBuilder()
setNotifications_ru.add(InlineKeyboardButton(text="Включить", callback_data="able"))
setNotifications_ru.add(InlineKeyboardButton(text="Выключить", callback_data="disable"))
setNotifications_ru = setNotifications_ru.adjust(2).as_markup()

setNotifications_en = InlineKeyboardBuilder()
setNotifications_en.add(InlineKeyboardButton(text="Turn on", callback_data="able"))
setNotifications_en.add(InlineKeyboardButton(text="Turn off", callback_data="disable"))
setNotifications_en = setNotifications_en.adjust(2).as_markup()

update_deadline_en = InlineKeyboardBuilder()
update_deadline_en.add(InlineKeyboardButton(text="Time", callback_data="время дэдлайн"))
update_deadline_en.add(InlineKeyboardButton(text="Date", callback_data="дата дэдлайн"))
update_deadline_en.add(InlineKeyboardButton(text="Status", callback_data="статус дэдлайн"))
update_deadline_en = update_deadline_en.adjust(3).as_markup()

update_deadline_ru = InlineKeyboardBuilder()
update_deadline_ru.add(InlineKeyboardButton(text="Время", callback_data="время дэдлайн"))
update_deadline_ru.add(InlineKeyboardButton(text="Дата", callback_data="дата дэдлайн"))
update_deadline_ru.add(InlineKeyboardButton(text="Статус", callback_data="статус дэдлайн"))
update_deadline_ru = update_deadline_ru.adjust(3).as_markup()

update_task_en = InlineKeyboardBuilder()
update_task_en.add(InlineKeyboardButton(text="Time", callback_data="время задача"))
update_task_en.add(InlineKeyboardButton(text="Date", callback_data="дата дэдлайн"))
update_task_en.add(InlineKeyboardButton(text="Status", callback_data="статус дэдлайн"))
update_task_en = update_task_en.adjust(3).as_markup()

update_task_ru = InlineKeyboardBuilder()
update_task_ru.add(InlineKeyboardButton(text="Время", callback_data="время задача"))
update_task_ru.add(InlineKeyboardButton(text="Дата", callback_data="дата задача"))
update_task_ru.add(InlineKeyboardButton(text="Статус", callback_data="статус задача"))
update_task_ru = update_task_ru.adjust(3).as_markup()

update_status_task_en = InlineKeyboardBuilder()
update_status_task_en.add(InlineKeyboardButton(text="Completed", callback_data="completed task"))
update_status_task_en.add(InlineKeyboardButton(text="Partially completed", callback_data="partially completed task"))
update_status_task_en.add(InlineKeyboardButton(text="Not completed", callback_data="not completed task"))
update_status_task_en = update_status_task_en.adjust(3).as_markup()

update_status_task_ru = InlineKeyboardBuilder()
update_status_task_ru.add(InlineKeyboardButton(text="Выполнено", callback_data="completed task"))
update_status_task_ru.add(InlineKeyboardButton(text="Частично выполнено", callback_data="partially completed task"))
update_status_task_ru.add(InlineKeyboardButton(text="Не выполнено", callback_data="not completed task"))
update_status_task_ru = update_status_task_ru.adjust(3).as_markup()

update_status_deadline_en = InlineKeyboardBuilder()
update_status_deadline_en.add(InlineKeyboardButton(text="Completed", callback_data="completed deadline"))
update_status_deadline_en.add(InlineKeyboardButton(text="Not completed", callback_data="not completed deadline"))
update_status_deadline_en = update_status_deadline_en.adjust(2).as_markup()

update_status_deadline_ru = InlineKeyboardBuilder()
update_status_deadline_ru.add(InlineKeyboardButton(text="Завершён", callback_data="completed deadline"))
update_status_deadline_ru.add(InlineKeyboardButton(text="Не завершён", callback_data="not completed deadline"))
update_status_deadline_ru = update_status_deadline_ru.adjust(2).as_markup()

edit_profile_ru = InlineKeyboardBuilder()
edit_profile_ru.add(InlineKeyboardButton(text="Имя", callback_data="edit_name"))
edit_profile_ru.add(InlineKeyboardButton(text="Язык", callback_data="edit_language"))
edit_profile_ru = edit_profile_ru.adjust(2).as_markup()

edit_profile_en = InlineKeyboardBuilder()
edit_profile_en.add(InlineKeyboardButton(text="Name", callback_data="edit_name"))
edit_profile_en.add(InlineKeyboardButton(text="Language", callback_data="edit_language"))
edit_profile_en = edit_profile_en.adjust(2).as_markup()

quest_ru = InlineKeyboardBuilder()
quest_ru.add(InlineKeyboardButton(text="Голосовой ввод", callback_data="voice enter"))
quest_ru.add(InlineKeyboardButton(text="Ввод текстом", callback_data="text enter"))
quest_ru = quest_ru.adjust(2).as_markup()

quest_en = InlineKeyboardBuilder()
quest_en.add(InlineKeyboardButton(text="Voice input", callback_data="voice enter"))
quest_en.add(InlineKeyboardButton(text="Text input", callback_data="text enter"))
quest_en = quest_en.adjust(2).as_markup()
