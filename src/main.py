from config import tg_bot_token
from Check_Function import proverka,is_zero_and_neg

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from string import digits, ascii_letters, punctuation, ascii_uppercase, ascii_lowercase
from random import choice
import math
from time import sleep


bot = Bot(token=tg_bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создаём класс для пароля
class Password(StatesGroup):
    num = State()
    symb=State()

#Создаём класс для суммы и указываем поля
class Geom(StatesGroup):
    first_num = State()
    num_of_num = State()
    den = State() #знаменатель

#Creating buttons

inline_butt_01=InlineKeyboardButton('Сумма',callback_data='sum')
inline_butt_02=InlineKeyboardButton('Пароль',callback_data='gen')

murkup_1=InlineKeyboardMarkup().add(inline_butt_01,inline_butt_02)

#CrEATING iNLINE bUTTONS
inline_butt_1=InlineKeyboardButton('Простой',callback_data='Simple')
inline_butt_2=InlineKeyboardButton('Средний',callback_data='Average')
inline_butt_3=InlineKeyboardButton('Сложный',callback_data='Strong')
inline_butt_4=InlineKeyboardButton('Кастомный',callback_data='Custom')
inline_butt_4_1=InlineKeyboardButton('На главную',callback_data='call_start')

all_inline_1=InlineKeyboardMarkup().add(inline_butt_1,inline_butt_2,inline_butt_3,inline_butt_4).add(inline_butt_4_1)


inline_butt_5=InlineKeyboardButton('Заглавные символы',callback_data='Big_Letters')
inline_butt_6=InlineKeyboardButton('Строчные символы',callback_data='Low_Letters')
inline_butt_7=InlineKeyboardButton('Числа',callback_data='Numbers')
inline_butt_8=InlineKeyboardButton('Пунктационные знаки',callback_data='Punk')
inline_butt_9=InlineKeyboardButton('Длина',callback_data='Length')
inline_butt_10=InlineKeyboardButton('Свои символы',callback_data='Your Sumbols')
inline_butt_11=InlineKeyboardButton('Получить пароль',callback_data='PassWord')

all_inline_2=InlineKeyboardMarkup(row_width=1).add(inline_butt_5,inline_butt_6,inline_butt_7,inline_butt_8,inline_butt_9,inline_butt_10,inline_butt_11)

inline_butt_12=InlineKeyboardButton('Подтвердить',callback_data='Confirm')

all_inline_3=InlineKeyboardMarkup().add(inline_butt_12)

inline_butt_13=InlineKeyboardButton('Назад',callback_data='Back')
inline_butt_14=InlineKeyboardButton('Добавить символы',callback_data='Input_Uzer_Symbols')
inline_butt_15=InlineKeyboardButton('Удалить добавленные символы',callback_data='Delete_Uzer_Symbols')
inline_butt_16=InlineKeyboardButton('Просмотреть символы',callback_data='Show_Symbols')

all_inline_4=InlineKeyboardMarkup(row_width=2).add(inline_butt_13,inline_butt_14)
all_inline_5=InlineKeyboardMarkup(row_width=2).add(inline_butt_13,inline_butt_14,inline_butt_15)#.add(inline_butt_16)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет, Я бот CoolChill и я помогу тебе посчитать сумму геометрической прогресии или сделать надёжный пароль.",reply_markup=murkup_1)

@dp.callback_query_handler(text='call_start')
async def start_command(callback_query:types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await callback_query.message.answer("Привет, Я бот CoolChill и я помогу тебе посчитать сумму геометрической прогресии или сделать надёжный пароль.",reply_markup=murkup_1)

# Добавляем возможность отмены, если пользователь передумал заполнять
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')



################################################################################################################################
################################################################################################################################
################################################################################################################################



# Генератор пароля
YourSumbols_input=''
Sumbols = [YourSumbols_input]
BIGLET='❌'
LITLET='❌'
NUMBERS='❌'
PUNK='❌'
SUMB='❌'
LEN=int(8)
#,digits,punctuation,ascii_lowercase,ascii_uppercase

async def process_callback_button4(callback_query: types.CallbackQuery):
    #global BIGLET,LITLET,NUMBERS,PUNK,LEN
    await bot.answer_callback_query(callback_query.id)
    try:
        await callback_query.message.delete()
    except Exception:
        pass
    await callback_query.message.answer('--- Настройки пароля ---\n'
                                        '\n'
                                        f'Заглавные символы {BIGLET}\n'
                                        '\n'
                                        f'Строчные символы {LITLET}\n'
                                        '\n'
                                        f'Числа {NUMBERS}\n'
                                        '\n'
                                        f'Пунктационные знаки {PUNK}\n'
                                        '\n'
                                        f'Длинна {LEN}\n'
                                        '\n'
                                        f'Свои символы {SUMB}',reply_markup=all_inline_2)



@dp.callback_query_handler(text='gen')
async def get_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer('Какой пароль хотите получить?',reply_markup=all_inline_1)
    await callback_query.message.delete()


#Тут Простой пароль
@dp.callback_query_handler(lambda c: c.data == 'Simple')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    all = ascii_letters
    password = ''.join(choice(all) for _ in (range(8)))
    await bot.send_message(callback_query.from_user.id, f'Ваш пароль:\n{password}',reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Назад',callback_data='gen')))

#Тут Средний пароль
@dp.callback_query_handler(lambda c: c.data == 'Average')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    all = digits+ascii_letters
    password = ''.join(choice(all) for _ in (range(10)))
    await bot.send_message(callback_query.from_user.id, f'Ваш пароль:\n{password}',reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Назад',callback_data='gen')))

#Тут Сложный пароль
@dp.callback_query_handler(lambda c: c.data == 'Strong')
async def process_callback_button3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    all = digits+ascii_letters+punctuation
    password = ''.join(choice(all) for _ in (range(12)))
    await bot.send_message(callback_query.from_user.id, f'Ваш пароль:\n{password}',reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Назад',callback_data='gen')))


@dp.callback_query_handler(lambda c: c.data == 'Custom')
async def gg(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await process_callback_button4(callback_query)

@dp.callback_query_handler(lambda c:c.data=='Big_Letters')
async def process_callback_BL(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    global BIGLET, Sumbols
    if BIGLET=='✅':
        Sumbols.remove(ascii_uppercase)
        BIGLET='❌'
    else:
        Sumbols+=[ascii_uppercase]
        BIGLET='✅'
    await process_callback_button4(callback_query)

@dp.callback_query_handler(lambda c:c.data=='Low_Letters')
async def process_callback_LL(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    global LITLET, Sumbols
    if LITLET=='✅':
        Sumbols.remove(ascii_lowercase)
        LITLET='❌'
    else:
        Sumbols+=[ascii_lowercase]
        LITLET='✅'
    await process_callback_button4(callback_query)

@dp.callback_query_handler(lambda c:c.data=='Numbers')
async def process_callback_NUM_1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    global NUMBERS,Sumbols
    if NUMBERS=='✅':
        Sumbols.remove(digits)
        NUMBERS='❌'
    else:
        Sumbols+=[digits]
        NUMBERS='✅'
    await process_callback_button4(callback_query)

@dp.callback_query_handler(lambda c:c.data=='Punk')
async def process_callback_PUNKT(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    global PUNK, Sumbols
    if PUNK=='✅':
        Sumbols.remove(punctuation)
        PUNK='❌'
    else:
        Sumbols+=[punctuation]
        PUNK='✅'
    await process_callback_button4(callback_query)

@dp.callback_query_handler(lambda c:c.data=='Length')
async def process_callback_en(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.answer_callback_query(callback_query.id)
    await Password.num.set()
    await callback_query.message.answer('Введите длину пароля')


@dp.message_handler(lambda message: (not proverka(message.text) or not is_zero_and_neg(message.text)), state=Password.num)
async def process_num_invalid(message: types.Message):
    await message.reply("Длина пароля может быть только целым положительным числом и не равным нулю!")
    sleep(0.5)
    await message.answer('Повтроите ввод или нажмите /cancel')

@dp.message_handler(lambda message:len(message.text)>4000, state=Password.num)
async def process_num_invalid(message: types.Message):
    await message.reply("Длина пароля не может превышать 4000 символов")
    sleep(0.5)
    await message.answer('Повтроите ввод или нажмите /cancel')

@dp.message_handler(state=Password.num)
async def pass_len(message: types.Message, state: FSMContext):
    global LEN
    async with state.proxy() as data:
        data['num']=message.text
        LEN=int(data['num'])
    await message.answer('{}'.format(LEN), reply_markup=all_inline_3)
    await state.reset_state (with_data = False)


@dp.callback_query_handler(text="Confirm")
async def conf(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    return await process_callback_button4(callback_query)



@dp.callback_query_handler(text='Your Sumbols')
async def your_sumbols_1(callback_query:types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    Chek=True if len(Sumbols[0])==0 else False
    await callback_query.message.answer('--- Настройки символов ---',reply_markup=all_inline_4 if Chek else all_inline_5)

@dp.callback_query_handler(text='Back')
async def go_back_to_menu(callback_query:types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await process_callback_button4(callback_query)

@dp.callback_query_handler(text='Input_Uzer_Symbols')
async def uzers_symbols(callback_query:types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await Password.symb.set()
    await callback_query.message.answer('Введите символы')

Uzer_Input_Sumbols=''

@dp.message_handler(state=Password.symb)
async def pass_len(message: types.Message, state: FSMContext):
    global Sumbols,Uzer_Input_Sumbols,SUMB
    SUMB = '✅'
    async with state.proxy() as data:
        data['symb']=message.text
        if len(Sumbols[0])==0:
            Sumbols[0]+=data['symb']
            Uzer_Input_Sumbols+=data['symb']
        else:
            Sumbols[0]=''
            Uzer_Input_Sumbols+=data['symb']
            Sumbols[0]+=Uzer_Input_Sumbols
    await message.answer('Введённые символы:\n{}'.format(Sumbols[0]), reply_markup=all_inline_3)
    await state.reset_state (with_data = False)

@dp.callback_query_handler(text='Delete_Uzer_Symbols')
async def delete_uzers_symbols(callback_query:types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    global Sumbols,Uzer_Input_Sumbols,SUMB
    SUMB = '❌'
    Sumbols[0]=''
    Uzer_Input_Sumbols=''
    await state.update_data(symb='')
    await callback_query.message.answer('Успешно удалено')
    await process_callback_button4(callback_query)




@dp.callback_query_handler(lambda c:c.data=='PassWord')
async def process_callback_NUM(callback_query: types.CallbackQuery,state:FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    global YourSumbols_input,BIGLET,LITLET,NUMBERS,PUNK,SUMB,LEN,Sumbols
    all=''.join(Sumbols)
    if len(all)==0:
        await callback_query.message.answer('Выберите, что входит в пароль или введите свои символы',reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('К настройкам',callback_data='Custom')))
    else:#4096 макс число символов в сообщении
        password = ''.join(choice(all) for _ in (range(LEN)))
       #if len(password) > 4096:
       #    try:
       #        for x in range(0, len(password), 4096):
       #            await callback_query.message.answer(password[x:x + 4096])
       #    except Exception:
       #        pass

        await callback_query.message.answer(f'Ваш пароль:\n{password}',reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('На главную',callback_data='call_start')))

        YourSumbols_input = ''
        BIGLET = '❌'
        LITLET = '❌'
        NUMBERS = '❌'
        PUNK = '❌'
        SUMB = '❌'
        LEN = int(8)

        Sumbols = [YourSumbols_input]
        await state.finish()


################################################################################################################################
################################################################################################################################



# Сумма геометрической прогрессии
@dp.callback_query_handler(text='sum')
async def get_info(callback_query:types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await Geom.first_num.set()
    await callback_query.message.answer("Ведите число, с которого будем начинать считать сумму геометрической прогрессии")

#Проверяем первое число на цифры
@dp.message_handler(lambda message: not proverka(message.text), state=Geom.first_num)
async def process_num_invalid(message: types.Message):
    await message.reply("Число не может состоять из букв")
    sleep(0.5)
    await message.answer('Повтроите ввод или нажмите /cancel')

# Сюда приходит ответ с первым числом и принимается кол-во чисел
@dp.message_handler(state=Geom.first_num)
async def process_pass(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_num'] = message.text

    await Geom.next()
    await message.answer("А теперь количество множителей")


#Проверяем кол-во чиел на целое число
@dp.message_handler(lambda message: (not proverka(message.text) or not is_zero_and_neg(message.text)), state=Geom.num_of_num)
async def process_num_invalid(message: types.Message):
    await message.reply("Количество множителей может быть только целым положительным числом и не равным нулю!")
    sleep(0.5)
    await message.answer('Повтроите ввод или нажмите /cancel')

# Сюда приходит ответ с кол-вом чисел и принимается знаменатель
@dp.message_handler(state=Geom.num_of_num)
async def process_pass(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['num_of_num'] = message.text

    await Geom.next()
    await message.answer("И наконец значение знаменателя")

#Проверяем знаменатель на цифры
@dp.message_handler(lambda message: not proverka(message.text), state=Geom.den)
async def process_num_invalid(message: types.Message):
    await message.reply("Знаменатель должен состоять из чисел.\nНапример, 3.14")
    sleep(0.5)
    await message.answer('Повтроите ввод или нажмите /cancel')

# Сюда приходит ответ с знаменателем и происходят расчёты
@dp.message_handler(state=Geom.den)
async def process_pass(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['den'] = message.text

        n=0
        b=0
        for c in range(int(float(data['first_num'])), (int(float(data['first_num']))+int(float(data['num_of_num'])))):
            if c == int(float(data['first_num'])):
                n = float(data['first_num'])
                b = n
                continue
            if int(float(data['num_of_num'])) != 1:
                n *= float(data['den'])
                b += n
        if math.isinf(b):
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text('Первое число:', md.hbold(float(data['first_num']))),
                    md.text('Кол-во чисел:', md.hbold(float(data['num_of_num']))),
                    md.text('Знаменатель:', md.hbold(float(data['den']))),
                    sep='\n',
                ), parse_mode=ParseMode.HTML)
            await message.answer('Упсс, кажется, даже я сбился со счёта. Попробуй другие числа)')
        else:
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text('Первое число:', md.hbold(float(data['first_num']))),
                    md.text('Кол-во чисел:', md.hbold(float(data['num_of_num']))),
                    md.text('Знаменатель:', md.hbold(float(data['den']))),
                    md.text(),
                    md.text('Сумма:',(b)),
                    sep='\n',
                        ),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('На главную',callback_data='call_start')))
            await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




