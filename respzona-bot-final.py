import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
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
YOUTUBE_STREAM_URL = "https://www.youtube.com/live/RESPZONA"
TIKTOK_STREAM_URL = "https://www.tiktok.com/@respozona/live"

# ⭐ ССЫЛКИ НА ПОДДЕРЖКУ
YOOMONEY_URL = "https://yoomoney.ru/to/4100118663676748"
MERCH_URL = "https://respzona-merch.printful.com/"
BOOSTY_DONATE_URL = "https://boosty.to/respzona/donate"

# 🤝 СОТРУДНИЧЕСТВО
COLLABORATION_CONTACT = "@aryxresp"

# Реквизиты
CARD_NUMBER = "2200 7019 4251 1996"
CARD_HOLDER = "RESPZONA"

USERS_FILE = "users_data.json"
RATINGS_FILE = "ratings_data.json"
GALLERY_FILE = "gallery_data.json"
REFERRALS_FILE = "referrals_data.json"

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

# События
EVENTS = [
    {
        'date': '07.01.2025',
        'time': '19:00',
        'title': '🎉 БОЛЬШОЙ НОВОГОДНИЙ СТРИМ',
        'description': 'Масштабная новогодняя трансляция музыки, веселья и общения с фанатами!',
        'platforms': [
            {'name': '🎬 YouTube (БЕСПЛАТНО)', 'url': YOUTUBE_STREAM_URL},
            {'name': '🎵 TikTok Live (БЕСПЛАТНО)', 'url': TIKTOK_STREAM_URL},
            {'name': '💎 Boosty (БЕСПЛАТНО)', 'url': BOOSTY_DONATE_URL}
        ]
    },
    {
        'date': '❓ Дата секрет',
        'time': '⏰ Время неизвестно',
        'title': '🎵 ТРЕК СЮРПРИЗ 🎵',
        'description': 'Самый ожидаемый момент! Будет шокирующее объявление! Подписывайся чтобы не пропустить!',
        'platforms': [
            {'name': '📱 Telegram', 'url': TELEGRAM_URL},
            {'name': '🎬 YouTube', 'url': YOUTUBE_URL},
            {'name': '🎵 TikTok', 'url': TIKTOK_URL}
        ]
    }
]

