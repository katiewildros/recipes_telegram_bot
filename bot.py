import logging
import notion
import helper

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

config = helper.read_config()
TELEGRAM_TOKEN = config['TOKENS']['TELEGRAM_TOKEN']

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    button1 = types.KeyboardButton('Узнать')
    button2 = types.KeyboardButton('Добавить')
    button3 = types.KeyboardButton('Удалить')
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
        button1, button2, button3
    )
    await message.reply("Привет! Что ты хочешь сделать?", reply_markup=mark)

# ------------------------------------------
# This part allows to get the recipes
# ------------------------------------------
@dp.message_handler(text=['Узнать'])
async def get_tags(message: types.Message):

    # This function allows to get a list of tags

    pages = notion.get_pages()
    tags = []
    for page in pages:
        props = page["properties"]
        tags_json = props["Tags"]["select"]["name"]
        tags.append(tags_json)
    all_tags = list(set(tags))

    markup_tags = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for tag in all_tags:
        markup_tags.add(types.KeyboardButton(tag))
    await message.reply("Выбери категорию", reply_markup=markup_tags)

@dp.message_handler(text=['завтрак', 'суп', 'второе', 'десерты', 'начинки'])
async def get_recipes(message: types.Message):

        # This function allows to get a list of recipes

    text_btn = message.text
    pages = notion.get_pages()
    names = []
    names_url_dict = {}
    for page in pages:
        props = page["properties"]
        url_item = props["URL"]["url"]
        name_item = props["Name"]["title"][0]["text"]["content"]
        tags_json = props["Tags"]["select"]["name"]
        if tags_json == text_btn:
            names_url_dict[name_item] = url_item
            names.append(name_item)

    markup_names = types.InlineKeyboardButton(names[0], url = names_url_dict.get(names[0]))
    inline_names = types.InlineKeyboardMarkup(row_width=2).add(markup_names)
    if len(names) > 1:
        for name in names[1:]:
            inline_names.add(types.InlineKeyboardButton(name, url = names_url_dict.get(name)))

    await message.reply("Выбери рецепт", reply_markup=inline_names)

if __name__ == '__main__':
    executor.start_polling(dp)