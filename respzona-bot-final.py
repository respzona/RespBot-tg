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
referrals_data = load_json_file(REFERRALS_FILE)
lottery_data = load_json_file(LOTTERY_FILE)
polls_data = load_json_file(POLLS_FILE)
scheduled_data = load_json_file(SCHEDULED_FILE)

# ====================================================================
# РЕФЕРАЛЬНАЯ СИСТЕМА 🔗
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
        [InlineKeyboardButton("📋 Скопировать ссылку", callback_data='copy_referral_link')],
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
    else:
        # Просто добавляем нового пользователя если его нет
        if chat_id_str not in users_data:
            users_data[chat_id_str] = {
                'user_id': user.id,
                'username': user.username or 'unknown',
                'first_name': user.first_name,
                'notifications_enabled': True,
                'join_date': datetime.now().isoformat(),
                'referral_count': 0
            }
            save_json_file(USERS_FILE, users_data)
    
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
        f"🔗 Приглашать друзей и получать награды\n"
        f"📱 Следить за нами в социальных сетях\n\n"
        f"Выбери нужный пункт меню ниже!",
        reply_markup=reply_markup
    )

# ====================================================================
# ЛОТЕРЕЯ ДЛЯ ДОНАТОРОВ 🎰
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
# ОПРОСЫ И ГОЛОСОВАНИЕ 📊
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
# СИСТЕМА ОБЪЯВЛЕНИЙ (ТОЛЬКО АДМИН) 📢
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

# ====================================================================
# ОСНОВНЫЕ ФУНКЦИИ
# ====================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_referral_start(update, context)

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

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    try:
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
        elif query.data == 'show_card':
            await show_card_details(query, chat_id)
        elif query.data == 'show_yoomoney':
            await show_yoomoney_details(query, chat_id)
        elif query.data == 'show_boosty':
            await show_boosty_details(query, chat_id)
        elif query.data == 'about':
            await show_about(query)
        elif query.data == 'collaboration':
            await show_collaboration(query)
        elif query.data == 'back_to_menu':
            await back_to_menu(query)
        elif query.data.startswith('play_track_'):
            track_id = query.data.replace('play_track_', '')
            await play_track(query, track_id, context)
        elif query.data.startswith('info_track_'):
            track_id = query.data.replace('info_track_', '')
            await show_track_info(query, track_id)
        
        # Реферальная система
        elif query.data == 'referral_menu':
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
    
    except Exception as e:
        logger.error(f"❌ Ошибка в button_callback: {e}", exc_info=True)
        await query.answer(f"❌ Произошла ошибка: {str(e)}", show_alert=True)

def main() -> None:
    logger.info("=" * 60)
    logger.info("🚀 ЗАПУСК БОТА RESPZONA V4 (ИСПРАВЛЕННАЯ ВЕРСИЯ)")
    logger.info(f"📊 Загружено {len(users_data)} пользователей")
    logger.info("=" * 60)

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("announce", announce_handler))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: None))

    logger.info("🎵 БОТ RESPZONA V4 ГОТОВ К РАБОТЕ!")
    logger.info("=" * 60)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
