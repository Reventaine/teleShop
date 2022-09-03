# main shop functions to bot
import logging
import re

import psycopg2
import config


from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

conn = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password, host=config.host)
cursor = conn.cursor()

cursor.execute(f'''CREATE TABLE IF NOT EXISTS public."TeleShop"
(
    "ID" serial PRIMARY KEY,
    "Game" character varying PRIMARY KEY UNIQUE,
    "Console" character varying NOT NULL,
    "Price" numeric PRIMARY KEY NOT NULL,
    "Cover" text
    )''')

cursor.execute(f'''CREATE TABLE IF NOT EXISTS public."Users"
(
    "User_ID" integer PRIMARY KEY UNIQUE,
    "Email" character varying NOT NULL,
    "GamesBought" character varying,
    CONSTRAINT "GamesBought" FOREIGN KEY ("GamesBought")
        REFERENCES public."TeleShop" ("Game") MATCH SIMPLE
    )''')

conn.commit()


def create_cart():
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS public."Cart"
    (
        "Buyer" integer,
        "Game" character varying,
        "Price" numeric,
        CONSTRAINT "Buyer" FOREIGN KEY ("User_ID")
            REFERENCES public."Users" ("User_ID") MATCH SIMPLE,
        CONSTRAINT "Game" FOREIGN KEY ("Game")
            REFERENCES public."TeleShop" ("Game") MATCH SIMPLE,  
        CONSTRAINT "Price" FOREIGN KEY ("Price")
            REFERENCES public."TeleShop" ("Price") MATCH SIMPLE
        )''')

    conn.commit()


CATALOG, REGISTER, ADMIN, ADMIN_PRICE, ADMIN_IMAGE, ADMIN_ADD = range(6)


# iterator for shop table
def all_games():
    cursor.execute(f'''SELECT * FROM public."TeleShop" WHERE "Console"='{console_name}' ''')
    records = cursor.fetchall()
    for i in range(len(records)):
        yield records[i]


async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text

    if text == "Catalog":

        reply_keyboard = [
            ["PC"],
            ['Switch'],
            ['BACK'],
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)

        await update.message.reply_text(
            "Please select your console",
            reply_markup=markup
        )

        return CATALOG

    elif text == '/admin3517':
        return ADMIN_START


async def show_games(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    global console_name

    if text == "PC":
        console_name = 'PC'

    elif text == "Switch":
        console_name = 'Switch'

    for elem in all_games():
        keyboard = [
            [InlineKeyboardButton(text=f"Price: ${elem[3]}", callback_data=elem[1]), ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_photo(elem[4], caption=f'*{elem[1]} \({text}\)*', reply_markup=reply_markup,
                                         parse_mode='MarkdownV2')


async def addtocart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton(text=f'In cart 🛒', parse_mode='MarkdownV2', callback_data='ADD')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()
    #create_cart()
    #cursor.execute(f'''INSERT INTO public."Cart"("Buyer", "Game", "Price")VALUES ('{user_id}', '{query.data}');''')
    #conn.commit()
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ['BACK'],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Your cart is empty", reply_markup=markup)

    return CATALOG


######### Registration of user contact info ############

async def registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ReplyKeyboardRemove()
    await update.message.reply_text("Enter your email")
    return REGISTER


async def enter_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Committing user info...')
    email = update.message.text
    user_id = update.effective_user.id

    if re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
        try:
            cursor.execute(
                f'''INSERT INTO public."Users"("User_ID", "Email")
                             VALUES ('{user_id}', '{email}');''')
            conn.commit()
            await update.message.reply_text("Email saved")
        except:
            await update.message.reply_text('User exists')
    else:
        await update.message.reply_text("Wrong email")

