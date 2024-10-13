
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен бота
API_TOKEN = '7743338045:AAEVi1F7sakeT44C7MavxiYTmbQhnSzUuss'

# Правильные ответы и соответствующие изображения
CORRECT_ANSWERS = {
    '1': ("5", 'answers/ex1/1.1_ans.jpg'),
    '2': ("10", 'answers/ex2/1_ans.jpg'),
    '3': ("5", 'answers/ex3/3_ans.jpg'),
    '4': ("0,995", 'answers/ex4/4_ans.jpg'),
    '5': ("0,6", 'answers/ex5/5_ans.jpg'),
    '6': ("13", 'answers/ex6/6_ans.jpg'),
    '7': ("80", 'answers/ex7/7_ans.jpg'),
    '8': ("20", 'answers/ex8/8_ans.jpg'),
    '9': ("25", 'answers/ex9/9_ans.jpg'),
    '10': ("20", 'answers/ex10/10_ans.jpg'),
    '11': ("-10", 'answers/ex11/11_ans.jpg'),
    '12': ("2", 'answers/ex12/12_ans.jpg'),
    '13': ('представлен ниже', 'answers/ex13/13_ans.jpg'),
    '14': ('представлен ниже', 'answers/ex14/14_ans.jpg'),
    '15': ('представлен ниже', 'answers/ex15/15_ans.jpg'),
    '16': ('представлен ниже', 'answers/ex16/16_ans.jpg'),
    '17': ('представлен ниже', 'answers/ex17/17_ans.jpg'),
    '18': ('представлен ниже', 'answers/ex18/18_ans.jpg'),
    '19': ('представлен ниже', 'answers/ex18/18_ans.jpg')
}

# Условия заданий и пути к изображениям
TASKS = {
    '1': ("Условие задания 1:", 'answers/ex1/1_1.jpg'),
    '2': ("Условие задания 2:", 'answers/ex2/1.jpg'),
    '3': ("Условие задания 3: Два ребра прямоугольного параллелепипеда, выходящие из одной вершины, равны 3 и 4. Площадь"
          " поверхности этого параллелепипеда равна 94. Найдите третье ребро, выходящее из той же вершины.", 'answers/ex3/3.jpg'),
    '4': ("Условие задания 4: В среднем из 1400 садовых насосов, поступивших в продажу, 7 подтекают. Найдите вероятность"
          " того, что один случайно выбранный для контроля насос не подтекает.", 'answers/ex4/4.jpg'),
    '5': ("Условие задания 5: Агрофирма закупает куриные яйца только в двух домашних хозяйствах. Известно, что 5% яиц из"
          " первого хозяйства — яйца высшей категории, а из второго хозяйства — 30% яиц высшей категории. В этой агрофирме"
          " 15% яиц высшей категории. Найдите вероятность того, что яйцо, купленное у этой агрофирмы, окажется из первого"
          " хозяйства.", 'answers/ex5/5.jpg'),
    '6': ("Условие задания 6:", 'answers/ex6/6.jpg'),
    '7': ("Условие задания 7:", 'answers/ex7/7.jpg'),
    '8': ("Условие задания 8:", 'answers/ex8/8_1.jpg'),
    '9': ("Условие задания 9:", 'answers/ex9/9.jpg'),
    '10': ("Условие задания 10: В понедельник акции компании подорожали на некоторое количество процентов, а во вторник "
           "подешевели на то же самое количество процентов. В результате они стали стоить на  дешевле, чем при открытии "
           "торгов в понедельник. На сколько процентов подорожали акции компании в понедельник?", 'answers/ex10/10.jpg'),
    '11': ("Условие задания 11:", 'answers/ex11/11.jpg'),
    '12': ("Условие задания 12:", 'answers/ex12/12.jpg'),
    '13': ("Условие задания 13:", 'answers/ex13/13_1.jpg'),
    '14': ("Условие задания 14:", 'answers/ex14/14.jpg'),
    '15': ("Условие задания 15:", 'answers/ex15/15.jpg'),
    '16': ("Условие задания 16: \n В банк был положен вклад под 10% годовых. Через год, после начисления процентов, вкладчик"
           " снял со счета 2000 рублей, а еще через год (опять после начисления процентов) снова внес 2000 рублей. Вследствие "
           "этих действий через три года со времени открытия вклада вкладчик получил сумму меньше запланированной (если бы не"
           " было промежуточных операций со вкладом). На сколько рублей меньше запланированной суммы он получил?", 'answers/ex16/16.jpg'),
    '17': ("Условие задания 17:", 'answers/ex17/17.jpg'),
    '18': ("Условие задания 18:", 'answers/ex18/18.jpg'),
    '19': ("Условие задания 19:", 'answers/ex19/19.jpg')
}

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()


