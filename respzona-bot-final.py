import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
import random

# Логирование с подробностью
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ✅ ПРЯМОЙ ТОКЕН
TOKEN = "8351765550:AAFyuAfkijrRN8EB4t7EG-64sXNLUqDAZd0"

WEBAPP_URL = "https://resp1-two.vercel.app/"
TELEGRAM_URL = "https://t.me/RESPZONA"
YOUTUBE_URL = "https://www.youtube.com/@respzonamus"
TIKTOK_URL = "https://www.tiktok.com/@respozona"

# ⭐ ССЫЛКИ НА ПОДДЕРЖКУ
YOOMONEY_URL = "https://yoomoney.ru/to/4100118663676748"
BOOSTY_DONATE_URL = "https://boosty.to/respzona/donate"

# Реквизиты
CARD_NUMBER = "2200 7019 4251 1996"
CARD_HOLDER = "RESPZONA"

USERS_FILE = "users_data.json"
POLLS_FILE = "polls_data.json"

# Твой админ-ID
ADMIN_ID = 8026939529

# ====================================================================
# СЛУЧАЙНЫЕ МОТИВИРУЮЩИЕ ЦИТАТЫ 💪
# ====================================================================
MOTIVATIONAL_QUOTES = [
    "🎵 Музыка - это язык, который говорит во всех местах мира! ❤️",
    "🎸 Каждый звук - это чудо! Слушай с открытым сердцем 🎧",
    "🎤 RESPZONA создаёт не просто музыку, а эмоции! 🔥",
    "🌟 Поддержи нас донатом и помоги создавать лучшую музыку! 💎",
    "🚀 Это только начало! Скоро будет много нового! 🎉",
    "💫 Спасибо за то, что веришь в нас! Вы - наша мотивация! 💪",
    "🎵 Между музыкой и молчанием есть время - слушай RESPZONA! 🎶",
    "🔥 Phonk не просто жанр - это стиль жизни! ⚡",
]

# Треки
TRACKS = {
    'huday': {
        'name': 'HUDAY',
        'file_id': 'CQACAgIAAxkBAANhaVaocDVsMGfqD7ydZ8PusmNYc60AAt2QAAIRtrhKGcu5eMwsApI4BA',
        'date': '19.06.2025',
        'artists': 'Aryx, Nng',
        'genre': 'Мемный поп/рэп',
        'description': 'Мемный по настроению, но при этом завалакивающий трек про бездомного и пирог',
        'emoji': '🥧'
    },
    'huday_phonk': {
        'name': 'HUDAY PHONK',
        'file_id': 'CQACAgIAAxkBAANjaVaoty9NuQjt01IoWbxIS8kMyEMAAuKQAAIRtrhKvfyGOcOPtZI4BA',
        'date': '30.10.2025',
        'artists': 'Aryx, Nng',
        'genre': 'Phonk/Электроника',
        'description': 'Киберпанк-версия легендарного HUDAY с неоновыми синтезаторами',
        'emoji': '🌆'
    },
    'world_run': {
        'name': 'WORLD RUN PHONK',
        'file_id': 'CQACAgIAAxkBAANlaVao18Y2p2sq4dulIj5OJrg6rA4AAuWQAAIRtrhKHo_Cz9bMz004BA',
        'date': '01.11.2025',
        'artists': 'Aryx, Nng',
        'genre': 'Phonk/Киберпанк',
        'description': 'Энергетичный трек про скорость, адреналин и движение',
        'emoji': '🏃'
    },
    'midnight_glow': {
        'name': '🌙 MIDNIGHT GLOW',
        'file_id': None,
        'date': '❓ Скоро',
        'artists': 'Aryx, Nng',
        'genre': 'Электроника/Лирика',
        'description': 'Новый трек выходит очень скоро! Ночной звук с лирическим посланием',
        'emoji': '🌙'
    }
}

# События (Архив)
EVENTS = [
    {
        'date': '07.01.2025',
        'time': '19:00',
        'title': '🎉 БОЛЬШОЙ НОВОГОДНИЙ СТРИМ',
        'description': 'Масштабная новогодняя трансляция музыки, веселья и общения с фанатами!',
        'platforms': [
            {'name': '🎬 YouTube', 'url': 'https://www.youtube.com/@respzonamus'},
            {'name': '🎵 TikTok Live', 'url': 'https://www.tiktok.com/@respozona'},
            {'name': '💎 Boosty', 'url': 'https://boosty.to/respzona'}
        ]
    }
]

