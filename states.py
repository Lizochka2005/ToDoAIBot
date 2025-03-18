from aiogram.fsm.state import State, StatesGroup

class Question(StatesGroup):
    text = State()
    voice = State()

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_language = State()
    confirmed = State()

class UpdateRegistration(StatesGroup):
    waiting_for_new_name = State()
    waiting_for_new_language = State()

class TaskCreation(StatesGroup):
    waiting_for_task = State()
    waiting_for_date = State()
    waiting_for_time = State()

class TaskUpdate(StatesGroup):
    waiting_for_task_id = State()
    waiting_for_new_status = State()
    waiting_for_new_date = State()
    waiting_for_new_time = State()

class DeadlineCreation(StatesGroup):
    waiting_for_deadline = State()
    waiting_for_date = State()
    waiting_for_time = State()

class DeadlineUpdate(StatesGroup):
    waiting_for_deadline_id = State()
    waiting_for_new_status = State()
    waiting_for_new_date = State()
    waiting_for_new_time = State()

class GetTaskListForDate(StatesGroup):
    waiting_for_date = State()

class EditProfile(StatesGroup):
    waiting_for_choice = State()
    waiting_for_name = State()
    waiting_for_language = State()