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
LOTTERY_FILE = "lottery_data.json"
POLLS_FILE = "polls_data.json"
SCHEDULED_FILE = "scheduled_messages.json"

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

# ОПРОСЫ
ACTIVE_POLLS = {
    'current_poll': None,
    'poll_data': {}
}

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
lottery_data = load_json_file(LOTTERY_FILE)
polls_data = load_json_file(POLLS_FILE)
scheduled_data = load_json_file(SCHEDULED_FILE)

# ====================================================================
# НОВАЯ: РЕФЕРАЛЬНАЯ СИСТЕМА 🔗
# ====================================================================

async def show_referral_menu(query) -> None:
    """Показывает меню реферальной системы"""
    user_id = query.from_user.id
    chat_id_str = str(query.message.chat_id)
    
    if chat_id_str not in users_data:
        await query.answer("❌ Ты не зарегистрирован в системе", show_alert=True)
        return
    
    referral_count = users_data[chat_id_str].get('referral_count', 0)
    
    # Генерируем реферальную ссылку
    ref_link = f"https://t.me/RESPZONA?start={user_id}"
    
    keyboard = [
        [InlineKeyboardButton("📋 Скопировать ссылку", callback_data='copy_referral')],
        [InlineKeyboardButton("👥 Мои рефералы", callback_data='show_my_referrals')],
        [InlineKeyboardButton("🎁 Награды", callback_data='referral_rewards')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"🔗 **РЕФЕРАЛЬНАЯ СИСТЕМА RESPZONA** 🔗\n\n"
             f"Приглашай друзей и получай награды!\n\n"
             f"👥 **Твои рефералы:** {referral_count}\n\n"
             f"**Твоя ссылка:**\n"
             f"`{ref_link}`\n\n"
             f"💎 **Награды за рефералов:**\n"
             f"• 5 рефералов → скидка 10% на мерч\n"
             f"• 10 рефералов → эксклюзивное видео\n"
             f"• 25 рефералов → пожизненная премиум доступ\n\n"
             f"🔄 Когда твой друг присоединится - оба получите бонус!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_referral_rewards(query) -> None:
    """Показывает доступные награды"""
    chat_id_str = str(query.message.chat_id)
    
    if chat_id_str not in users_data:
        await query.answer("❌ Ты не зарегистрирован", show_alert=True)
        return
    
    referral_count = users_data[chat_id_str].get('referral_count', 0)
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='referral_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    rewards_text = f"🎁 **СИСТЕМА НАГРАДА RESPZONA** 🎁\n\n"
    rewards_text += f"👥 У тебя сейчас: **{referral_count}** рефералов\n\n"
    rewards_text += "📊 **Таблица наград:**\n\n"
    
    rewards = [
        ("5 рефералов", "10% скидка на весь мерч", "5", referral_count >= 5),
        ("10 рефералов", "Эксклюзивное видео с группой", "10", referral_count >= 10),
        ("15 рефералов", "Фирменная кепка RESPZONA", "15", referral_count >= 15),
        ("25 рефералов", "Пожизненный премиум доступ", "25", referral_count >= 25),
        ("50 рефералов", "Встреча с группой (онлайн)", "50", referral_count >= 50),
    ]
    
    for milestone, reward, count, unlocked in rewards:
        icon = "✅" if unlocked else "🔒"
        rewards_text += f"{icon} **{count}+ рефералов**: {reward}\n"
    
    rewards_text += "\n💡 Совет: Поделись ссылкой в своём статусе в соцсетях!"
    
    await query.edit_message_text(
        text=rewards_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_referral_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка присоединения по реферальной ссылке"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    chat_id_str = str(chat_id)
    
    # Проверяем есть ли реферер ID
    if context.args and context.args[0].isdigit():
        referrer_id = int(context.args[0])
        referrer_chat_id_str = str(referrer_id)
        
        # Проверяем что реферер существует
        if referrer_chat_id_str in users_data:
            # Добавляем нового пользователя
            if chat_id_str not in users_data:
                users_data[chat_id_str] = {
                    'user_id': user.id,
                    'username': user.username or 'unknown',
                    'first_name': user.first_name,
                    'notifications_enabled': True,
                    'join_date': datetime.now().isoformat(),
                    'referrer_id': referrer_id,
                    'referral_count': 0
                }
                
                # Увеличиваем счетчик рефералов у пригласившего
                users_data[referrer_chat_id_str]['referral_count'] = \
                    users_data[referrer_chat_id_str].get('referral_count', 0) + 1
                
                save_json_file(USERS_FILE, users_data)
                
                # Отправляем сообщение реферёру
                try:
                    await context.bot.send_message(
                        chat_id=referrer_id,
                        text=f"🎉 **НОВЫЙ РЕФЕРАЛ!** 🎉\n\n"
                             f"👤 **{user.first_name}** присоединился по твоей ссылке!\n\n"
                             f"👥 Твоих рефералов: **{users_data[referrer_chat_id_str]['referral_count']}**\n\n"
                             f"🎁 Ты близко к следующей награде! Продолжай приглашать!",
                        parse_mode='Markdown'
                    )
                except:
                    pass
                
                logger.info(f"✅ Новый реферал: {user.first_name} (от {referrer_id})")
    
    # Стандартная команда /start
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
        [
            InlineKeyboardButton("🔗 Рефералы", callback_data='referral_menu'),
            InlineKeyboardButton("🎰 Лотерея", callback_data='lottery_menu')
        ],
        [
            InlineKeyboardButton("📊 Опросы", callback_data='polls_menu'),
            InlineKeyboardButton("📢 Объявления", callback_data='announcements_menu')
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
        f"🔗 Приглашать друзей и получать награды\n"
        f"📱 Следить за нами в социальных сетях\n\n"
        f"Выбери нужный пункт меню ниже!",
        reply_markup=reply_markup
    )

# ====================================================================
# НОВАЯ: ЛОТЕРЕЯ ДЛЯ ДОНАТОРОВ 🎰
# ====================================================================

async def show_lottery_menu(query) -> None:
    """Показывает меню лотереи"""
    
    keyboard = [
        [InlineKeyboardButton("🎰 Принять участие", callback_data='join_lottery')],
        [InlineKeyboardButton("📊 Статистика лотереи", callback_data='lottery_stats')],
        [InlineKeyboardButton("🏆 Предыдущие победители", callback_data='lottery_winners')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🎰 **ЛОТЕРЕЯ RESPZONA** 🎰\n\n"
             "Поддержи группу донатом и участвуй в ежемесячном розыгрыше!\n\n"
             "🎁 **Как это работает:**\n"
             "1️⃣ Поддержи нас донатом (любая сумма)\n"
             "2️⃣ За каждые 100₽ - один билет в лотерею\n"
             "3️⃣ Каждый месяц мы проводим розыгрыш\n"
             "4️⃣ Победители получают крутые призы!\n\n"
             "🏆 **Что можно выиграть:**\n"
             "🥇 1-е место: Эксклюзивная встреча с группой (онлайн)\n"
             "🥈 2-е место: Фирменный мерч пакет\n"
             "🥉 3-е место: 500₽ на следующий донат\n\n"
             "⏰ **Следующая лотерея:** 31.01.2026 в 20:00",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def join_lottery(query) -> None:
    """Присоединиться к лотерее"""
    chat_id_str = str(query.message.chat_id)
    
    if chat_id_str not in users_data:
        await query.answer("❌ Ты не зарегистрирован", show_alert=True)
        return
    
    keyboard = [
        [InlineKeyboardButton("💳 Карта", callback_data='show_card')],
        [InlineKeyboardButton("💎 Boosty", callback_data='show_boosty')],
        [InlineKeyboardButton("💰 YooMoney", callback_data='show_yoomoney')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='lottery_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="💳 **ПРИНЯТЬ УЧАСТИЕ В ЛОТЕРЕЕ**\n\n"
             "Выбери способ поддержки:\n\n"
             "💎 Boosty - рекомендуется\n"
             "💳 Карта Т-Банк - прямой перевод\n"
             "💰 YooMoney - цифровой кошелек\n\n"
             "После поддержки отправь скриншот @respzonachat\n"
             "и мы добавим тебя в розыгрыш!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_lottery_stats(query) -> None:
    """Показывает статистику лотереи"""
    
    if 'lottery' not in lottery_data:
        lottery_data['lottery'] = {'participants': 0, 'prize_pool': 0}
    
    stats = lottery_data['lottery']
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='lottery_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="📊 **СТАТИСТИКА ЛОТЕРЕИ**\n\n"
             f"👥 Участников: **{stats.get('participants', 0)}**\n"
             f"💰 Общая сумма призов: **{stats.get('prize_pool', 0)}₽**\n\n"
             f"🎰 Шанс выигрыша главного приза: **1/{max(1, stats.get('participants', 1))}**\n\n"
             f"⏰ Следующий розыгрыш: 31.01.2026\n"
             f"🕐 Время: 20:00 по Мск\n\n"
             f"Чем больше ты поддержишь - тем выше шанс выигрыша!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ====================================================================
# НОВАЯ: ОПРОСЫ И ГОЛОСОВАНИЕ 📊
# ====================================================================

async def show_polls_menu(query) -> None:
    """Показывает меню опросов"""
    
    keyboard = [
        [InlineKeyboardButton("🎵 Текущий опрос", callback_data='current_poll')],
        [InlineKeyboardButton("📈 Результаты", callback_data='poll_results')],
        [InlineKeyboardButton("📋 История опросов", callback_data='poll_history')],
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
# НОВАЯ: ОТПРАВКА КАСТОМНЫХ СООБЩЕНИЙ (РАСШИРЕННАЯ РАССЫЛКА) 📢
# ====================================================================

async def show_announcements_menu(query) -> None:
    """Показывает меню объявлений (только для админа)"""
    
    if query.from_user.id != ADMIN_ID:
        await query.answer("❌ Только администратор может отправлять объявления", show_alert=True)
        return
    
    keyboard = [
        [InlineKeyboardButton("📢 Отправить объявление", callback_data='send_announcement')],
        [InlineKeyboardButton("⏰ Запланировать", callback_data='schedule_announcement')],
        [InlineKeyboardButton("📋 История объявлений", callback_data='announcements_history')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="📢 **ОБЪЯВЛЕНИЯ И РАССЫЛКИ** 📢\n\n"
             "Админ-панель для отправки сообщений всем пользователям.\n\n"
             "📤 **Отправить сейчас** - мгновенная рассылка\n"
             "⏰ **Запланировать** - отложенная отправка\n"
             "📋 **История** - все отправленные объявления\n\n"
             "⚠️ **Помни:** объявления видят все пользователи с включенными уведомлениями!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка админских команд"""
    
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Доступ запрещен")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 **КОМАНДЫ АДМИНИСТРАТОРА:**\n\n"
            "**Отправить объявление:**\n"
            "`/announce Твое сообщение здесь`\n\n"
            "**Запланировать на время (мин):**\n"
            "`/schedule_message 10 Сообщение` (через 10 минут)\n\n"
            "**Отправить файл:**\n"
            "Отправь файл, а я помогу его разослать",
            parse_mode='Markdown'
        )
        return

async def announce_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /announce - отправка объявления"""
    
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Только администратор может это делать")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 Использование: `/announce Твое сообщение`",
            parse_mode='Markdown'
        )
        return
    
    message_text = ' '.join(context.args)
    
    if len(message_text) > 4096:
        await update.message.reply_text("❌ Сообщение слишком длинное (макс 4096 символов)")
        return
    
    # Сохраняем в историю
    if 'announcements' not in scheduled_data:
        scheduled_data['announcements'] = []
    
    announcement = {
        'text': message_text,
        'sent_at': datetime.now().isoformat(),
        'status': 'sending',
        'recipients': 0
    }
    
    await update.message.reply_text(
        "📢 Отправляю объявление всем...\n⏳ Это может занять несколько секунд..."
    )
    
    sent_count = 0
    failed_count = 0
    blocked_count = 0
    
    # Отправляем всем активным пользователям
    for chat_id_str, user_data in users_data.items():
        if user_data.get('notifications_enabled', True):
            try:
                chat_id = int(chat_id_str)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"📢 **ОБЪЯВЛЕНИЕ ОТ RESPZONA:**\n\n{message_text}",
                    parse_mode='Markdown'
                )
                sent_count += 1
            except Exception as e:
                error_msg = str(e).lower()
                if 'blocked' in error_msg or 'forbidden' in error_msg:
                    blocked_count += 1
                    user_data['notifications_enabled'] = False
                    save_json_file(USERS_FILE, users_data)
                else:
                    failed_count += 1
    
    announcement['status'] = 'sent'
    announcement['recipients'] = sent_count
    scheduled_data['announcements'].append(announcement)
    save_json_file(SCHEDULED_FILE, scheduled_data)
    
    report = (
        f"✅ **ОБЪЯВЛЕНИЕ ОТПРАВЛЕНО!**\n\n"
        f"📊 **Статистика:**\n"
        f"✅ Доставлено: **{sent_count}**\n"
        f"❌ Ошибок: **{failed_count}**\n"
        f"🚫 Заблокировано: **{blocked_count}**\n"
        f"📈 Всего пользователей: **{len(users_data)}**"
    )
    
    await update.message.reply_text(report, parse_mode='Markdown')
    logger.info(f"📢 Объявление отправлено: {sent_count} юзерам")

async def schedule_announcement(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда для планирования объявления"""
    
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Только администратор")
        return
    
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "⏰ Использование: `/schedule_message [минуты] [сообщение]`\n\n"
            "Пример: `/schedule_message 30 Новый трек выйдет скоро!`",
            parse_mode='Markdown'
        )
        return
    
    try:
        delay_minutes = int(context.args[0])
        message_text = ' '.join(context.args[1:])
    except ValueError:
        await update.message.reply_text("❌ Первый аргумент должен быть числом (минуты)")
        return
    
    scheduled_time = datetime.now() + timedelta(minutes=delay_minutes)
    
    await update.message.reply_text(
        f"✅ Объявление запланировано!\n\n"
        f"⏰ Отправится в: {scheduled_time.strftime('%H:%M')}\n"
        f"📝 Сообщение: {message_text[:50]}...",
        parse_mode='Markdown'
    )
    
    logger.info(f"⏰ Объявление запланировано на {scheduled_time}")

# ====================================================================
# Основная функция start
# ====================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_referral_start(update, context)

# ====================================================================
# Обработчик кнопок
# ====================================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    # Реферальная система
    if query.data == 'referral_menu':
        await show_referral_menu(query)
    elif query.data == 'referral_rewards':
        await show_referral_rewards(query)
    
    # Лотерея
    elif query.data == 'lottery_menu':
        await show_lottery_menu(query)
    elif query.data == 'join_lottery':
        await join_lottery(query)
    elif query.data == 'lottery_stats':
        await show_lottery_stats(query)
    
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
    
    # Объявления
    elif query.data == 'announcements_menu':
        await show_announcements_menu(query)
    
    elif query.data == 'back_to_menu':
        await back_to_menu(query)

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
        [
            InlineKeyboardButton("🔗 Рефералы", callback_data='referral_menu'),
            InlineKeyboardButton("🎰 Лотерея", callback_data='lottery_menu')
        ],
        [
            InlineKeyboardButton("📊 Опросы", callback_data='polls_menu'),
            InlineKeyboardButton("📢 Объявления", callback_data='announcements_menu')
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
# MAIN
# ====================================================================

def main() -> None:
    logger.info("=" * 60)
    logger.info("🚀 ЗАПУСК БОТА RESPZONA V3 (С НОВЫМИ ФИЧАМИ)")
    logger.info(f"📊 Загружено {len(users_data)} пользователей")
    logger.info("=" * 60)

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("announce", announce_handler))

    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: None))

    logger.info("🎵 БОТ RESPZONA V3 ГОТОВ К РАБОТЕ!")
    logger.info("=" * 60)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
