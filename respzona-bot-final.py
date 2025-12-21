import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime


# Логирование с подробностью
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ✅ ПРЯМОЙ ТОКЕН (НЕ ЗАБЫВАЙ ПОТОМ СПРЯТАТЬ)
TOKEN = "8501298263:AAFsKnHjy9ha9pWji7j36kfQ3e5za01aYdQ"

WEBAPP_URL = "https://verdant-paprenjak-887d4a.netlify.app/"
TELEGRAM_URL = "https://t.me/RESPZONA"
YOUTUBE_URL = "https://www.youtube.com/@ANTWOORDMUS"
TIKTOK_URL = "https://www.tiktok.com/@respozona"
YOUTUBE_STREAM_URL = "https://www.youtube.com/live/RESPZONA"
TIKTOK_STREAM_URL = "https://www.tiktok.com/@respozona/live"

# Реквизиты
CARD_NUMBER = "2200 7019 4251 1996"
CARD_HOLDER = "RESPZONA"

USERS_FILE = "users_data.json"

# Твой админ-ID
ADMIN_ID = 8026939529

# Треки
TRACKS = {
    'huday': {
        'name': 'HUDAY',
        'file_id': 'CQACAgIAAxkBAAM6aUWjWuDlBxzAyK-ZQi1JOQ8tvRkAAmuTAALKbTFK7KogMulGkc42BA',
        'date': '19.06.2025',
        'artists': 'Aryx, Nng',
        'genre': 'Мемный поп/рэп',
        'description': 'Мемный по настроению, но при этом завалакивающий трек про бездомного и пирог'
    },
    'huday_phonk': {
        'name': 'HUDAY PHONK',
        'file_id': 'CQACAgIAAxkBAANHaUWluTVBY9v6R2dpf9o1VHJLGpgAApGTAALKbTFKhwWrBH7qkD42BA',
        'date': '30.10.2025',
        'artists': 'Aryx, Nng',
        'genre': 'Phonk/Электроника',
        'description': 'Киберпанк-версия легендарного HUDAY с неоновыми синтезаторами'
    },
    'world_run': {
        'name': 'WORLD RUN PHONK',
        'file_id': 'CQACAgIAAxkBAANJaUWl3P9Epi17pyrTZAABD1gsKLwkAAKUkwACym0xSrJw9quY1smxNgQ',
        'date': '01.11.2025',
        'artists': 'Aryx, Nng',
        'genre': 'Phonk/Киберпанк',
        'description': 'Энергетичный трек про скорость, адреналин и движение'
    },
    'secret': {
        'name': '🔒 СЕКРЕТНЫЙ ТРЕК',
        'file_id': None,
        'date': '❓ Дата секрет',
        'artists': 'Aryx, Nng',
        'genre': 'Сюрприз',
        'description': 'Новый трек выйдет очень скоро! Следи за нашими обновлениями 🎵'
    }
}

# События
EVENTS = [
    {
        'date': '07.01.2025',
        'time': '19:00',
        'title': '🎵 RESPZONA LIVE СТРИМ',
        'description': 'Прямая трансляция музыки и общения с фанатами!',
        'platforms': [
            {'name': '🎬 YouTube', 'url': YOUTUBE_STREAM_URL},
            {'name': '🎵 TikTok', 'url': TIKTOK_STREAM_URL}
        ]
    }
]


# ====================================================================
# Работа с пользователями
# ====================================================================

def load_users_data():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
            return {}
    return {}


def save_users_data(users_data):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        logger.info("✅ Данные пользователей сохранены")
    except Exception as e:
        logger.error(f"❌ Ошибка сохранения данных: {e}")


users_data = load_users_data()


