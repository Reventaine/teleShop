import logging
import psycopg2

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
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
)

import sections.config as config
import sections.admin as admin
import sections.teleShop as shop

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

conn = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password, host=config.host)
cursor = conn.cursor()

CATALOG, REGISTER, ADMIN, ADMIN_PRICE, ADMIN_IMAGE, ADMIN_ADD = range(6)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == "/start":
        await update.message.reply_text(
            "Hello! We welcome you in our shop!",
        )

    reply_keyboard = [
        ["Catalog"],
        ['Cart'],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "How can I help you?",
        reply_markup=markup,
    )

    return CATALOG


def main() -> None:
    application = Application.builder().token(config.teleToken).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("admin3517", admin.start),
            CommandHandler("register", shop.registration),
        ],
        states={
            CATALOG: [
                MessageHandler(filters.Regex("^(Catalog)$"), shop.catalog),
                MessageHandler(filters.Regex("^(PC|Switch)$"), shop.show_games),
                ],
            REGISTER: [
                MessageHandler(filters.TEXT, shop.enter_email),
            ],
            ADMIN: [MessageHandler(filters.TEXT, admin.consolename), ],
            ADMIN_PRICE: [MessageHandler(filters.TEXT, admin.price), ],
            ADMIN_IMAGE: [MessageHandler(filters.TEXT, admin.image), ],
            ADMIN_ADD: [MessageHandler(filters.TEXT, admin.add), ],
        },
        fallbacks=[CommandHandler("start", start), MessageHandler(filters.Regex("^BACK$"), start)], allow_reentry=True,
    )

    application.add_handler(MessageHandler(filters.Regex("^Cart$"), shop.cart))
    application.add_handler(CallbackQueryHandler(shop.addtocart)),
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
