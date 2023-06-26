import logging
from aiogram import Bot, Dispatcher, executor, types
import messages, predicts

API_TOKEN = 'TOKEN'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

button_texts = list()



async def commands_list_menu(disp):
    await disp.bot.set_my_commands([
        types.BotCommand("start", "info"),
        types.BotCommand("help", "same as start"),
        types.BotCommand("recommend", "Ex: after prompt write a movie name"),
    ])

# Start
@dp.message_handler(commands=['start', 'help'])
async def start_(message: types.Message):
    await message.reply(messages.start_message)


# Recommend
@dp.message_handler(commands=['recommend'])
async def recommend_(message: types.Message):
    text = message.get_args()
    if text == '':
        await message.reply(messages.empty_recommend)

    else:
        text = predicts.nlp(text)


        similar_titles = predicts.select_title(text)
        keyboard = types.InlineKeyboardMarkup()

        for sm_title in similar_titles:
            title = sm_title[0]
            button_texts.append(str(title))
            keyboard.add(types.InlineKeyboardButton(text=str(title), callback_data=str(title)))

        await message.reply('Which one did you mean? ', reply_markup=keyboard)


@dp.callback_query_handler(text=button_texts)
async def handle_callbacks(call: types.CallbackQuery):
    similar_10 = predicts.similar_movies(call.data)

    response = ''
    for i, tpl in enumerate(similar_10, 2):
        if tpl[2] > 0.4:
            response += f'{tpl[0]}  --> Score: {round(tpl[2] * 100, 1)}% ⬆️️\n\n'
        else:
            response += f'{tpl[0]}  --> Score: {round(tpl[2] * 100, 1)}% ↗️️\n\n'

    await call.message.answer('<b>🤖 Here are 10 movies that are similar in genre or theme🤖</b> \n\n\n' \
                              + response, parse_mode=types.ParseMode.HTML)


executor.start_polling(dp)