# Состояния для FSM
class QuizState(StatesGroup):
    waiting_for_answer = State()


@router.message(Command('start'))
async def start(message: types.Message):
    # Приветственное сообщение
    welcome_message = (
        "Привет! Я ваш сборник заданий ЕГЭ по математике.\n"
    )
    await message.answer(welcome_message)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 часть", callback_data='1_part')],
        [InlineKeyboardButton(text="2 часть", callback_data='2_part')]
    ])
    await message.answer("Выберите часть экзамена:", reply_markup=keyboard)


@router.callback_query(F.data == '1_part')
async def show_part1(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(i), callback_data=f'task_{i}') for i in range(1, 7)],
        [InlineKeyboardButton(text=str(i), callback_data=f'task_{i}') for i in range(8, 13)],
        [InlineKeyboardButton(text="Вернуться к выбору частей", callback_data='return_to_parts')]
    ])
    await callback_query.message.edit_text("Выберите задание из 1 части:", reply_markup=keyboard)


@router.callback_query(F.data == '2_part')
async def show_part2(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(i), callback_data=f'task_{i}') for i in range(13, 20)],
        [InlineKeyboardButton(text="Вернуться к выбору частей", callback_data='return_to_parts')]
    ])
    await callback_query.message.edit_text("Выберите задание из 2 части:", reply_markup=keyboard)


@router.callback_query(F.data.startswith('task_'))
async def show_task(callback_query: types.CallbackQuery, state: FSMContext):
    task_number = callback_query.data.split('_')[1]

    task_text, image_path = TASKS[task_number]

    if task_number in ['13', '14', '15', '16', '17', '18', '19']:
        # Если это задание из 2 части, сразу предлагаем показать ответ
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Показать ответ", callback_data=f'view_answer_{task_number}')]
            # [InlineKeyboardButton(text="Вернуться к выбору частей", callback_data='return_to_parts')]
        ])
        await callback_query.message.answer(task_text, reply_markup=keyboard)
        # Отправляем изображение задания, если оно есть
        if image_path:
            await callback_query.message.answer_photo(types.FSInputFile(image_path))
    else:
        await callback_query.message.answer(task_text)
        await state.set_state(QuizState.waiting_for_answer)
        await state.update_data(task_number=task_number)
        if image_path:
            await callback_query.message.answer_photo(types.FSInputFile(image_path))
        await callback_query.message.answer("Введите ваш ответ:")

@router.callback_query(F.data == 'return_to_parts')
async def return_to_parts(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 часть", callback_data='1_part')],
        [InlineKeyboardButton(text="2 часть", callback_data='2_part')]
    ])
    await callback_query.message.edit_text("Выберите часть:", reply_markup=keyboard)


@router.message(QuizState.waiting_for_answer)
async def process_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_number = data.get('task_number')

    if task_number in CORRECT_ANSWERS:
        correct_answer, answer_image = CORRECT_ANSWERS[task_number]

        if message.text == correct_answer:
            await message.answer("Правильно! Вы решили задачу верно.")

            await state.clear()

        else:
            # Создаем кнопку для просмотра правильного ответа
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Посмотреть ответ", callback_data=f'view_answer_{task_number}')]
            ])
            await message.answer("Неправильно. Попробуйте ещё раз или посмотрите правильный ответ.",
                                 reply_markup=keyboard)
    else:
        await message.answer("Произошла ошибка. Попробуйте заново.")
        await state.clear()



@router.callback_query(F.data.startswith('view_answer_'))
async def view_answer(callback_query: types.CallbackQuery):
    task_number = callback_query.data.split('_')[2]
    if task_number in CORRECT_ANSWERS:
        correct_answer, answer_image = CORRECT_ANSWERS[task_number]
        await callback_query.message.answer(f"Правильный ответ на задание {task_number}: {correct_answer}")

        # Отправляем изображение с правильным ответом, если оно есть
        if answer_image:
            await callback_query.message.answer_photo(types.FSInputFile(answer_image))

    await callback_query.answer()  # Убираем спиннер


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