# ====================================================================
# Работа с пользователями
# ====================================================================

def load_json_file(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки {filename}: {e}")
            return {}
    return {}

def save_json_file(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ Данные сохранены в {filename}")
    except Exception as e:
        logger.error(f"❌ Ошибка сохранения {filename}: {e}")

users_data = load_json_file(USERS_FILE)
polls_data = load_json_file(POLLS_FILE)

# ====================================================================
# ОПРОСЫ И ГОЛОСОВАНИЕ 📊
# ====================================================================

async def show_polls_menu(query) -> None:
    """Показывает меню опросов"""
    
    keyboard = [
        [InlineKeyboardButton("🎵 Текущий опрос", callback_data='current_poll')],
        [InlineKeyboardButton("📈 Результаты", callback_data='poll_results')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="📊 **ОПРОСЫ И ГОЛОСОВАНИЯ** 📊\n\n"
             "Помогите нам выбрать будущие треки!\n\n"
             "🎵 **Текущий опрос:** Какой стиль трека хочешь услышать?\n\n"
             "Голосуй и влияй на музыку группы!\n"
             "Каждый голос важен для RESPZONA! 💜",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_current_poll(query) -> None:
    """Показывает текущий опрос"""
    
    poll_options = [
        ("🔥 PHONK", "phonk"),
        ("💔 ЛИРИКА", "lyric"),
        ("🎤 РЭП", "rap"),
        ("🎸 РОК", "rock"),
    ]
    
    keyboard = []
    for option_text, option_id in poll_options:
        keyboard.append([
            InlineKeyboardButton(option_text, callback_data=f'vote_poll_{option_id}')
        ])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='polls_menu')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🎵 **ОПРОС: КАКОЙ СТИЛЬ ТРЕКА ХОЧЕШЬ УСЛЫШАТЬ?**\n\n"
             "Выбери свой любимый стиль:\n\n"
             "🔥 **PHONK** - Киберпанк и электроника\n"
             "💔 **ЛИРИКА** - Душевные и трогательные треки\n"
             "🎤 **РЭП** - Хип-хоп и рэп\n"
             "🎸 **РОК** - Гитарные композиции\n\n"
             "Каждый голос влияет на будущее музыку группы!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def vote_poll(query, option_id: str) -> None:
    """Голосование в опросе"""
    user_id = query.from_user.id
    
    if 'polls' not in polls_data:
        polls_data['polls'] = {}
    
    if 'main_poll' not in polls_data['polls']:
        polls_data['polls']['main_poll'] = {
            'phonk': 0,
            'lyric': 0,
            'rap': 0,
            'rock': 0,
            'voters': []
        }
    
    # Проверка что уже голосовал
    if user_id in polls_data['polls']['main_poll']['voters']:
        await query.answer("⚠️ Ты уже голосовал в этом опросе!", show_alert=True)
        return
    
    # Учитываем голос
    polls_data['polls']['main_poll'][option_id] += 1
    polls_data['polls']['main_poll']['voters'].append(user_id)
    save_json_file(POLLS_FILE, polls_data)
    
    await query.answer("✅ Твой голос учтен!")
    logger.info(f"✅ Голос учтен: {user_id} → {option_id}")

async def show_poll_results(query) -> None:
    """Показывает результаты опроса"""
    
    if 'polls' not in polls_data or 'main_poll' not in polls_data['polls']:
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='polls_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="📊 Опрос еще не начался",
            reply_markup=reply_markup
        )
        return
    
    poll = polls_data['polls']['main_poll']
    
    # Подсчитываем результаты
    options = {
        'phonk': ('🔥 PHONK', poll.get('phonk', 0)),
        'lyric': ('💔 ЛИРИКА', poll.get('lyric', 0)),
        'rap': ('🎤 РЭП', poll.get('rap', 0)),
        'rock': ('🎸 РОК', poll.get('rock', 0)),
    }
    
    total = sum(count for _, count in options.values())
    
    text = "📊 **РЕЗУЛЬТАТЫ ОПРОСА**\n\n"
    
    if total == 0:
        text += "Голосов еще нет 😢\n"
    else:
        sorted_options = sorted(options.items(), key=lambda x: x[1][1], reverse=True)
        
        for idx, (_, (name, count)) in enumerate(sorted_options, 1):
            percentage = (count / total) * 100
            bar_length = 10
            filled = int((percentage / 100) * bar_length)
            bar = "🟩" * filled + "⬜" * (bar_length - filled)
            
            text += f"{idx}. {name}\n"
            text += f"   {bar} {percentage:.0f}% ({count} голосов)\n\n"
    
    text += f"💬 **Всего голосов:** {total}\n\n"
    text += "Опрос закончится 31.01.2026\n"
    text += "Выигравший стиль будет использован в новом треке!"
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='polls_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ====================================================================
# ОСНОВНЫЕ ФУНКЦИИ
# ====================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id
    chat_id_str = str(chat_id)
    
    # Добавляем пользователя в БД
    if chat_id_str not in users_data:
        users_data[chat_id_str] = {
            'user_id': user.id,
            'username': user.username or 'unknown',
            'first_name': user.first_name,
            'notifications_enabled': True,
            'join_date': datetime.now().isoformat(),
            'is_admin': user.id == ADMIN_ID
        }
        save_json_file(USERS_FILE, users_data)
        logger.info(f"✅ Новый пользователь: {user.first_name}")
    
    # МЕНЮ ДЛЯ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
    keyboard = [
        [InlineKeyboardButton("🎵 Приложение Respzona", web_app=WebAppInfo(url=WEBAPP_URL))],
        [
            InlineKeyboardButton("🎵 Треки", callback_data='tracks'),
            InlineKeyboardButton("📰 Новости", callback_data='news')
        ],
        [
            InlineKeyboardButton("💳 Донаты", callback_data='donates'),
            InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')
        ],
        [
            InlineKeyboardButton("👥 О нас", callback_data='about'),
        ],
        [
            InlineKeyboardButton("📊 Опросы", callback_data='polls_menu'),
        ],
        [InlineKeyboardButton("📱 Telegram", url=TELEGRAM_URL)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🎶 Привет, {user.first_name}! Добро пожаловать в RESPZONA! 🎶\n\n"
        f"Мы - музыкальная группа из Уфы.\n"
        f"Здесь ты можешь:\n"
        f"✨ Слушать наши треки онлайн\n"
        f"📰 Читать последние новости\n"
        f"💳 Поддержать развитие проекта\n"
        f"🔔 Включить уведомления о новых релизах\n"
        f"📱 Следить за нами в социальных сетях\n\n"
        f"Выбери нужный пункт меню ниже!",
        reply_markup=reply_markup
    )

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
            InlineKeyboardButton("🎵 WORLD RUN", callback_data='info_track_world_run'),
            InlineKeyboardButton("▶️ Слушать", callback_data='play_track_world_run')
        ],
        [
            InlineKeyboardButton("🌙 MIDNIGHT GLOW", callback_data='info_track_midnight_glow'),
            InlineKeyboardButton("❓ Узнать", callback_data='info_track_midnight_glow')
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    quote = random.choice(MOTIVATIONAL_QUOTES)

    await query.edit_message_text(
        text=(
            "🎵 **Наши треки:**\n\n"
            "Выбери трек для прослушивания или информации:\n\n"
            "🎵 HUDAY - мемный поп/рэп про пирог 🥧\n"
            "🎵 HUDAY PHONK - киберпанк версия 🌆\n"
            "🎵 WORLD RUN PHONK - энергетичный phonk 🏃\n"
            "🌙 MIDNIGHT GLOW - новый трек выходит скоро! 🌙\n\n"
            "Нажми 'Слушать' для прослушивания или имя для подробностей:\n\n"
            f"💭 *{quote}*"
        ),
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
            "⚠️ Этот трек еще не вышел! 🔒\n\n"
            "Следи за нашими обновлениями чтобы не пропустить релиз! 🎵\n\n"
            "📱 Подпишись на уведомления",
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
            await query.answer(f"✅ Отправляю: {track['name']}")
            logger.info(f"✅ Трек {track_id} отправлен пользователю {query.message.chat_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка воспроизведения трека: {e}")
            await query.answer(
                "❌ Ошибка при загрузке трека\n\n"
                "Слушай на YouTube @respzonamus",
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
        text=(
            f"🎵 **{track['name']}** 🎵\n\n"
            f"📅 **Дата релиза:** {track['date']}\n"
            f"🎤 **Исполнители:** {track['artists']}\n"
            f"🎸 **Жанр:** {track['genre']}\n\n"
            f"📝 **О треке:**\n"
            f"{track['description']}\n\n"
            f"🔗 **Слушай в социальных сетях:**\n"
            f"📱 {TELEGRAM_URL}"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_news(query, chat_id) -> None:
    """Показывает страницу новостей с архивом событий"""
    keyboard = [
        [InlineKeyboardButton("📅 Архив событий", callback_data='events_archive')],
        [InlineKeyboardButton("🎵 Новые треки", callback_data='new_tracks_news')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "📰 **НОВОСТИ И ОБНОВЛЕНИЯ:**\n\n"
            "Последние новости RESPZONA:\n\n"
            "🎵 **Новые треки** - смотри информацию о наших последних релизах\n"
            "📅 **Архив событий** - вспоминай прошлые трансляции и события\n\n"
            "Подпишись на уведомления, чтобы не пропустить ничего! 🔔"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_events_archive(query, chat_id) -> None:
    """Показывает архив событий"""
    if not EVENTS:
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='news')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="📅 **Архив событий:**\n\n❌ События пока не добавлены",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    text = "📅 **АРХИВ СОБЫТИЙ:**\n\n"
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
    text += "Спасибо, что были вместе с нами! 🎶"

    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='news')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_new_tracks_news(query, chat_id) -> None:
    """Показывает информацию о новых треках"""
    keyboard = [
        [InlineKeyboardButton("🎵 Слушать все треки", callback_data='tracks')],
        [InlineKeyboardButton("⬅️ Назад к новостям", callback_data='news')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "🎵 **НОВЫЕ ТРЕКИ:**\n\n"
            "Последние релизы RESPZONA:\n\n"
            "🌙 **MIDNIGHT GLOW** - Скоро выходит!\n"
            "Электроника/Лирика - новый трек с лирическим посланием\n\n"
            "Следи за нашими социальными сетями, чтобы узнать точную дату релиза! 🔔\n\n"
            "📱 Подпишись на уведомления и первым узнаешь о новых треках!"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_donates(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("💎 Boosty Донаты", callback_data='show_boosty')],
        [InlineKeyboardButton("💳 Номер карты", callback_data='show_card')],
        [InlineKeyboardButton("💰 YooMoney", callback_data='show_yoomoney')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "💳 **ВКЛАДКА ДОНАТОВ** 💳\n\n"
            "Поддержи RESPZONA - выбери способ:\n\n"
            "💎 **Boosty** - самый удобный способ\n"
            "💳 **Карта** - прямой перевод\n"
            "💰 **YooMoney** - цифровой кошелек\n\n"
            "Каждый донат помогает нам создавать лучшую музыку! ❤️"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_boosty_details(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("💎 Перейти на Boosty", url=BOOSTY_DONATE_URL)],
        [InlineKeyboardButton("⬅️ Назад к донатам", callback_data='donates')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "💎 **DONATES НА BOOSTY:**\n\n"
            "Самый удобный и безопасный способ поддержать группу!\n\n"
            "✨ **Что ты получишь:**\n"
            "💝 Спасибо видеомессаж от группы\n"
            "🎁 Эксклюзивный контент для донаторов\n"
            "🎵 Доступ к премиум постам\n"
            "💬 Прямой контакт с нами\n"
            "🏆 Статус 'Поддержчик' в чате\n\n"
            "🔗 Нажми кнопку ниже и донати! 👇"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

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
        save_json_file(USERS_FILE, users_data)

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
        text=(
            "🔔 **Уведомления о новых релизах:**\n\n"
            f"{status_icon} Текущий статус: {status_text}\n\n"
            "Когда выйдет новый трек, ты получишь:\n"
            "🎵 Название трека\n"
            "📅 Дату релиза\n"
            "🎤 Информацию об артистах\n"
            "🎸 Жанр трека\n"
            "📝 Полное описание\n"
            "🎧 Аудиофайл для прослушивания\n\n"
            "💾 **Статус сохранен!** Останется таким пока ты его не изменишь"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def toggle_notifications(query, chat_id) -> None:
    chat_id_str = str(chat_id)

    if chat_id_str in users_data:
        current_status = users_data[chat_id_str]['notifications_enabled']
        users_data[chat_id_str]['notifications_enabled'] = not current_status
        save_json_file(USERS_FILE, users_data)

        new_status = users_data[chat_id_str]['notifications_enabled']
        status_text = "✅ ВКЛЮЧЕНЫ" if new_status else "❌ ОТКЛЮЧЕНЫ"
        status_icon = "🟢" if new_status else "⭕"

        keyboard = [
            [InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')],
            [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=(
                "🔔 **Уведомления о новых релизах:**\n\n"
                f"{status_icon} Статус: {status_text}\n\n"
                "Когда выйдет новый трек, ты получишь:\n"
                "🎵 Название трека\n"
                "📅 Дату релиза\n"
                "🎤 Информацию об артистах\n"
                "🎸 Жанр трека\n"
                "📝 Полное описание\n"
                "🎧 Аудиофайл для прослушивания\n\n"
                "💾 **Статус сохранен!** Останется таким пока ты его не изменишь"
            ),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def show_about(query) -> None:
    keyboard = [
        [InlineKeyboardButton("📱 Telegram канал", url=TELEGRAM_URL)],
        [InlineKeyboardButton("🎬 YouTube канал", url=YOUTUBE_URL)],
        [InlineKeyboardButton("🎵 TikTok", url=TIKTOK_URL)],
        [InlineKeyboardButton("📧 Написать нам", callback_data='contact_us')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "👥 **О RESPZONA:**\n\n"
            "RESPZONA — музыкальная группа из Уфы 🎶\n\n"
            "**Команда проекта:**\n"
            "⭐ **Aryx** — главный идеолог\n"
            "⭐ **Nng** — главный идеолог\n"
            "🎸 **nRIS** — помощник проекта\n\n"
            "**Наш стиль:** Pop / Rap / Phonk / Electronic 🎵\n\n"
            "**Следи за нами:**\n"
            "📱 Telegram: https://t.me/RESPZONA\n"
            "🎬 YouTube: https://www.youtube.com/@respzonamus\n"
            "🎵 TikTok: https://www.tiktok.com/@respozona\n"
            "📧 Email: resp.zona@bk.ru\n\n"
            "Спасибо, что слушаешь RESPZONA! ❤️"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_contact_us(query) -> None:
    """Показывает информацию о сотрудничестве"""
    keyboard = [
        [InlineKeyboardButton("💬 Telegram чат", url="https://t.me/respzonachat")],
        [InlineKeyboardButton("📧 Email: resp.zona@bk.ru", callback_data='copy_email')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=(
            "🤝 **СОТРУДНИЧЕСТВО:**\n\n"
            "Ты хочешь сотрудничать с нами? Отлично! 🎵\n\n"
            "✨ **Мы открыты для:**\n"
            "🎨 Дизайнеров (обложки, визуалы, мерч)\n"
            "🎬 Видеографов (клипы, превью, обработка)\n"
            "🎤 Певцов и рэперов (фичеры, синглы)\n"
            "🎵 Продюсеров (создание биов, миксинг)\n"
            "📱 Маркетологов (SMM, реклама)\n"
            "💻 Программистов (сайты, боты, приложения)\n"
            "🎸 Музыкантов (гитара, бас, ударные)\n\n"
            "💬 **Как с нами связаться:**\n"
            "Telegram чат или напиши на почту resp.zona@bk.ru\n\n"
            "📝 **Расскажи нам:**\n"
            "• Кто ты и чем занимаешься\n"
            "• Какой идеей ты хочешь помочь\n"
            "• Портфолио или примеры работ\n"
            "• Твои контакты для связи\n\n"
            "⚡ Мы ответим в течение 24 часов!\n\n"
            "Давай создавать крутую музыку вместе! 🚀"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_card_details(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад к донатам", callback_data='donates')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "💳 **Реквизиты карты:**\n\n"
            f"**Номер карты:**\n"
            f"`{CARD_NUMBER}`\n\n"
            f"**Получатель:** RESPZONA\n\n"
            "Любая сумма поддержки! 💰\n\n"
            "❤️ Спасибо за поддержку проекта!\n\n"
            "После перевода можешь отправить скриншот @respzonachat для спасибо видеомессажа 🎬"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_yoomoney_details(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("💳 Перейти в YooMoney", url=YOOMONEY_URL)],
        [InlineKeyboardButton("⬅️ Назад к донатам", callback_data='donates')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "💰 **YooMoney (Яндекс.Касса):**\n\n"
            "Быстрый способ поддержать группу через цифровой кошелек!\n\n"
            "✨ **Преимущества:**\n"
            "✅ Быстрое пополнение\n"
            "✅ Безопасно\n"
            "✅ Любая сумма\n\n"
            "💰 Любая сумма поддержки важна!\n\n"
            "❤️ Спасибо за поддержку проекта!\n\n"
            "После пополнения можешь отправить скриншот @respzonachat для спасибо видеомессажа 🎬"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def back_to_menu(query) -> None:
    # МЕНЮ ДЛЯ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
    keyboard = [
        [InlineKeyboardButton("🎵 Приложение Respzona", web_app=WebAppInfo(url=WEBAPP_URL))],
        [
            InlineKeyboardButton("🎵 Треки", callback_data='tracks'),
            InlineKeyboardButton("📰 Новости", callback_data='news')
        ],
        [
            InlineKeyboardButton("💳 Донаты", callback_data='donates'),
            InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')
        ],
        [
            InlineKeyboardButton("👥 О нас", callback_data='about'),
        ],
        [
            InlineKeyboardButton("📊 Опросы", callback_data='polls_menu'),
        ],
        [InlineKeyboardButton("📱 Telegram", url=TELEGRAM_URL)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="🎶 **RESPZONA - главное меню** 🎶\n\nВыбери нужный пункт:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    try:
        if query.data == 'tracks':
            await show_tracks(query, chat_id)
        elif query.data == 'news':
            await show_news(query, chat_id)
        elif query.data == 'events_archive':
            await show_events_archive(query, chat_id)
        elif query.data == 'new_tracks_news':
            await show_new_tracks_news(query, chat_id)
        elif query.data == 'donates':
            await show_donates(query, chat_id)
        elif query.data == 'notifications':
            await show_notifications_menu(query, chat_id)
        elif query.data == 'toggle_notifications_action':
            await toggle_notifications(query, chat_id)
        elif query.data == 'show_card':
            await show_card_details(query, chat_id)
        elif query.data == 'show_yoomoney':
            await show_yoomoney_details(query, chat_id)
        elif query.data == 'show_boosty':
            await show_boosty_details(query, chat_id)
        elif query.data == 'about':
            await show_about(query)
        elif query.data == 'contact_us':
            await show_contact_us(query)
        elif query.data == 'back_to_menu':
            await back_to_menu(query)
        elif query.data.startswith('play_track_'):
            track_id = query.data.replace('play_track_', '')
            await play_track(query, track_id, context)
        elif query.data.startswith('info_track_'):
            track_id = query.data.replace('info_track_', '')
            await show_track_info(query, track_id)
        
        # Опросы
        elif query.data == 'polls_menu':
            await show_polls_menu(query)
        elif query.data == 'current_poll':
            await show_current_poll(query)
        elif query.data.startswith('vote_poll_'):
            option_id = query.data.replace('vote_poll_', '')
            await vote_poll(query, option_id)
        elif query.data == 'poll_results':
            await show_poll_results(query)
    
    except Exception as e:
        logger.error(f"❌ Ошибка в button_callback: {e}", exc_info=True)
        await query.answer(f"❌ Произошла ошибка: {str(e)}", show_alert=True)

def main() -> None:
    logger.info("=" * 70)
    logger.info("🚀 ЗАПУСК БОТА RESPZONA V10")
    logger.info(f"📊 Загружено {len(users_data)} пользователей")
    logger.info("=" * 70)

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: None))

    logger.info("🎵 БОТ RESPZONA V10 ГОТОВ К РАБОТЕ!")
    logger.info("=" * 70)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