# ====================================================================
# Команды
# ====================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(f"👤 Пользователь {user.first_name} (ID: {user.id}) запустил /start")

    if str(chat_id) not in users_data:
        users_data[str(chat_id)] = {
            'user_id': user.id,
            'username': user.username or 'unknown',
            'first_name': user.first_name,
            'notifications_enabled': True,
            'join_date': datetime.now().isoformat()
        }
        save_users_data(users_data)
        logger.info(f"✅ Новый пользователь добавлен: {user.first_name}")
    else:
        logger.info(f"📝 Пользователь вернулся: {user.first_name}")

    keyboard = [
        [InlineKeyboardButton("🎵 Приложение Respzona", web_app=WebAppInfo(url=WEBAPP_URL))],
        [
            InlineKeyboardButton("🎵 Треки", callback_data='tracks'),
            InlineKeyboardButton("🎟️ Билеты", callback_data='tickets')
        ],
        [
            InlineKeyboardButton("🔔 Уведомления", callback_data='notifications'),
            InlineKeyboardButton("📱 Telegram", url=TELEGRAM_URL)
        ],
        [
            InlineKeyboardButton("💳 Поддержать группу", callback_data='support'),
            InlineKeyboardButton("👥 О нас", callback_data='about')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🎶 Привет, {user.first_name}! Добро пожаловать в RESPZONA! 🎶\n\n"
        f"Мы - музыкальная группа из Уфы и Стерлитамака.\n"
        f"Здесь ты можешь:\n"
        f"✨ Слушать наши треки онлайн\n"
        f"🎤 Узнать о концертах и событиях\n"
        f"🔔 Включить уведомления о новых релизах\n"
        f"💳 Поддержать развитие проекта\n"
        f"📱 Следить за нами в социальных сетях\n\n"
        f"Выбери нужный пункт меню ниже!",
        reply_markup=reply_markup
    )


async def notify_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ У тебя нет прав на отправку уведомлений!\n\n"
            "Это может делать только администратор."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "📢 **Команда отправки уведомлений:**\n\n"
            "Использование:\n"
            "`/notify huday`\n"
            "`/notify huday_phonk`\n"
            "`/notify world_run`\n"
            "`/notify secret`\n\n"
            "**Доступные треки:**\n"
            "🎵 huday\n"
            "🎵 huday_phonk\n"
            "🎵 world_run\n"
            "🔒 secret",
            parse_mode='Markdown'
        )
        return

    track_id = context.args[0]
    if track_id not in TRACKS:
        await update.message.reply_text(
            f"❌ Трек '{track_id}' не найден!\n\n"
            "Доступные треки: huday, huday_phonk, world_run, secret"
        )
        return

    await update.message.reply_text(
        f"📢 Отправляю уведомление о треке '{TRACKS[track_id]['name']}'...\n"
        f"⏳ Это может занять несколько секунд..."
    )

    await send_track_notification(context, track_id)

    await update.message.reply_text(
        f"✅ Уведомление отправлено!\n\n"
        f"📊 Проверь логи для деталей отправки"
    )


async def broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ У тебя нет прав на отправку уведомлений!")
        return

    if not context.args:
        await update.message.reply_text(
            "📢 **Команда отправки своего сообщения:**\n\n"
            "Использование:\n"
            "`/broadcast Ваше сообщение здесь`\n\n"
            "Сообщение будет отправлено всем, кто включил уведомления ✅",
            parse_mode='Markdown'
        )
        return

    message_text = ' '.join(context.args)

    await update.message.reply_text(
        f"📢 Отправляю сообщение:\n\n`{message_text}`\n\n"
        f"⏳ Это может занять несколько секунд...",
        parse_mode='Markdown'
    )

    sent_count = 0
    failed_count = 0

    for chat_id_str, user_data in users_data.items():
        if user_data.get('notifications_enabled', True):
            try:
                chat_id = int(chat_id_str)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"📢 **НОВОЕ СООБЩЕНИЕ:**\n\n{message_text}",
                    parse_mode='Markdown'
                )
                sent_count += 1
                logger.info(f"✅ Сообщение отправлено пользователю {chat_id}")
            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Ошибка отправки сообщения {chat_id_str}: {e}")

    await update.message.reply_text(
        f"✅ **Отправка завершена!**\n\n"
        f"✅ Доставлено: {sent_count}\n"
        f"❌ Ошибок: {failed_count}",
        parse_mode='Markdown'
    )