# ====================================================================
# ВИКТОРИНА О RESPZONA 🎯
# ====================================================================
QUIZ_QUESTIONS = [
    {
        'question': 'Из каких городов состоит RESPZONA?',
        'options': ['Уфа и Стерлитамак', 'Казань и Уфа', 'Москва и Уфа', 'СПб и Казань'],
        'correct': 0,
        'emoji': '🏙️'
    },
    {
        'question': 'Сколько главных членов в группе?',
        'options': ['2', '3', '4', '5'],
        'correct': 1,
        'emoji': '👥'
    },
    {
        'question': 'Какой жанр НЕ входит в стиль RESPZONA?',
        'options': ['Классика', 'Phonk', 'Pop', 'Rap'],
        'correct': 0,
        'emoji': '🎸'
    },
    {
        'question': 'Как зовут администратора бота?',
        'options': ['Nng', 'Aryx', 'nRIS', 'RESPZONA'],
        'correct': 1,
        'emoji': '🤖'
    },
    {
        'question': 'Какой трек вышел 19.06.2025?',
        'options': ['WORLD RUN', 'HUDAY PHONK', 'HUDAY', 'MIDNIGHT GLOW'],
        'correct': 2,
        'emoji': '🎵'
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
ratings_data = load_json_file(RATINGS_FILE)
gallery_data = load_json_file(GALLERY_FILE)
referrals_data = load_json_file(REFERRALS_FILE)

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
            'join_date': datetime.now().isoformat(),
            'referrer_id': None,
            'referral_count': 0
        }
        save_json_file(USERS_FILE, users_data)
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
            InlineKeyboardButton("💳 Донаты", callback_data='donates'),
            InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')
        ],
        [
            InlineKeyboardButton("👥 О нас", callback_data='about'),
            InlineKeyboardButton("🤝 Сотрудничество", callback_data='collaboration')
        ],
        [
            InlineKeyboardButton("🎯 Викторина", callback_data='quiz_start'),
            InlineKeyboardButton("🏆 Рейтинги", callback_data='ratings')
        ],
        [InlineKeyboardButton("📱 Telegram", url=TELEGRAM_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🎶 Привет, {user.first_name}! Добро пожаловать в RESPZONA! 🎶\n\n"
        f"Мы - музыкальная группа из Уфы и Стерлитамака.\n"
        f"Здесь ты можешь:\n"
        f"✨ Слушать наши треки онлайн\n"
        f"🎤 Узнать о концертах и событиях\n"
        f"💳 Поддержать развитие проекта\n"
        f"🔔 Включить уведомления о новых релизах\n"
        f"🎯 Сыграть в викторину\n"
        f"🏆 Посмотреть рейтинг треков\n"
        f"📱 Следить за нами в социальных сетях\n\n"
        f"Выбери нужный пункт меню ниже!",
        reply_markup=reply_markup
    )

# ====================================================================
# НОВАЯ: СИСТЕМА РЕЙТИНГА ТРЕКОВ ⭐
# ====================================================================

async def show_track_ratings(query) -> None:
    """Показывает рейтинги всех треков"""
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    
    text = "🏆 **РЕЙТИНГ ТРЕКОВ RESPZONA:**\n\n"
    
    for track_id, track_info in TRACKS.items():
        if track_id in ratings_data:
            ratings = ratings_data[track_id]
            likes = ratings.get('likes', 0)
            dislikes = ratings.get('dislikes', 0)
            total = likes + dislikes
            
            if total > 0:
                percentage = (likes / total) * 100
            else:
                percentage = 0
            
            bar_length = 10
            filled = int((percentage / 100) * bar_length)
            bar = "🟩" * filled + "⬜" * (bar_length - filled)
            
            text += f"{track_info['emoji']} **{track_info['name']}**\n"
            text += f"👍 {likes} | 👎 {dislikes} | {percentage:.0f}%\n"
            text += f"{bar}\n\n"
        else:
            text += f"{track_info['emoji']} **{track_info['name']}**\n"
            text += "Еще никто не голосовал!\n\n"
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def rate_track(query, track_id, rating) -> None:
    """Голосует за трек (Like/Dislike)"""
    user_id = query.from_user.id
    
    if track_id not in ratings_data:
        ratings_data[track_id] = {'likes': 0, 'dislikes': 0, 'voted_users': []}
    
    if user_id in ratings_data[track_id]['voted_users']:
        await query.answer("⚠️ Ты уже голосовал за этот трек!", show_alert=True)
        return
    
    if rating == 'like':
        ratings_data[track_id]['likes'] += 1
        await query.answer("👍 Спасибо за оценку!")
    else:
        ratings_data[track_id]['dislikes'] += 1
        await query.answer("👎 Спасибо за отзыв!")
    
    ratings_data[track_id]['voted_users'].append(user_id)
    save_json_file(RATINGS_FILE, ratings_data)

# ====================================================================
# НОВАЯ: ВИКТОРИНА 🎯
# ====================================================================

async def start_quiz(query) -> None:
    """Начинает викторину"""
    user_id = query.from_user.id
    
    context.user_data = context.user_data or {}
    context.user_data[user_id] = {
        'quiz_active': True,
        'question_num': 0,
        'score': 0
    }
    
    await show_quiz_question(query, context, user_id)

async def show_quiz_question(query, context, user_id) -> None:
    """Показывает вопрос викторины"""
    user_data = context.user_data.get(user_id, {})
    question_num = user_data.get('question_num', 0)
    
    if question_num >= len(QUIZ_QUESTIONS):
        # Викторина завершена
        score = user_data.get('score', 0)
        total = len(QUIZ_QUESTIONS)
        percentage = (score / total) * 100
        
        emoji_result = "🏆" if percentage >= 80 else "✅" if percentage >= 50 else "❌"
        
        keyboard = [
            [InlineKeyboardButton("🎯 Заново", callback_data='quiz_start')],
            [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=f"{emoji_result} **ВИКТОРИНА ЗАВЕРШЕНА!**\n\n"
                 f"Твой результат: **{score}/{total}** ({percentage:.0f}%)\n\n"
                 f"{'🥇 Отличный результат! Ты супер-фан RESPZONA!' if percentage >= 80 else '✨ Хороший результат!' if percentage >= 50 else '📚 Не расстраивайся, слушай побольше нашей музыки!'}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    question_data = QUIZ_QUESTIONS[question_num]
    question_text = question_data['question']
    options = question_data['options']
    emoji = question_data['emoji']
    
    keyboard = []
    for i, option in enumerate(options):
        keyboard.append([
            InlineKeyboardButton(option, callback_data=f'quiz_answer_{question_num}_{i}')
        ])
    keyboard.append([
        InlineKeyboardButton("❌ Выход", callback_data='back_to_menu')
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"{emoji} **ВИКТОРИНА О RESPZONA** {emoji}\n\n"
             f"Вопрос {question_num + 1}/{len(QUIZ_QUESTIONS)}\n\n"
             f"**{question_text}**",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def check_quiz_answer(query, context, question_num, answer) -> None:
    """Проверяет ответ"""
    user_id = query.from_user.id
    user_data = context.user_data.get(user_id, {})
    
    question_data = QUIZ_QUESTIONS[question_num]
    correct_answer = question_data['correct']
    
    if answer == correct_answer:
        user_data['score'] = user_data.get('score', 0) + 1
        await query.answer("✅ Правильно!")
    else:
        await query.answer(f"❌ Неправильно! Правильный ответ: {question_data['options'][correct_answer]}")
    
    user_data['question_num'] = question_num + 1
    context.user_data[user_id] = user_data
    
    await show_quiz_question(query, context, user_id)

# ====================================================================
# КОМАНДА /broadcast - отправка рассылки всем пользователям
# ====================================================================

async def broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ У тебя нет прав на отправку рассылок!\n\n"
            "Это может делать только администратор."
        )
        logger.warning(f"⚠️ Попытка рассылки от неавторизованного пользователя: {update.effective_user.id}")
        return

    if not context.args:
        await update.message.reply_text(
            "📢 **Команда отправки своего сообщения:**\n\n"
            "Использование:\n"
            "`/broadcast Ваше сообщение здесь`\n\n"
            "Примеры:\n"
            "`/broadcast 🎉 Новый трек выпущен!`\n"
            "`/broadcast Привет всем! Спасибо за поддержку ❤️`\n\n"
            "Сообщение будет отправлено всем, у кого включены уведомления ✅",
            parse_mode='Markdown'
        )
        return

    message_text = ' '.join(context.args)
    
    if len(message_text) > 4096:
        await update.message.reply_text(
            f"❌ Сообщение слишком длинное!\n\n"
            f"Максимум: 4096 символов\n"
            f"Ваше сообщение: {len(message_text)} символов"
        )
        return

    await update.message.reply_text(
        f"📢 **Отправляю рассылку:**\n\n"
        f"``````\n\n"
        f"⏳ Это может занять несколько секунд...",
        parse_mode='Markdown'
    )

    sent_count = 0
    failed_count = 0
    blocked_count = 0

    for chat_id_str, user_data in users_data.items():
        if user_data.get('notifications_enabled', True):
            try:
                chat_id = int(chat_id_str)
                
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"📢 **НОВОЕ СООБЩЕНИЕ ОТ RESPZONA:**\n\n{message_text}",
                    parse_mode='Markdown'
                )
                sent_count += 1
                logger.info(f"✅ Сообщение отправлено пользователю {chat_id} (@{user_data.get('username', 'unknown')})")
                
            except Exception as e:
                error_msg = str(e).lower()
                
                if 'blocked' in error_msg or 'forbidden' in error_msg:
                    blocked_count += 1
                    logger.warning(f"🚫 Пользователь {chat_id_str} заблокировал бота")
                    user_data['notifications_enabled'] = False
                    save_json_file(USERS_FILE, users_data)
                else:
                    failed_count += 1
                    logger.error(f"❌ Ошибка отправки сообщения {chat_id_str}: {e}")

    save_json_file(USERS_FILE, users_data)

    report_text = (
        f"✅ **РАССЫЛКА ЗАВЕРШЕНА!**\n\n"
        f"📊 **Статистика:**\n"
        f"✅ Доставлено: **{sent_count}**\n"
        f"❌ Ошибок: **{failed_count}**\n"
        f"🚫 Заблокировано: **{blocked_count}**\n"
        f"📈 Всего пользователей: **{len(users_data)}**\n\n"
        f"💬 **Отправленное сообщение:**\n"
        f"``````"
    )
    
    await update.message.reply_text(report_text, parse_mode='Markdown')
    
    logger.info(
        f"📊 РАССЫЛКА ЗАВЕРШЕНА: "
        f"Доставлено {sent_count}, Ошибок {failed_count}, Заблокировано {blocked_count}"
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
    elif query.data == 'donates':
        await show_donates(query, chat_id)
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
    elif query.data == 'show_yoomoney':
        await show_yoomoney_details(query, chat_id)
    elif query.data == 'show_merch':
        await show_merch_details(query, chat_id)
    elif query.data == 'show_boosty':
        await show_boosty_details(query, chat_id)
    elif query.data == 'about':
        await show_about(query)
    elif query.data == 'collaboration':
        await show_collaboration(query)
    elif query.data == 'back_to_menu':
        await back_to_menu(query)
    elif query.data == 'ratings':
        await show_track_ratings(query)
    elif query.data == 'quiz_start':
        await start_quiz(query)
    elif query.data.startswith('play_track_'):
        track_id = query.data.replace('play_track_', '')
        await play_track(query, track_id, context)
    elif query.data.startswith('info_track_'):
        track_id = query.data.replace('info_track_', '')
        await show_track_info(query, track_id)
    elif query.data.startswith('like_track_'):
        track_id = query.data.replace('like_track_', '')
        await rate_track(query, track_id, 'like')
    elif query.data.startswith('dislike_track_'):
        track_id = query.data.replace('dislike_track_', '')
        await rate_track(query, track_id, 'dislike')
    elif query.data.startswith('quiz_answer_'):
        parts = query.data.split('_')
        question_num = int(parts[2])
        answer = int(parts[3])
        await check_quiz_answer(query, context, question_num, answer)

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
            InlineKeyboardButton("🌙 MIDNIGHT GLOW", callback_data='info_track_midnight_glow'),
            InlineKeyboardButton("❓ Узнать", callback_data='info_track_midnight_glow')
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Случайная мотивирующая цитата
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
        [
            InlineKeyboardButton("👍 Класс!", callback_data=f'like_track_{track_id}'),
            InlineKeyboardButton("👎 Не то", callback_data=f'dislike_track_{track_id}')
        ],
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

async def show_tickets(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("📅 Предстоящие события", callback_data='upcoming_events')],
        [InlineKeyboardButton("🎬 YouTube БЕСПЛАТНО", url=YOUTUBE_STREAM_URL)],
        [InlineKeyboardButton("🎵 TikTok Live БЕСПЛАТНО", url=TIKTOK_STREAM_URL)],
        [InlineKeyboardButton("💎 Boosty БЕСПЛАТНО", url=BOOSTY_DONATE_URL)],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "🎟️ **Билеты и события:**\n\n"
            "📺 **СМОТРИ ТРАНСЛЯЦИИ БЕСПЛАТНО!**\n\n"
            "🎬 **YouTube** - смотри прямые трансляции\n"
            "🎵 **TikTok Live** - следи за нашим TikTok\n"
            "💎 **Boosty** - эксклюзивный контент\n\n"
            "🔔 Нажми кнопку 'Предстоящие события' для полной информации!"
        ),
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
# ДОНАТЫ
# ====================================================================

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

# ====================================================================
# Поддержка / реквизиты
# ====================================================================

async def show_support(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("💳 Карта Т-Банк", callback_data='show_card')],
        [InlineKeyboardButton("💰 YooMoney", callback_data='show_yoomoney')],
        [InlineKeyboardButton("🎫 Купить мерч", callback_data='show_merch')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "💳 **Поддержите развитие RESPZONA!** 💳\n\n"
            "Ваша поддержка помогает нам:\n"
            "🎵 Создавать новые треки\n"
            "🎤 Организовывать концерты\n"
            "🎸 Улучшать качество звука\n"
            "📱 Развивать проект\n\n"
            "**Выбери способ поддержки:**\n"
            "💳 Карта Т-Банк\n"
            "💰 YooMoney (кошелек)\n"
            "🎫 Купить мерч\n\n"
            "Каждый рубль важен! Спасибо за поддержку! ❤️"
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

async def show_merch_details(query, chat_id) -> None:
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "🎫 **Официальный мерч RESPZONA:**\n\n"
            "🚀 **САЙТ В РАЗРАБОТКЕ** 🚀\n\n"
            "Скоро здесь появится магазин, где ты сможешь купить:\n\n"
            "👕 **Футболки** (все размеры) - ~500₽\n"
            "🧢 **Кепки** - ~400₽\n"
            "🏷️ **Стикеры** (10шт) - ~50₽\n"
            "🎵 **И другое!**\n\n"
            "💫 **Как это будет работать:**\n"
            "1️⃣ Жмешь кнопку «Купить»\n"
            "2️⃣ Выбираешь товар\n"
            "3️⃣ Оплачиваешь\n"
            "4️⃣ Получаешь посылку в свой город автоматически! 🚚\n\n"
            "🔔 **Следи за обновлениями!**\n"
            "Напиши @respzonachat чтобы узнать когда откроется магазин!"
        ),
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
        text=(
            "👥 **О RESPZONA:**\n\n"
            "RESPZONA — музыкальная группа из Уфы и Стерлитамака 🎶\n\n"
            "**Команда проекта:**\n"
            "⭐ **Aryx** — главный идеолог, социальные сети, превью, тексты, "
            "программирование и программные функции 💻\n"
            "⭐ **Nng** — социальные сети, превью, тексты, event-менеджер 📱\n"
            "🎸 **nRIS** — третья гитара, помощник проекта\n\n"
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

# ====================================================================
# СОТРУДНИЧЕСТВО
# ====================================================================

async def show_collaboration(query) -> None:
    keyboard = [
        [InlineKeyboardButton("📱 Написать Aryx", url=f"https://t.me/{COLLABORATION_CONTACT.replace('@', '')}")],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            "🤝 **СОТРУДНИЧЕСТВО С RESPZONA:**\n\n"
            "Ты хочешь сотрудничать с нами? Отлично! 🎵\n\n"
            "✨ **Мы открыты для:**\n"
            "🎨 Дизайнеров (обложки, визуалы, мерч)\n"
            "🎬 Видеографов (клипы, превью, обработка)\n"
            "🎤 Певцов и рэперов (фичеры, синглы)\n"
            "🎵 Продюсеров (создание биов, миксинг)\n"
            "📱 Маркетологов (SMM, реклама)\n"
            "💻 Программистов (сайты, боты, приложения)\n"
            "🎸 Музыкантов (гитара, бас, ударные)\n\n"
            "💬 **Как с нами связаться:**\n\n"
            f"📌 **Контакт для сотрудничества:** {COLLABORATION_CONTACT}\n\n"
            "💡 **Расскажи нам:**\n"
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

async def back_to_menu(query) -> None:
    keyboard = [
        [InlineKeyboardButton("🎵 Приложение Respzona", web_app=WebAppInfo(url=WEBAPP_URL))],
        [
            InlineKeyboardButton("🎵 Треки", callback_data='tracks'),
            InlineKeyboardButton("🎟️ Билеты", callback_data='tickets')
        ],
        [
            InlineKeyboardButton("💳 Донаты", callback_data='donates'),
            InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')
        ],
        [
            InlineKeyboardButton("👥 О нас", callback_data='about'),
            InlineKeyboardButton("🤝 Сотрудничество", callback_data='collaboration')
        ],
        [
            InlineKeyboardButton("🎯 Викторина", callback_data='quiz_start'),
            InlineKeyboardButton("🏆 Рейтинги", callback_data='ratings')
        ],
        [InlineKeyboardButton("📱 Telegram", url=TELEGRAM_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="🎶 **RESPZONA - главное меню** 🎶\n\nВыбери нужный пункт:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ====================================================================
# Обработка текста
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
                    "🎵 **НОВЫЙ ТРЕК ВЫПУЩЕН!** 🎵\n\n"
                    f"{'=' * 50}\n"
                    f"🎵 **{track['name']}**\n"
                    f"{'=' * 50}\n\n"
                    f"📅 **Дата релиза:** {track['date']}\n"
                    f"🎤 **Исполнители:** {track['artists']}\n"
                    f"🎸 **Жанр:** {track['genre']}\n\n"
                    "📝 **О треке:**\n"
                    f"{track['description']}\n\n"
                    "🎧 Слушай трек ниже 👇"
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
    logger.info("🚀 ЗАПУСК БОТА RESPZONA V2")
    logger.info(f"📊 Загружено {len(users_data)} пользователей")
    logger.info("=" * 50)

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast_handler))

    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("🎵 БОТ ГОТОВ К РАБОТЕ!")
    logger.info("=" * 50)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
