import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import dp
from states.numbers import Numbers

WORD_TYPE = '___'

choice = InlineKeyboardMarkup(row_width=4)
choice.insert(InlineKeyboardButton(text='1', callback_data='percent:1'))
choice.insert(InlineKeyboardButton(text='2', callback_data='percent:2'))
choice.insert(InlineKeyboardButton(text='3', callback_data='percent:3'))
choice.insert(InlineKeyboardButton(text='4', callback_data='percent:4'))

questions = ('Сколько составляет {} % от числа {}',
             'Сколько % составляет число {} от числа {}',
             'Прибавить {} % к числу {}',
             'Вычесть {} % из числа {}')

STANDART_TEXT = 'Введите поочереди два числа для расчета:'
ERROR_TEXT = 'Вы ввели не число'
NEGATIVE_TEXT = 'Вы ввели отрицательное число :('
RESULT_TEXT = 'Ответ : {}'


def percent_counter(quest_number: float, number_1: float, number_2: float):
    if quest_number == 0:
        return number_2 * number_1 / 100
    elif quest_number == 1:
        return number_1 / number_2 * 100
    elif quest_number == 2:
        return number_2 + number_2 * number_1 / 100
    elif quest_number == 3:
        return number_2 - number_2 * number_1 / 100


@dp.message_handler(Command("start"))
async def enter_test(message: types.Message, state: FSMContext):
    await message.answer("Что посчитать?\n"
                         "1.Сколько составляет ___ % от числа ___\n"
                         "2.Сколько % составляет число ___ от числа ___\n"
                         "3.Прибавить ___ % к числу ___\n"
                         "4.Вычесть ___ % из числа ___"
                         , reply_markup=choice)


@dp.callback_query_handler(text_contains='percent:')
async def percent_1(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    logging.info(f'call = {callback_data}')
    quest_number = callback_data.replace('percent:', '')
    try:
        quest_number = int(quest_number) - 1
        await state.update_data(question_number=quest_number)
        await call.message.answer(str(questions[quest_number]).format(WORD_TYPE, WORD_TYPE) + '\n' + STANDART_TEXT)
        await Numbers.Num1.set()
    except ValueError:
        await call.message.answer('Server has problem with InlineKeyboard')


@dp.message_handler(state=Numbers.Num1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        number = float(answer.replace(',', '.'))
        if number > 0:
            await state.update_data(number_1=number)
            await Numbers.Num2.set()
        else:
            await message.answer(NEGATIVE_TEXT)
    except ValueError:
        await message.answer(ERROR_TEXT)


@dp.message_handler(state=Numbers.Num2)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        number2 = float(answer.replace(',', '.'))
        if number2 > 0:
            data = await state.get_data()
            number1 = data.get('number_1')
            quest_number = data.get('question_number')
            await message.answer(str(questions[quest_number]).format(number1, number2))
            result = percent_counter(quest_number, number1, number2)
            await message.answer(RESULT_TEXT.format(result))
            await state.finish()
        else:
            await message.answer(NEGATIVE_TEXT)
    except ValueError:
        await message.answer(ERROR_TEXT)