# admin functions to bot
import psycopg2
import sections.config as config

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
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

CATALOG, REGISTER, ADMIN, ADMIN_PRICE, ADMIN_IMAGE, ADMIN_ADD = range(6)

conn = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password, host=config.host)
cursor = conn.cursor()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ReplyKeyboardRemove()
    await update.message.reply_text(text=f'Enter the title of the game')
    return ADMIN


async def consolename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    gamename = update.message.text
    context.user_data["gamename"] = gamename
    await update.message.reply_text(text=f'Enter console')
    return ADMIN_PRICE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    consolename = update.message.text
    context.user_data["consolename"] = consolename
    await update.message.reply_text(text=f'Enter price')
    return ADMIN_IMAGE


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    price = update.message.text
    context.user_data["price"] = price
    await update.message.reply_text(text=f'Paste URL link to image cover')
    return ADMIN_ADD


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    gamename = context.user_data["gamename"]
    consolename = context.user_data["consolename"]
    price = context.user_data["price"]
    imageurl = update.message.text

    try:
        cursor.execute(
            f'''INSERT INTO public."TeleShop"("Game", "Console", "Price", "Cover")
                VALUES ('{gamename}', '{consolename}', {price}, '{imageurl}');''')

        conn.commit()
        context.user_data.clear()
        await update.message.reply_text('Succes')
        return ConversationHandler.END
    except:
        await update.message.reply_text('Wrong input')