# ====================================================================
# Медиа / треки / события
# ====================================================================

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("🎵 ПОЛУЧЕН АУДИОФАЙЛ!")
    try:
        audio = update.message.audio
        file_id = audio.file_id
        file_name = audio.file_name or "Unknown"
        duration = audio.duration or 0
        user_name = update.effective_user.first_name

        logger.info(f"📄 Файл: {file_name} | Длина: {duration}s | File ID: {file_id}")

        response_text = (
            f"✅ **АУДИОФАЙЛ ПОЛУЧЕН!**\n\n"
            f"📄 **Название:** `{file_name}`\n"
            f"⏱️ **Длина:** {duration} сек\n"
            f"🆔 **File ID:**\n"
            f"`{file_id}`\n\n"
            f"✅ **Копируй File ID выше и вставь в код бота**"
        )

        await update.message.reply_text(response_text, parse_mode='Markdown')
        logger.info(f"✅ Ответ отправлен пользователю {user_name}")
    except Exception as e:
        logger.error(f"❌ ОШИБКА при обработке аудио: {e}", exc_info=True)
        await update.message.reply_text(
            f"❌ Ошибка при обработке файла:\n\n`{str(e)}`",
            parse_mode='Markdown'
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    if query.data == 'tracks':
        await show_tracks(query, chat_id)
    elif query.data == 'tickets':
        await show_tickets(query, chat_id)
    elif query.data == 'upcoming_events':
        await show_upcoming_events(query, chat_id)
    elif query.data == 'notifications':
        await show_notifications_menu(query, chat_id)
    elif query.data == 'toggle_notifications_action':
        await toggle_notifications(query, chat_id)
    elif query.data == 'support':
        await show_support(query, chat_id)
    elif query.data == 'show_card':
        await show_card_details(query, chat_id)
    elif query.data == 'about':
        await show_about(query)
    elif query.data == 'back_to_menu':
        await back_to_menu(query)
    elif query.data.startswith('play_track_'):
        track_id = query.data.replace('play_track_', '')
        await play_track(query, track_id, context)
    elif query.data.startswith('info_track_'):
        track_id = query.data.replace('info_track_', '')
        await show_track_info(query, track_id)


async def show_tracks(query, chat_id) -> None:
    keyboard = [
        [
            InlineKeyboardButton("🎵 HUDAY", callback_data='info_track_huday'),
            InlineKeyboardButton("▶️ Слушать", callback_data='play_track_huday')
        ],
        [
            InlineKeyboardButton("🎵 HUDAY PHONK", callback_data='info_track_huday_phonk'),
            InlineKeyboardButton("▶️ Слушать", callback_data='play_track_huday_phonk')
        ],
        [
            InlineKeyboardButton("🎵 WORLD RUN PHONK", callback_data='info_track_world_run'),
            InlineKeyboardButton("▶️ Слушать", callback_data='play_track_world_run')
        ],
        [
            InlineKeyboardButton("🔒 СЕКРЕТНЫЙ ТРЕК", callback_data='info_track_secret'),
            InlineKeyboardButton("❓ Узнать", callback_data='info_track_secret')
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="🎵 **Наши треки:**\n\n"
             "Выбери трек для прослушивания или информации:\n\n"
             "🎵 HUDAY - мемный поп/рэп про пирог 🥧\n"
             "🎵 HUDAY PHONK - киберпанк версия 🌆\n"
             "🎵 WORLD RUN PHONK - энергетичный phonk 🏃\n"
             "🔒 СЕКРЕТНЫЙ ТРЕК - выходит скоро! 🎉\n\n"
             "Нажми 'Слушать' для прослушивания или имя для подробностей:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def play_track(query, track_id, context) -> None:
    if track_id not in TRACKS:
        await query.answer("❌ Трек не найден", show_alert=True)
        return

    track = TRACKS[track_id]

    if track['file_id'] is None:
        await query.answer(
            "⚠️ Трек еще не загружен в бота\n\n"
            "1️⃣ Отправь аудиофайл боту\n"
            "2️⃣ Скопируй File ID из ответа\n"
            "3️⃣ Вставь в код TRACKS\n\n"
            "📱 Слушай на @RESPZONA",
            show_alert=True
        )
    else:
        try:
            await context.bot.send_audio(
                chat_id=query.message.chat_id,
                audio=track['file_id'],
                title=track['name'],
                performer='RESPZONA'
            )
            await query.answer(f"▶️ Проигрывается: {track['name']}")
        except Exception as e:
            logger.error(f"Ошибка воспроизведения трека: {e}")
            await query.answer(
                "❌ Ошибка при загрузке трека\n\n"
                "Слушай в Telegram @RESPZONA",
                show_alert=True
            )


async def show_track_info(query, track_id) -> None:
    if track_id not in TRACKS:
        await query.edit_message_text(text="❌ Трек не найден")
        return

    track = TRACKS[track_id]

    keyboard = [
        [InlineKeyboardButton("▶️ Слушать трек", callback_data=f'play_track_{track_id}')],
        [InlineKeyboardButton("⬅️ Назад к трекам", callback_data='tracks')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"🎵 **{track['name']}** 🎵\n\n"
             f"📅 **Дата релиза:** {track['date']}\n"
             f"🎤 **Исполнители:** {track['artists']}\n"
             f"🎸 **Жанр:** {track['genre']}\n\n"
             f"📝 **О треке:**\n"
             f"{track['description']}\n\n"
             f"🔗 **Слушай в социальных сетях:**\n"
             f"📱 {TELEGRAM_URL}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_tickets(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("📅 Предстоящие события", callback_data='upcoming_events')],
        [InlineKeyboardButton("🎟️ Купить билеты (Скоро...)", callback_data='buy_tickets')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="🎟️ **Билеты и события:**\n\n"
             "Функция покупки билетов находится в разработке 🚀\n\n"
             "Скоро вы сможете:\n"
             "✓ Покупать билеты на наши концерты\n"
             "✓ Узнавать о предстоящих событиях\n"
             "✓ Получать приоритетный доступ к билетам\n\n"
             "Подпишитесь на уведомления, чтобы не пропустить!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_upcoming_events(query, chat_id) -> None:
    if not EVENTS:
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='tickets')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="📅 **Предстоящие события:**\n\n❌ Событий пока нет",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    text = "📅 **ПРЕДСТОЯЩИЕ СОБЫТИЯ:**\n\n"
    for event in EVENTS:
        text += f"{'=' * 50}\n"
        text += f"📆 **{event['date']}** | ⏰ **{event['time']}**\n"
        text += f"🎵 **{event['title']}**\n\n"
        text += f"📝 {event['description']}\n\n"
        text += f"**Смотри на:**\n"
        for platform in event['platforms']:
            text += f"🔗 [{platform['name']}]({platform['url']})\n"
        text += "\n"
    text += f"{'=' * 50}\n\n"
    text += "Подпишись на уведомления, чтобы не пропустить! 🔔"

    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='tickets')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# ====================================================================
# Уведомления
# ====================================================================

async def show_notifications_menu(query, chat_id) -> None:
    chat_id_str = str(chat_id)

    if chat_id_str not in users_data:
        users_data[chat_id_str] = {
            'user_id': query.from_user.id,
            'username': query.from_user.username or 'unknown',
            'first_name': query.from_user.first_name,
            'notifications_enabled': True,
            'join_date': datetime.now().isoformat()
        }
        save_users_data(users_data)

    current_status = users_data[chat_id_str]['notifications_enabled']
    status_text = "✅ ВКЛЮЧЕНЫ" if current_status else "❌ ОТКЛЮЧЕНЫ"
    status_icon = "🟢" if current_status else "⭕"
    button_text = "❌ ОТКЛЮЧИТЬ уведомления" if current_status else "✅ ВКЛЮЧИТЬ уведомления"

    keyboard = [
        [InlineKeyboardButton(button_text, callback_data='toggle_notifications_action')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"🔔 **Уведомления о новых релизах:**\n\n"
             f"{status_icon} Текущий статус: {status_text}\n\n"
             f"Когда выйдет новый трек, ты получишь:\n"
             f"🎵 Название трека\n"
             f"📅 Дату релиза\n"
             f"🎤 Информацию об артистах\n"
             f"🎸 Жанр трека\n"
             f"📝 Полное описание\n"
             f"🎧 Аудиофайл для прослушивания\n\n"
             f"💾 **Статус сохранен!** Останется таким пока ты его не изменишь",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def toggle_notifications(query, chat_id) -> None:
    chat_id_str = str(chat_id)

    if chat_id_str in users_data:
        current_status = users_data[chat_id_str]['notifications_enabled']
        users_data[chat_id_str]['notifications_enabled'] = not current_status
        save_users_data(users_data)

        new_status = users_data[chat_id_str]['notifications_enabled']
        status_text = "✅ ВКЛЮЧЕНЫ" if new_status else "❌ ОТКЛЮЧЕНЫ"
        status_icon = "🟢" if new_status else "⭕"

        keyboard = [
            [InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')],
            [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"🔔 **Уведомления о новых релизах:**\n\n"
                 f"{status_icon} Статус: {status_text}\n\n"
                 f"Когда выйдет новый трек, ты получишь:\n"
                 f"🎵 Название трека\n"
                 f"📅 Дату релиза\n"
                 f"🎤 Информацию об артистах\n"
                 f"🎸 Жанр трека\n"
                 f"📝 Полное описание\n"
                 f"🎧 Аудиофайл для прослушивания\n\n"
                 f"💾 **Статус сохранен!** Останется таким пока ты его не изменишь",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


# ====================================================================
# Поддержка / реквизиты
# ====================================================================

async def show_support(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("💳 Реквизиты карты", callback_data='show_card')],
        [InlineKeyboardButton("❤️ Другие способы (Скоро)", callback_data='other_support')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="💳 **Поддержите развитие RESPZONA!** 💳\n\n"
             "Ваша поддержка помогает нам:\n"
             "🎵 Создавать новые треки\n"
             "🎤 Организовывать концерты\n"
             "🎸 Улучшать качество звука\n"
             "📱 Развивать проект\n\n"
             "**Способы поддержки:**\n"
             "💳 Перевод на карту (Т-Банк)\n"
             "❤️ Другие способы скоро будут доступны\n\n"
             "Каждый рубль важен! Спасибо за поддержку! ❤️",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_card_details(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("📋 Скопировать номер", callback_data='copy_card')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="💳 **Реквизиты для поддержки:**\n\n"
             f"**Номер карты:**\n"
             f"`{CARD_NUMBER}`\n\n"
             f"**Получатель:** RESPZONA\n\n"
             f"**Банк:** Т-Банк (Тинькофф)\n\n"
             f"Минимально - 10₽, максимально - ваши возможности! 💰\n\n"
             f"❤️ Спасибо за поддержку проекта!\n\n"
             f"После перевода можешь отправить скриншот @respzonachat для спасибо видеомессажа 🎬",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# ====================================================================
# О нас / главное меню
# ====================================================================

async def show_about(query) -> None:
    keyboard = [
        [InlineKeyboardButton("📱 Telegram канал", url=TELEGRAM_URL)],
        [InlineKeyboardButton("🎬 YouTube канал", url=YOUTUBE_URL)],
        [InlineKeyboardButton("🎵 TikTok", url=TIKTOK_URL)],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="👥 **О RESPZONA:**\n\n"
             "RESPZONA — музыкальная группа из Уфы и Стерлитамака 🎶\n\n"
             "**Команда проекта:**\n"
             "⭐ **Aryx (Арсен)** — главный идеолог, социальные сети, превью, тексты, "
             "программирование и программные функции RESPZONA 💻\n"
             "⭐ **Nng (Дамир)** — главный идеолог, соцсети, превью, тексты, event-менеджер 📱\n"
             "🎸 **nRIS (Радмир)** — помощник проекта, третья гитара, оценщик идей 🎵\n\n"
             "**Наш стиль:** Pop / Rap / Phonk / Electronic 🎵\n\n"
             "**Следи за нами:**\n"
             "📱 Telegram: https://t.me/RESPZONA\n"
             "🎬 YouTube: https://www.youtube.com/@ANTWOORDMUS\n"
             "🎵 TikTok: https://www.tiktok.com/@respozona\n"
             "📧 Email: resp.zona@bk.ru\n\n"
             "Спасибо, что слушаешь RESPZONA! ❤️",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def back_to_menu(query) -> None:
    keyboard = [
        [InlineKeyboardButton("🎵 Приложение Respzona", web_app=WebAppInfo(url=WEBAPP_URL))],
        [
            InlineKeyboardButton("🎵 Треки", callback_data='tracks'),
            InlineKeyboardButton("🎟️ Билеты", callback_data='tickets')
        ],
        [
            InlineKeyboardButton("🔔 Уведомления", callback_data='notifications'),
            InlineKeyboardButton("📱 Telegram", url=TELEGRAM_URL)
        ],
        [
            InlineKeyboardButton("💳 Поддержать группу", callback_data='support'),
            InlineKeyboardButton("👥 О нас", callback_data='about')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="🎶 **RESPZONA - главное меню** 🎶\n\n"
             "Выбери нужный пункт:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# ====================================================================
# Текст
# ====================================================================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()
    logger.info(f"📝 Текстовое сообщение: {user_message}")

    if 'привет' in user_message:
        await update.message.reply_text("Привет! 👋 Используй /start для открытия меню")
    elif 'трек' in user_message or 'музыка' in user_message:
        await update.message.reply_text("Нажми кнопку 🎵 Треки для просмотра наших треков!")
    else:
        await update.message.reply_text(
            "Не поняла команду 🤔\n"
            "Используй /start для открытия меню"
        )


# ====================================================================
# Рассылка уведомлений о треках
# ====================================================================

async def send_track_notification(context: ContextTypes.DEFAULT_TYPE, track_id: str) -> None:
    if track_id not in TRACKS:
        logger.error(f"❌ Трек {track_id} не найден")
        return

    track = TRACKS[track_id]
    sent_count = 0
    failed_count = 0

    for chat_id_str, user_data in users_data.items():
        if user_data.get('notifications_enabled', True):
            try:
                chat_id = int(chat_id_str)
                notification_text = (
                    f"🎵 **НОВЫЙ ТРЕК ВЫПУЩЕН!** 🎵\n\n"
                    f"{'=' * 50}\n"
                    f"🎵 **{track['name']}**\n"
                    f"{'=' * 50}\n\n"
                    f"📅 **Дата релиза:** {track['date']}\n"
                    f"🎤 **Исполнители:** {track['artists']}\n"
                    f"🎸 **Жанр:** {track['genre']}\n\n"
                    f"📝 **О треке:**\n"
                    f"{track['description']}\n\n"
                    f"🎧 Слушай трек ниже 👇"
                )

                await context.bot.send_message(
                    chat_id=chat_id,
                    text=notification_text,
                    parse_mode='Markdown'
                )

                if track['file_id'] is not None:
                    await context.bot.send_audio(
                        chat_id=chat_id,
                        audio=track['file_id'],
                        title=track['name'],
                        performer='RESPZONA'
                    )

                sent_count += 1
                logger.info(f"✅ Уведомление отправлено пользователю {chat_id}")
            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Ошибка отправки уведомления пользователю {chat_id_str}: {e}")

    logger.info(f"📊 Уведомления: отправлено {sent_count}, ошибок {failed_count}")


# ====================================================================
# MAIN
# ====================================================================

def main() -> None:
    logger.info("=" * 50)
    logger.info("🚀 ЗАПУСК БОТА RESPZONA")
    logger.info(f"📊 Загружено {len(users_data)} пользователей")
    logger.info("=" * 50)

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("notify", notify_handler))
    application.add_handler(CommandHandler("broadcast", broadcast_handler))

    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("🎵 БОТ ГОТОВ К РАБОТЕ!")
    logger.info("=" * 50)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
