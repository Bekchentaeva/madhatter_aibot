from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import CommandStart
from app.generators import gpt4
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio

router=Router()

class Generate(StatesGroup):
    text=State()

@router.message(CommandStart())
async def cmd_start(message: Message,state: FSMContext):
    await message.answer('Добро пожаловать в бот! Чем могу помочь?')
    await state.clear()

@router.message(Generate.text)
async def generate_error(message:Message):
    await message.answer('Идёт генерация ответа. Пожалуйста, подождите...')

@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    max_attempts = 3  # Максимальное количество попыток
    attempt = 0

    while attempt < max_attempts:
        try:
            response = await gpt4(message.text, timeout=100)
            await message.answer(response.choices[0].message.content)
            break  # Выход из цикла, если запрос успешен
        except Exception as e:
            if "Request timed out" in str(e):
                attempt += 1
                if attempt < max_attempts:
                    await message.answer(f'Ошибка: {str(e)}. Повторная попытка {attempt}/{max_attempts}...')
                    await asyncio.sleep(2)  # Небольшая пауза перед повторной попыткой
                else:
                    await message.answer(f'Произошла ошибка: {str(e)}. Превышено количество попыток.')
                    break
            else:
                await message.answer(f'Произошла ошибка: {str(e)}')
                break

    await state.clear()
