from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    waiting_for_link = State()
    waiting_for_email_text = State()
    waiting_for_support_message = State()