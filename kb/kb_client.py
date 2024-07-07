from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
one_marcup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True


).add(
    KeyboardButton("Brawl Stars"),
    KeyboardButton("Free Fire"),
    KeyboardButton("Pubg mobile"),

)

bs_marcup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True


).add(
    KeyboardButton("ОДИНОЧНЫЙ"),
    KeyboardButton("КОМАНДНЫЙ"),


)


menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True


).add(
    KeyboardButton("/start"),



)


