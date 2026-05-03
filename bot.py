from datetime import datetime, timedelta
import asyncio
import random
import hashlib
import time
import sqlite3
import threading
import json
from datetime import datetime, timedelta
import traceback
import sys
from io import StringIO

from aiogram import BaseMiddleware
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

import logging
import traceback
from datetime import datetime

import traceback
import sys
from io import StringIO

# Настройка логирования в файл
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'bot_debug_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Функция для логирования callback'ов
def log_callback(call: CallbackQuery, status: str, extra: str = ""):
    logger.info(f"[CALLBACK] {status} | user={call.from_user.id} | data={call.data[:100]} | {extra}")

# Настройка логирования в файл
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'bot_debug_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
        logging.StreamHandler()  # вывод в консоль
    ]
)
logger = logging.getLogger(__name__)

# Функция для логирования callback'ов
def log_callback(call: CallbackQuery, status: str, extra: str = ""):
    logger.info(f"[CALLBACK] {status} | user={call.from_user.id} | data={call.data[:100]} | {extra}")

# ===== ФИКС РЕКУРСИВНОГО КУРСОРА =====
import threading
_db_lock = threading.Lock()

def safe_execute(query, params=(), commit=False):
    """Безопасное выполнение запроса с блокировкой"""
    with _db_lock:
        cur = sql.execute(query, params)
        if commit:
            db.commit()
        return cur

def safe_fetchone(query, params=()):
    """Безопасное получение одной записи"""
    with _db_lock:
        sql.execute(query, params)
        return sql.fetchone()

def safe_fetchall(query, params=()):
    """Безопасное получение всех записей"""
    with _db_lock:
        sql.execute(query, params)
        return sql.fetchall()

# ВСЕ вызовы sql.execute замени на safe_execute
# ВСЕ вызовы fetchone() замени на safe_fetchon

# ================== НАСТРОЙКИ ==================
TOKEN = "8643904191:AAG8MVCcoL1dp0X04Cq3zkVIa5DtnTf8tOc"
HUNT_COOLDOWN = 180  # 3 минуты
EXP_PER_LEVEL = 500
ADMIN_ID = 6924481166  # Ваш ID
ADMIN_USERNAME = "DeepSleep01"  # Ваш username

# ================== НАСТРОЙКИ ИВЕНТА ==================
EVENT_ACTIVE = True   # <---- ВКЛ/ВЫКЛ ИВЕНТА (True - включен, False - выключен)

# ДАННЫЕ ТЕКУЩЕГО ИВЕНТА (меняй здесь для нового ивента)
EVENT_ID = "easter_2026"
EVENT_NAME = "🐣 Пасха 2026"
EVENT_LOCATION = "🐣 Пасхальная поляна"
EVENT_LOCATION_LEVEL = 25
EVENT_CURRENCY = "🥚 Пасхальное яйцо"
EVENT_ITEM_NAME = "🥚 Золотое яйцо удачи"

# ================== СИСТЕМА ПОГОДЫ ==================
WEATHER_TYPES = ["☀️ Солнечно", "☁️ Облачно", "🌧️ Дождь", "⛈️ Гроза", "🌫️ Туманно", "💨 Ветер"]
WEATHER_EFFECTS = {
    "☀️ Солнечно": {"search": 0, "hit": 10, "find_heavy": 0, "find_dangerous": 0},
    "☁️ Облачно": {"search": 0, "hit": 0, "find_heavy": 0, "find_dangerous": 0},
    "🌧️ Дождь": {"search": 0, "hit": -7, "find_heavy": 10, "find_dangerous": 0},
    "⛈️ Гроза": {"search": 0, "hit": -10, "find_heavy": 0, "find_dangerous": 15},
    "🌫️ Туманно": {"search": 0, "hit": -10, "find_heavy": 0, "find_dangerous": 0},  # особый эффект
    "💨 Ветер": {"search": 20, "hit": 0, "find_heavy": 0, "find_dangerous": 0}
}

# ================== МУТАЦИИ ==================
MUTATIONS = {
    "🔥Гигант": {"chance": 20, "coins_mult": 1.5, "exp_mult": 1.0},
    "🤍Альбинос": {"chance": 10, "coins_mult": 1.0, "exp_mult": 7.0},
    "👑Вожак": {"chance": 4, "coins_mult": 3.0, "exp_mult": 12.0}
}
# Обычный (шанс ..%) обрабатывается отдельно, без множителей

current_weather = random.choice(WEATHER_TYPES)
last_weather_change = int(time.time())

# Животные ивента
EVENT_ANIMALS = {
    "Мелочь": ["Цыплёнок", "Пасх яйцо", "Кролик"],
    "Средн": ["Пасх заяц", "Ход кулич", "Лет свеча"],
    "Опасн": ["Волк крашенка", "Лиса корзинка", "Яйцо кабан"],
    "Тяжел": ["Медведь кулич", "Драконояйцо"],
    "Титан": ["Цыпа монстр"]
}

# Задания ивента
EVENT_QUESTS = [
    {"need": 1, "reward_coins": 500, "reward_exp": 0, "reward_item": None, "title_name": None},
    {"need": 5, "reward_coins": 1000, "reward_exp": 0, "reward_item": None, "title_name": None},
    {"need": 15, "reward_coins": 2000, "reward_exp": 1000, "reward_item": None, "title_name": None},
    {"need": 30, "reward_coins": 5000, "reward_exp": 0, "reward_item": "golden_bullet", "title_name": None},
    {"need": 55, "reward_coins": 7500, "reward_exp": 0, "reward_item": "diamond_bullet", "title_name": None},
    {"need": 100, "reward_coins": 15000, "reward_exp": 0, "reward_item": "drone", "title_name": None},
    {"need": 200, "reward_coins": 0, "reward_exp": 0, "reward_item": "title", "title_name": "🐇 Пасхальный кролик"}
]

# Текст для кнопки "Что это?"
EVENT_HELP_TEXT = f"""
📖 **ЧТО ТАКОЕ ИВЕНТ?**

🎯 Ивент "{EVENT_NAME}" — временное событие!

📍 **ВРЕМЕННАЯ ЛОКАЦИЯ:**
"{EVENT_LOCATION}" (доступна с {EVENT_LOCATION_LEVEL} уровня)

🥚 **КАК ПОЛУЧИТЬ {EVENT_CURRENCY}:**
• Убить Опасн/Тяжел/Титан в любой локации → +3 🥚
• Убить любое животное на ивентовой локации → +3 🥚
• Убить титана на ивентовой локации → +5 🥚
• Купить в магазине ивента (1 🥚 = 500 монет)

📋 **ЗАДАНИЯ:**
Выполняй задания последовательно, награды выдаются автоматически!

1. 1 яйцо → 500 монет
2. 5 яиц → 1000 монет
3. 15 яиц → 2000 монет + 1000 опыта
4. 30 яиц → 5000 монет + Золотая пуля
5. 55 яиц → 7500 монет + Алмазная пуля
6. 100 яиц → 15000 монет + Дрон
7. 200 яиц → Титул "🐇 Пасхальный кролик"

🛒 **МАГАЗИН ИВЕНТА** (покупка за яйца):
• 5000 монет — 10 🥚
• Золотая пуля — 3 🥚
• Алмазная пуля — 7 🥚
• Аптечка — 1 🥚
• Титул "🐣 Цыпленок" — 50 🥚
• {EVENT_ITEM_NAME} — 100 🥚

🥚 **{EVENT_ITEM_NAME}:**
Снаряжение (как рюкзак). Пока надето — каждые 24 часа даёт 500 монет!

⏰ Ивент активен до отключения администратором.
"""


# ================== ДАННЫЕ ==================
LOCATIONS = {
    "Тайга": {"level": 0, "animals": {
        "Мелочь": ["Заяц", "Белка", "Бурундук", "Рябчик", "Выдра", "Ласка", "Горностай", "Соболь", "Барсук", "Землеройка"],
        "Средн": ["Бобр", "Глухарь", "Северный олень", "Косуля", "Лиса", "Енот", "Уж" ],
        "Опасн": ["Кабан", "Рысь", "Росомаха", "Серый волк", "Бурый медведь", "Гадюка", "Гризли", "Баран"],
        "Тяжел": ["Лось", "Зубр", "Амурский Тигр"],
        "Титан": ["Оборотень", "Вендиго", "Василиск"]
    }},
    "Саванна": {"level": 10, "animals": {
        "Мелочь": ["Дикобраз", "Мангуст", "Сурикат", "Антилоповый заяц", "Суслик", "Даман", "Песчанка", "Геккон", "Шипохвост", "Хамеллеон"],
        "Средн": ["Зебра", "Шакал", "Антилопа Гну", "Антилопа Импала", "Страус", "Бородавочник", "Сервал"],
        "Опасн": ["Гиена", "Пума", "Лев", "Леопард", "Гепард", "Мамба"],
        "Тяжел": ["Жираф", "Буйвол", "Африканский Слон", "Бегемот"],
        "Титан": ["Гротсланг", "Кикияон", "Нанди"]
    }},
    "Арктика": {"level": 25, "animals": {
        "Мелочь": ["Лемминг", "Песец", "Арктикческий заяц", "Пуночка", "Гага", "Сибирская Полёвка", "Куропатка"],
        "Средн": ["Полярная сова", "Тюлень", "Карибу", "Лахтак"],
        "Опасн": ["Снежный барс", "Белый медведь", "Морской леопард"],
        "Тяжел": ["Морж", "Белуха", "Овцебык", "Косатка", "Морской слон"],
        "Титан": ["Мамонт", "Йети", "Ледяной дракон"]
    }},
    "Джунгли": {"level": 50, "animals": {
        "Мелочь": ["Капибара", "Ленивец", "Долгопят", "Тукан", "Мара", "Агути"],
        "Средн": ["Окапи", "Обезьяна", "Казуар", "Тапир", "Броненосец", "Ревун"],
        "Опасн": ["Комодский варан", "Крокодил", "Анаконда", "Ягуар", "Горилла", "Тигр", "Пантера"],
        "Тяжел": ["Носорог", "Лесной Слон", "Гаур"],
        "Титан": ["Чупакабра", "Бойтата", "Якумама"]
    }},
    "Горы": {"level": 80, "animals": {
        "Мелочь": ["Воробей", "Кедровка", "Голубь", "Синица", "Королёк", "Крапивник", "Чиж", "Зяблик", "Зарянка"],
        "Средн": ["Кеклик", "Улар", "Куропатка", "Дятел", "Тетерев", "Фазан", "Сойка"],
        "Опасн": ["Сапсан", "Беркут", "Ястреб", "Бородач"],
        "Тяжел": ["Черный гриф", "Кондор", "Пеликан"],
        "Титан": ["Орел", "Птица Рух", "Зиз"]
    }}, 
    "Древний мир": {"level": 140, "animals": {
        "Мелочь": ["Компсогнат", "Иберомезорнис", "Археоптерикс", "Гаттерия", "Харамия", "Шуотерий", "Докодон", "Кюнеотерий", "Тринаксодон"],
        "Средн": ["Велоцираптор", "Динопитек", "Дейноних", "Троодон", "Целур", "Репеномам", "Эритрозух"],
        "Опасн": ["Смилодон", "Энтелодонт", "Келенкен", "Гиенодон"],
        "Тяжел": ["Трицератопс", "Стегозавр", "Гадрозавр", "Эласмотерий", "Мегалания", "Шерстистый носорог"],
        "Титан": ["Тираннозавр", "Брахиозавр", "Птеродактиль", "Годзилла"]
    }},
    "Подводный мир": {"level": 245, "animals": {
        "Мелочь": ["Рыба-светляк", "Краб", "Рыба-клоун", "Медуза", "Анчоус", "Офиура", "Кальмар", "Рыба-Капля"],
        "Средн": ["Электрический скат", "Осьминог", "Химера", "Рыба-фугу"],
        "Опасн": ["Удильщик", "Мурена", "Барракуда", "Крылатка", "Пиранья"],
        "Тяжел": ["Манта", "Кашалот", "Акула", "Кит"],
        "Титан": ["Мегалодон", "Кракен", "Левиафан", "Геликоприон"]
    }},
    "Болото проклятых": {"level": 400, "animals": {
        "Мелочь": ["Болотный огонёк", "Тиняк", "Водяной паук", "Пиявка", "Грязевой червь", "Болотная светлячка", "Трясинник"],
        "Средн": ["Топь", "Болотник", "Водяной", "Зыбун", "Корень-душитель", "Болотный уж", "Утопленник"],
        "Опасн": ["Болотный полоз", "Ведьма-трясина", "Трясинный волк", "Мокрый упырь", "Когтистая трясина"],
        "Тяжел": ["Болотный тролль", "Грязевой голем", "Леший", "Гигантская жаба"],
        "Титан": ["Мать трясин", "Болотный царь", "Дух болота"]
    }},
    "Призрачный лес": {"level": 700, "animals": {
        "Мелочь": ["Призрачный заяц", "Светляк", "Плакальщица", "Иглолап"],
        "Средн": ["Вервольф", "Теневой Ворон", "Скелет", "Гарпия"],
        "Опасн": ["Призрак", "Упырь", "Вампир", "Лорд Тумана", "Проклятый рыцарь"],
        "Тяжел": ["Энт", "Мантикора", "Минотавр", "Горгулья"],
        "Титан": ["Владыка леса", "Всадник", "Великий лич", "Черный Дракон"]
    }},
    "Рад-зона": {"level": 1300, "animals": {
        "Мелочь": ["Радиационная крыса", "Клещ", "Изотоп", "Спорик"],
        "Средн": ["Гуль", "Дикий пес", "Снор"],
        "Опасн": ["Химера","Излом", "Радиационный волк"],
        "Тяжел": ["Гигант", "Мутант", "Зверобой"],
        "Титан": ["Сталкер", "Кровосос"]
    }},
    "Грозовая бездна": {"level": 2000, "animals": {
        "Мелочь": ["Искра", "Разряд", "Плазменный сгусток", "Молниевая капля", "Статический блик", "Сверкающий осколок"],
        "Средн": ["Плазменный скат", "Молниевый змей", "Разрядный дух", "Громовой сгусток", "Электрический элементаль"],
        "Опасн": ["Грозовой страж", "Плазменный хищник", "Штормовой дух", "Электрический виверн"],
        "Тяжел": ["Грозовой дракон", "Молниевый гигант", "Плазменный левиафан", "Штормовой голем"],
        "Титан": ["Повелитель молний", "Буревой бог", "Разрушитель небес"]
    }},
     "Киберпанк": {"level": 3000, "animals": {
        "Мелочь": ["Микродрон", "Механическая крыса", "Бот-шпион", "Электро-скат", "Скан-бот", "Кибер-чип"],
        "Средн": ["Кибер-пес", "Бот-уборщик", "Андроид", "Голограмма", "Техно-краб"],
        "Опасн": ["Турель", "Киборг", "Терминатор", "Лазерный волк", "Наемник"],
        "Тяжел": ["Боевой мех", "Дрон-штурм", "Броневик", "Паук-танк"],
        "Титан": ["ИИ", "Техно-дракон"]
    }},
    "Инферно": {"level": 4000, "animals": {
        "Мелочь": ["Искра", "Шлаковый паук", "Дымный дух", "Уголёк", "Маленький бес", "Опалённый скелет", "Вулканическая саламандра"],
        "Средн": ["Огненный змей", "Лавовый бес", "Пепельный голем", "Демон-клинок", "Жар-птица малая", "Пламенный волк", "Адский гончий"],
        "Опасн": ["Инфернальный страж", "Пожиратель углей", "Магматический элементаль", "Демон-копьеносец", "Пламенный виверн"],
        "Тяжел": ["Лавовый гигант", "Баларог", "Пожиратель душ", "Цербер"],
        "Титан": ["Повелитель пламени", "Адский дракон", "Ифрит-император"]
    }},
    "Космическая пустошь": {"level": 5000, "animals": {
        "Мелочь": ["Космокрыса", "Звёздная медуза", "Пылевой червь", "Вакуумный слизень"],
        "Средн": ["Космический скавенджер", "Радиоактивный шакал", "Звёздный мантикор"],
        "Опасн": ["Космодесантник-отступник", "Чёрный карлик", "Гравитационный хищник", "Пожиратель энергии"],
        "Тяжел": ["Звёздный левиафан", "Космический титан", "Чёрная Дыра", "Некро-колосс"],
        "Титан": ["Пожиратель галактик", "Космический дракон", "Властелин Пустоты"]
    }}


}   # <--- ЭТО ЗАКРЫВАЮЩАЯ СКОБКА СЛОВАРЯ LOCATIONS

# ===== ВРЕМЕННАЯ ЛОКАЦИЯ ИВЕНТА (ДОБАВЛЯЕТСЯ ПОСЛЕ LOCATIONS) =====
if EVENT_ACTIVE:
    LOCATIONS[EVENT_LOCATION] = {
        "level": EVENT_LOCATION_LEVEL,
        "animals": EVENT_ANIMALS
    }

SEARCH_CHANCES = {
    "Мелочь": 60,
    "Средн": 45,
    "Опасн": 20,
    "Тяжел": 5,
    "Титан": 1
}

REWARDS = {
    "Мелочь": (30, 50),
    "Средн": (140, 250),
    "Опасн": (600, 1000),
    "Тяжел": (4000, 3000),
    "Титан": (20000, 10000)
}

# ================== НОВАЯ СИСТЕМА ОРУЖИЯ ==================
# ГРУППЫ: обычные, огненные, ледяные, ядовитые, электрические, тёмные, священные

# ----- ОБЫЧНЫЕ (уровень 0-70) -----
WEAPONS_COMMON = {
    "Револьвер": {"damage": 25, "chances": [55,20,3,0.5,0.05], "level_req": 0, "group": "обычные", "ability": None, "ability_desc": None, "ability_chance": 0, "description": "Мой дед охотился с ним на медведей. Говорил, что лучше друга не найти", "obtain": {"type": "start", "price": 0}},
    "Дробовик": {"damage": 35, "chances": [65,40,8,1,0.3], "level_req": 5, "group": "обычные", "ability": None, "ability_desc": None, "ability_chance": 0, "description": "Один залп — и проблема исчезает. Особенно если проблема размером с кабана", "obtain": {"type": "shop", "price": 1500}},
    "Винтовка": {"damage": 30, "chances": [25,60,20,5,1], "level_req": 10, "group": "обычные", "ability": None, "ability_desc": None, "ability_chance": 0, "description": "Говорят, из неё воевали в лесах. Метка 1943 до сих пор видна", "obtain": {"type": "shop", "price": 6000}},
    "Карабин": {"damage": 35, "chances": [30,50,45,10,3], "level_req": 20, "group": "обычные", "ability": None, "ability_desc": None, "ability_chance": 0, "description": "Золотая середина. Не громкий, но и не тихий. Как любимые тапки — всегда под рукой", "obtain": {"type": "shop", "price": 18000}},
    "Штуцер": {"damage": 40, "chances": [15,35,65,30,7], "level_req": 35, "group": "обычные", "ability": None, "ability_desc": None, "ability_chance": 0, "description": "Любит, чтобы его хвалили. 'Какой же я точный, какой же я красивый'. После удачного выстрела звенит самодовольно", "obtain": {"type": "shop", "price": 45000}},
    "Слонобой": {"damage": 50, "chances": [10,20,40,65,18], "level_req": 50, "group": "обычные", "ability": None, "ability_desc": None, "ability_chance": 0, "description": "Медведи при виде него сами падают в обморок. Экономит патроны. Вежливые звери попались", "obtain": {"type": "shop", "price": 100000}},
    "Снайперка": {"damage": 45, "chances": [30,40,55,65,58], "level_req": 70, "group": "обычные", "ability": None, "ability_desc": None, "ability_chance": 0, "description": "В оптику иногда видно, как зверь смеётся. Странно, правда? А потом ты стреляешь, и смех затихает", "obtain": {"type": "shop", "price": 300000}},
}

# ----- ОГНЕННЫЕ (уровень 25+) -----
WEAPONS_FIRE = {
    "Огненный мушкет": {"damage": 40, "chances": [20,50,35,8,3], "level_req": 25, "group": "огненные", "ability": "burn", "ability_desc": "Поджигает: -8 HP/ход (3 хода)", "ability_chance": 50, "description": "Ствол нагревается так, что можно чай вскипятить. Зверям такой чай не нравится", "obtain": {"type": "shop", "price": 80000}},
    "Вулканический револьвер": {"damage": 35, "chances": [50,18,5,1,0.1], "level_req": 40, "group": "огненные", "ability": "lava_shot", "ability_desc": "Лавовый шар: x1.5 урона", "ability_chance": 50, "description": "Говорят, кузнец уронил его в лаву. А когда достал — оружие само дышало жаром", "obtain": {"type": "achievement", "requirement": "100 убийств в Тайге"}},
    "Пирокинетический карабин": {"damage": 45, "chances": [25,45,40,12,5], "level_req": 60, "group": "огненные", "ability": "ignite", "ability_desc": "Воспламенение: животное не атакует 1 ход", "ability_chance": 50, "description": "Мыслишь огнём? Оно стреляет огнём. Идеальное попадание", "obtain": {"type": "craft", "requirement": "скоро"}},
    "Дыхание дракона": {"damage": 55, "chances": [55,35,10,2,0.5], "level_req": 80, "group": "огненные", "ability": "fire_wave", "ability_desc": "Огненный вал: урон по всем частям", "ability_chance": 50, "description": "Один выдох — и лес позади тебя превращается в пепел. Драконы одобряют", "obtain": {"type": "case", "requirement": "редкий кейс (скоро)"}},
    "Магматический арбалет": {"damage": 50, "chances": [10,30,60,28,8], "level_req": 100, "group": "огненные", "ability": "eruption", "ability_desc": "Извержение: +15% урона до конца боя", "ability_chance": 50, "description": "Вместо тетивы — раскалённая магма. Больно, очень больно", "obtain": {"type": "shop", "price": 250000}},
    "Адский револьвер": {"damage": 42, "chances": [45,15,8,2,0.3], "level_req": 120, "group": "огненные", "ability": "inferno", "ability_desc": "Пекло: -15% защиты животного", "ability_chance": 50, "description": "Чёрт возьми, даже сам чёрт им не пользуется — боится обжечься", "obtain": {"type": "achievement", "requirement": "50 убийств в Инферно"}},
    "Феникс-винтовка": {"damage": 48, "chances": [25,35,50,60,52], "level_req": 150, "group": "огненные", "ability": "rebirth", "ability_desc": "Возрождение: 1 раз воскреснуть", "ability_chance": 50, "description": "Сгорает дотла после каждого выстрела. И возрождается. У неё больше жизней, чем у кота", "obtain": {"type": "craft", "requirement": "редкий крафт (скоро)"}},
}

# ----- ЛЕДЯНЫЕ (уровень 50+) -----
WEAPONS_ICE = {
    "Снежный револьвер": {"damage": 30, "chances": [50,20,5,1,0.1], "level_req": 50, "group": "ледяные", "ability": "snowstorm", "ability_desc": "Снежная буря: -20% попадания животного", "ability_chance": 50, "description": "Зимой стреляет сам. Летом — только если попросить вежливо", "obtain": {"type": "shop", "price": 60000}},
    "Ледяной пистолет": {"damage": 38, "chances": [60,38,10,2,0.3], "level_req": 65, "group": "ледяные", "ability": "freeze", "ability_desc": "Заморозка: животное не атакует 1 ход", "ability_chance": 50, "description": "Хранить в морозилке. Между пельменями и мороженым", "obtain": {"type": "achievement", "requirement": "100 убийств в Арктике"}},
    "Ледяная винтовка": {"damage": 40, "chances": [20,55,25,8,2], "level_req": 80, "group": "ледяные", "ability": "ice_shard", "ability_desc": "Сосулька: x1.5 урона при попадании", "ability_chance": 50, "description": "Ствол покрыт инеем. Даже в руках холодно. А уж зверям — тем более", "obtain": {"type": "craft", "requirement": "скоро"}},
    "Хладнокровный арбалет": {"damage": 45, "chances": [10,30,55,30,10], "level_req": 100, "group": "ледяные", "ability": "slow", "ability_desc": "Замедление: атака раз в 2 хода", "ability_chance": 50, "description": "Спокойствие, только спокойствие. Зверь просто засыпает на ходу", "obtain": {"type": "shop", "price": 200000}},
    "Морозный посох": {"damage": 35, "chances": [25,45,40,15,5], "level_req": 120, "group": "ледяные", "ability": "icicle", "ability_desc": "Ледяной кристалл: гарант крита по замороженному", "ability_chance": 50, "description": "Маг из отдела кадров зачаровал. Теперь это не посох, а морозилка", "obtain": {"type": "case", "requirement": "скоро"}},
    "Северный карабин": {"damage": 42, "chances": [28,48,42,14,6], "level_req": 150, "group": "ледяные", "ability": "iceberg", "ability_desc": "Айсберг: крит по замороженному", "ability_chance": 50, "description": "Северный ветер шепчет тебе на ухо: 'Стреляй, я прикрою'", "obtain": {"type": "achievement", "requirement": "50 убийств в Грозовой бездне"}},
    "Вечная мерзлота": {"damage": 50, "chances": [8,18,38,62,20], "level_req": 180, "group": "ледяные", "ability": "permafrost", "ability_desc": "Ледяная глыба: -20% брони животного", "ability_chance": 50, "description": "Говорят, время лечит. Это оружие — лечит время. Замораживает навсегда", "obtain": {"type": "craft", "requirement": "редкий крафт (скоро)"}},
}

# ----- ЯДОВИТЫЕ (уровень 100+) -----
WEAPONS_POISON = {
    "Отравленный дротик": {"damage": 25, "chances": [50,22,6,1,0.1], "level_req": 100, "group": "ядовитые", "ability": "strong_poison", "ability_desc": "Сильный яд: -20% попадания животного", "ability_chance": 50, "description": "Маленький, тихий, незаметный. Как обиженный коллега, который подсыпал яд в чай", "obtain": {"type": "shop", "price": 50000}},
    "Ядовитый револьвер": {"damage": 30, "chances": [48,18,5,1,0.1], "level_req": 120, "group": "ядовитые", "ability": "infection", "ability_desc": "Заражение: яд при побеге", "ability_chance": 50, "description": "После выстрела не стреляй больше — подожди, пока само сдохнет. Экономия патронов", "obtain": {"type": "achievement", "requirement": "100 убийств в Джунглях"}},
    "Змеиный клык": {"damage": 35, "chances": [22,58,22,6,1.5], "level_req": 140, "group": "ядовитые", "ability": "paralyze", "ability_desc": "Паралич: животное не двигается 2 хода", "ability_chance": 50, "description": "Змея кусает раз. А тут — каждый выстрел как укус. И яд тот же", "obtain": {"type": "craft", "requirement": "скоро"}},
    "Токсичный карабин": {"damage": 38, "chances": [28,48,43,14,6], "level_req": 160, "group": "ядовитые", "ability": "acid", "ability_desc": "Кислота: -25% брони", "ability_chance": 50, "description": "Если кислота не разъедает — значит, это не кислота. А это кислота", "obtain": {"type": "shop", "price": 180000}},
    "Некротический арбалет": {"damage": 40, "chances": [12,32,58,28,9], "level_req": 180, "group": "ядовитые", "ability": "decay", "ability_desc": "Гниение: -12 HP/ход (3 хода)", "ability_chance": 50, "description": "Мёртвые не кусаются. Они просто гниют. И твой враг — не исключение", "obtain": {"type": "case", "requirement": "редкий кейс (скоро)"}},
    "Скорпион-пистолет": {"damage": 45, "chances": [58,35,12,3,0.5], "level_req": 200, "group": "ядовитые", "ability": "death_poison", "ability_desc": "Смертельный яд: умрёт через 2 хода", "ability_chance": 50, "description": "Один укус — и ты труп. Просто пока не знаешь об этом", "obtain": {"type": "achievement", "requirement": "30 убийств титанов"}},
    "Бактериальная винтовка": {"damage": 42, "chances": [28,38,48,58,50], "level_req": 220, "group": "ядовитые", "ability": "epidemic", "ability_desc": "Эпидемия: яд передаётся следующему", "ability_chance": 50, "description": "Чихать на зверей — буквально. Они подхватят заразу и разнесут дальше", "obtain": {"type": "craft", "requirement": "редкий крафт (скоро)"}},
}

# ----- ЭЛЕКТРИЧЕСКИЕ (уровень 200+) -----
WEAPONS_ELECTRIC = {
    "Электрошокер": {"damage": 35, "chances": [52,22,7,1,0.15], "level_req": 200, "group": "электрические", "ability": "paralyze_el", "ability_desc": "Паралич: пропуск хода", "ability_chance": 50, "description": "Ток останавливает сердце. У зверей — тоже", "obtain": {"type": "shop", "price": 120000}},
    "Разрядный пистолет": {"damage": 30, "chances": [62,40,12,2,0.25], "level_req": 220, "group": "электрические", "ability": "static_field", "ability_desc": "Статическое поле: -20% попадания животного", "ability_chance": 50, "description": "Волосы дыбом — это не от страха. Это от разряда", "obtain": {"type": "achievement", "requirement": "100 убийств в Подводном мире"}},
    "Громовой карабин": {"damage": 40, "chances": [28,48,44,15,7], "level_req": 240, "group": "электрические", "ability": "chain_lightning", "ability_desc": "Цепная молния: +15% урона соседнему", "ability_chance": 50, "description": "Гром среди ясного неба. И молния — туда же", "obtain": {"type": "craft", "requirement": "скоро"}},
    "Молниевый арбалет": {"damage": 50, "chances": [12,32,58,30,11], "level_req": 260, "group": "электрические", "ability": "discharge", "ability_desc": "Разряд: нет защиты 2 хода", "ability_chance": 50, "description": "Заряжай! Бах! Молния! Красота!", "obtain": {"type": "shop", "price": 300000}},
    "Плазменная винтовка": {"damage": 45, "chances": [22,55,28,10,4], "level_req": 280, "group": "электрические", "ability": "charged_shot", "ability_desc": "Заряженный выстрел: x1.5 урона", "ability_chance": 50, "description": "Плазма не оставляет шансов. И улик — тоже", "obtain": {"type": "case", "requirement": "эпический кейс (скоро)"}},
    "Тесла-пушка": {"damage": 55, "chances": [8,18,38,62,22], "level_req": 300, "group": "электрические", "ability": "emp", "ability_desc": "ЭМИ: отключает способность", "ability_chance": 50, "description": "Никола Тесла бы гордился. Или ужаснулся. Непонятно", "obtain": {"type": "achievement", "requirement": "50 убийств в Рад-зоне"}},
    "Грозовой револьвер": {"damage": 38, "chances": [48,20,8,2,0.3], "level_req": 320, "group": "электрические", "ability": "thunder_strike", "ability_desc": "Удар молнии: гарант попадания", "ability_chance": 50, "description": "Боги грома одобряют. Они даже скинулись на покупку", "obtain": {"type": "craft", "requirement": "редкий крафт (скоро)"}},
}

# ----- ТЁМНЫЕ (уровень 350+) -----
WEAPONS_DARK = {
    "Теневой арбалет": {"damage": 45, "chances": [10,30,58,32,12], "level_req": 350, "group": "тёмные", "ability": "darkness", "ability_desc": "Тьма: -30% попадания животного", "ability_chance": 50, "description": "Стреляешь — и тень становится длиннее. И холоднее. И страшнее", "obtain": {"type": "shop", "price": 400000}},
    "Обсидиановый револьвер": {"damage": 38, "chances": [50,20,8,2,0.2], "level_req": 370, "group": "тёмные", "ability": "stone_skin", "ability_desc": "Каменная кожа: +30% защиты 3 хода", "ability_chance": 50, "description": "Чёрный, как душа коллектора. И такой же беспощадный", "obtain": {"type": "achievement", "requirement": "100 убийств в Призрачном лесу"}},
    "Кошмарный карабин": {"damage": 42, "chances": [25,45,42,15,7], "level_req": 390, "group": "тёмные", "ability": "fear", "ability_desc": "Страх: убегает с наградой", "ability_chance": 50, "description": "Зверю снится кошмар. Твой выстрел. И ты в главной роли", "obtain": {"type": "craft", "requirement": "скоро"}},
    "Душелов": {"damage": 35, "chances": [48,20,8,2,0.2], "level_req": 410, "group": "тёмные", "ability": "soul_steal", "ability_desc": "Кража души: +20% урона до конца", "ability_chance": 50, "description": "Ловит не только зверей. Иногда — и удачу за хвост", "obtain": {"type": "case", "requirement": "эпический кейс (скоро)"}},
    "Вампирский кинжал": {"damage": 40, "chances": [28,48,42,14,6], "level_req": 430, "group": "тёмные", "ability": "bloodletting", "ability_desc": "Кровопускание: 50% урона → в HP", "ability_chance": 50, "description": "Пьёт кровь. Буквально. Держи подальше от шеи", "obtain": {"type": "shop", "price": 350000}},
    "Некро-винтовка": {"damage": 50, "chances": [25,35,48,58,54], "level_req": 450, "group": "тёмные", "ability": "summon", "ability_desc": "Призыв: убитое животное помогает", "ability_chance": 50, "description": "Мёртвые не кусаются. Но стреляют — да", "obtain": {"type": "achievement", "requirement": "30 убийств титанов в Древнем мире"}},
    "Проклятый мушкет": {"damage": 55, "chances": [8,18,38,62,24], "level_req": 470, "group": "тёмные", "ability": "curse", "ability_desc": "Проклятие: x2 урона в след. ход", "ability_chance": 50, "description": "Ствол изогнут, приклад треснут. Но стреляет так, что предки в гробу переворачиваются", "obtain": {"type": "craft", "requirement": "редкий крафт (скоро)"}},
}

# ----- СВЯЩЕННЫЕ (уровень 500+) -----
WEAPONS_HOLY = {
    "Святой арбалет": {"damage": 45, "chances": [12,32,58,30,12], "level_req": 500, "group": "священные", "ability": "blessing", "ability_desc": "Благословение: +25% попадания до конца", "ability_chance": 50, "description": "Стрелы светятся. Попадают — туда же. Молитва прилагается", "obtain": {"type": "shop", "price": 500000}},
    "Ангельский револьвер": {"damage": 35, "chances": [52,22,8,2,0.2], "level_req": 520, "group": "священные", "ability": "heal", "ability_desc": "Исцеление: +30 HP игроку", "ability_chance": 50, "description": "Ангелы стреляют редко. Но метко. И лечат после", "obtain": {"type": "achievement", "requirement": "100 убийств в Инферно"}},
    "Паладин-пистолет": {"damage": 38, "chances": [60,38,12,3,0.4], "level_req": 540, "group": "священные", "ability": "faith_shield", "ability_desc": "Щит веры: нет урона 1 ход", "ability_chance": 50, "description": "Бог на твоей стороне. И в стволе — тоже", "obtain": {"type": "craft", "requirement": "скоро"}},
    "Небесный карабин": {"damage": 40, "chances": [28,48,44,16,8], "level_req": 560, "group": "священные", "ability": "light", "ability_desc": "Свет: снимает проклятия", "ability_chance": 50, "description": "Стреляет радугой. Звери умирают от счастья", "obtain": {"type": "case", "requirement": "легендарный кейс (скоро)"}},
    "Светлый посох": {"damage": 42, "chances": [22,55,28,10,4], "level_req": 580, "group": "священные", "ability": "purify", "ability_desc": "Очищение: снимает эффекты +20 HP", "ability_chance": 50, "description": "Магия света. Чистая, как слеза младенца. И такая же опасная", "obtain": {"type": "shop", "price": 450000}},
    "Божественная винтовка": {"damage": 48, "chances": [28,38,50,60,57], "level_req": 600, "group": "священные", "ability": "divine_judgment", "ability_desc": "Кара: x2 против нежити/демонов", "ability_chance": 50, "description": "Боги смотрят на тебя свысока. И одобряют", "obtain": {"type": "achievement", "requirement": "50 убийств титанов"}},
    "Экзорцист": {"damage": 60, "chances": [10,20,40,65,27], "level_req": 650, "group": "священные", "ability": "exorcism", "ability_desc": "Изгнание: 20% убить нежить/демонов", "ability_chance": 50, "description": "Святой водой не обойтись. Придётся стрелять. Много стрелять", "obtain": {"type": "craft", "requirement": "легендарный крафт (скоро)"}},
}

WEAPONS_DATA = {}
for d in [WEAPONS_COMMON, WEAPONS_FIRE, WEAPONS_ICE, WEAPONS_POISON, WEAPONS_ELECTRIC, WEAPONS_DARK, WEAPONS_HOLY]:
    WEAPONS_DATA.update(d)

WEAPON_GROUPS = {
    "обычные": {"level_req": 0, "weapons": WEAPONS_COMMON},
    "огненные": {"level_req": 25, "weapons": WEAPONS_FIRE},
    "ледяные": {"level_req": 50, "weapons": WEAPONS_ICE},
    "ядовитые": {"level_req": 100, "weapons": WEAPONS_POISON},
    "электрические": {"level_req": 200, "weapons": WEAPONS_ELECTRIC},
    "тёмные": {"level_req": 350, "weapons": WEAPONS_DARK},
    "священные": {"level_req": 500, "weapons": WEAPONS_HOLY},
}

WEAPON_IDS = {name: str(i) for i, name in enumerate(WEAPONS_DATA.keys())}
WEAPON_NAMES = {v: k for k, v in WEAPON_IDS.items()}

# ================== ЭФФЕКТЫ СПОСОБНОСТЕЙ ОРУЖИЯ (ТОЧНО ПО ОПИСАНИЮ) ==================

def apply_weapon_ability(ability_name: str, user_id: int, damage: int, animal_hp: int, location: str) -> tuple:
    """
    Применяет способность оружия.
    Возвращает: (новый_урон, сообщение, дополнительный_эффект)
    """
    msg = ""
    new_damage = damage
    extra_effect = None
    
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    
    # ==================== ОГНЕННЫЕ ====================
    if ability_name == "burn":  # Огненный мушкет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'burn', 3, 8)", (user_id,))
        conn.commit()
        msg = "🔥 Животное подожжено! -8 HP в начале каждого хода (3 хода)"
    
    elif ability_name == "lava_shot":  # Вулканический револьвер
        new_damage = int(damage * 1.5)
        msg = f"🌋 Лавовый шар! Урон увеличен в 1.5 раза! {damage} → {new_damage}"
    
    elif ability_name == "ignite":  # Пирокинетический карабин
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'stun', 1, 0)", (user_id,))
        conn.commit()
        msg = "🔥 Воспламенение! Животное пропускает следующий ход!"
    
    elif ability_name == "fire_wave":  # Дыхание дракона
        new_damage = damage + 20
        msg = f"🌊 Огненный вал! Дополнительные 20 урона! {damage} → {new_damage}"
    
    elif ability_name == "eruption":  # Магматический арбалет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'damage_buff', 999, 15)", (user_id,))
        conn.commit()
        msg = "🌋 Извержение! +15% к урону до конца боя!"
    
    elif ability_name == "inferno":  # Адский револьвер
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'defense_down', 3, 15)", (user_id,))
        conn.commit()
        msg = "🔥 Адское пекло! Защита животного снижена на 15% на 3 хода!"
    
    elif ability_name == "rebirth":  # Феникс-винтовка
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'rebirth', 999, 1)", (user_id,))
        conn.commit()
        msg = "🔄 Возрождение феникса! При смерти вы воскреснете 1 раз!"
    
    # ==================== ЛЕДЯНЫЕ ====================
    elif ability_name == "snowstorm":  # Снежный револьвер
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'animal_hit_down', 2, 20)", (user_id,))
        conn.commit()
        msg = "🌨️ Снежная буря! Точность животного снижена на 20% на 2 хода!"
    
    elif ability_name == "freeze":  # Ледяной пистолет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'freeze', 1, 0)", (user_id,))
        conn.commit()
        msg = "❄️ Ледяная заморозка! Животное заморожено и пропускает ход!"
    
    elif ability_name == "ice_shard":  # Ледяная винтовка
        new_damage = int(damage * 1.5)
        msg = f"❄️ Ледяная сосулька! Критический урон x1.5! {damage} → {new_damage}"
    
    elif ability_name == "slow":  # Хладнокровный арбалет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'slow', 3, 0)", (user_id,))
        conn.commit()
        msg = "🐢 Хладнокровное замедление! Животное атакует только раз в 2 хода (3 хода)!"
    
    elif ability_name == "icicle":  # Морозный посох
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'crit_vs_frozen', 1, 200)", (user_id,))
        conn.commit()
        msg = "❄️ Ледяной кристалл! Гарантированный критический урон по замороженным целям!"
    
    elif ability_name == "iceberg":  # Северный карабин
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'iceberg', 1, 20)", (user_id,))
        conn.commit()
        msg = "🧊 Айсберг! Крит по замороженному +20 дополнительного урона!"
    
    elif ability_name == "permafrost":  # Вечная мерзлота
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'armor_down', 3, 20)", (user_id,))
        conn.commit()
        msg = "❄️ Вечная мерзлота! Броня животного снижена на 20% на 3 хода!"
    
    # ==================== ЯДОВИТЫЕ ====================
    elif ability_name == "strong_poison":  # Отравленный дротик
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'strong_poison', 3, 15)", (user_id,))
        conn.commit()
        msg = "🧪 Сильный яд! Точность животного снижена на 15% на 3 хода!"
    
    elif ability_name == "infection":  # Ядовитый револьвер
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'infection', 1, 50)", (user_id,))
        conn.commit()
        msg = "🦠 Заражение! 50% шанс, что животное умрёт при попытке побега!"
    
    elif ability_name == "paralyze":  # Змеиный клык
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'paralyze', 2, 0)", (user_id,))
        conn.commit()
        msg = "⚡ Парализующий яд! Животное не может двигаться 2 хода!"
    
    elif ability_name == "acid":  # Токсичный карабин
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'armor_down', 3, 25)", (user_id,))
        conn.commit()
        msg = "🧪 Кислотный дождь! Броня животного снижена на 25% на 3 хода!"
    
    elif ability_name == "decay":  # Некротический арбалет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'decay', 3, 12)", (user_id,))
        conn.commit()
        msg = "💀 Гниение! Животное теряет 12 HP в начале каждого хода (3 хода)!"
    
    elif ability_name == "death_poison":  # Скорпион-пистолет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'death_poison', 2, 999)", (user_id,))
        conn.commit()
        msg = "💀 Смертельный яд скорпиона! Животное умрёт через 2 хода!"
    
    elif ability_name == "epidemic":  # Бактериальная винтовка
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'epidemic', 1, 0)", (user_id,))
        conn.commit()
        msg = "🦠 Эпидемия! Яд распространится на следующее животное!"
    
    # ==================== ЭЛЕКТРИЧЕСКИЕ ====================
    elif ability_name == "paralyze_el":  # Электрошокер (переименовал чтобы не путать с ядовитым)
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'stun', 1, 0)", (user_id,))
        conn.commit()
        msg = "⚡ Электрошок! Животное парализовано и пропускает ход!"
    
    elif ability_name == "static_field":  # Разрядный пистолет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'animal_hit_down', 2, 20)", (user_id,))
        conn.commit()
        msg = "⚡ Статическое поле! Точность животного снижена на 20% на 2 хода!"
    
    elif ability_name == "chain_lightning":  # Громовой карабин
        new_damage = int(damage * 1.15)
        msg = f"⚡ Цепная молния! +15% урона и перекидывается на соседей! {damage} → {new_damage}"
    
    elif ability_name == "discharge":  # Молниевый арбалет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'no_defense', 2, 0)", (user_id,))
        conn.commit()
        msg = "⚡ Мощный разряд! Животное теряет защиту на 2 хода!"
    
    elif ability_name == "charged_shot":  # Плазменная винтовка
        new_damage = int(damage * 1.5)
        msg = f"⚡ Заряженный плазменный выстрел! Урон x1.5! {damage} → {new_damage}"
    
    elif ability_name == "emp":  # Тесла-пушка
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'disable_ability', 2, 0)", (user_id,))
        conn.commit()
        msg = "📡 Электромагнитный импульс! Способности животного отключены на 2 хода!"
    
    elif ability_name == "thunder_strike":  # Грозовой револьвер
        msg = f"⚡ Удар грома! Гарантированное попадание!"
        extra_effect = "guaranteed_hit"
    
    # ==================== ТЁМНЫЕ ====================
    elif ability_name == "darkness":  # Теневой арбалет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'animal_hit_down', 3, 30)", (user_id,))
        conn.commit()
        msg = "🌑 Абсолютная тьма! Точность животного снижена на 30% на 3 хода!"
    
    elif ability_name == "stone_skin":  # Обсидиановый револьвер
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'stone_skin', 3, 30)", (user_id,))
        conn.commit()
        msg = "🪨 Обсидиановая кожа! Ваша защита увеличена на 30% на 3 хода!"
    
    elif ability_name == "fear":  # Кошмарный карабин
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'fear', 1, 0)", (user_id,))
        conn.commit()
        msg = "😱 Кошмарный страх! Животное убегает, оставляя награду!"
    
    elif ability_name == "soul_steal":  # Душелов
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'damage_buff', 999, 20)", (user_id,))
        conn.commit()
        msg = "👻 Кража души! Ваш урон увеличен на 20% до конца боя!"
    
    elif ability_name == "bloodletting":  # Вампирский кинжал
        heal = int(damage * 0.5)
        update_health(user_id, heal)
        msg = f"🩸 Вампирское кровопускание! Вы восстанавливаете 50% от нанесённого урона! +{heal} HP"
    
    elif ability_name == "summon":  # Некро-винтовка
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'summon', 1, 0)", (user_id,))
        conn.commit()
        msg = "🧟 Некромантия! Убитое животное поможет вам в следующем бою!"
    
    elif ability_name == "curse":  # Проклятый мушкет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'curse_dark', 1, 200)", (user_id,))
        conn.commit()
        msg = "🌑 Древнее проклятие! Следующий удар нанесёт двойной урон!"
    
    # ==================== СВЯЩЕННЫЕ ====================
    elif ability_name == "blessing":  # Святой арбалет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'hit_buff', 999, 25)", (user_id,))
        conn.commit()
        msg = "✨ Святое благословение! Ваша точность увеличена на 25% до конца боя!"
    
    elif ability_name == "heal":  # Ангельский револьвер
        new_hp = update_health(user_id, 30)
        msg = "💚 Ангельское исцеление! Вы восстановили 30 HP!"
    
    elif ability_name == "faith_shield":  # Паладин-пистолет
        cur.execute("INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value) VALUES (?, 'invincible', 1, 0)", (user_id,))
        conn.commit()
        msg = "🛡️ Щит веры! В следующем ходу вы не получите урон!"
    
    elif ability_name == "light":  # Небесный карабин
        cur.execute("DELETE FROM battle_effects WHERE user_id = ?", (user_id,))
        conn.commit()
        msg = "✨ Божественный свет! Все негативные эффекты сняты!"
    
    elif ability_name == "purify":  # Светлый посох
        update_health(user_id, 20)
        cur.execute("DELETE FROM battle_effects WHERE user_id = ?", (user_id,))
        conn.commit()
        msg = "💚 Очищающий свет! +20 HP и сняты все эффекты!"
    
    elif ability_name == "divine_judgment":  # Божественная винтовка
        if location in ["Призрачный лес", "Инферно", "Болото проклятых"]:
            new_damage = int(damage * 2)
            msg = f"⚖️ Божественный суд! Двойной урон против нежити и демонов! {damage} → {new_damage}"
        else:
            msg = "⚖️ Божественный суд (обычный урон против смертных)"
    
    elif ability_name == "exorcism":  # Экзорцист
        if location in ["Призрачный лес", "Инферно", "Болото проклятых"]:
            if random.randint(1, 100) <= 20:
                msg = "🙏 Могущественное изгнание! Зло повержено мгновенно!"
                extra_effect = "instant_kill"
            else:
                msg = "🙏 Изгнание не сработало... Зло сопротивляется"
        else:
            msg = "🙏 Изгнание (не против нежити)"
    
    conn.close()
    return new_damage, msg, extra_effect


def calculate_damage_with_ability(weapon_name: str, group: str, location: str, user_id: int, body_part: str = None) -> tuple:
    """
    Рассчитывает урон с учётом всех бонусов
    Возвращает: (final_damage, ability_msg, extra_effect)
    """
    weapon_data = get_weapon_data(weapon_name)
    base_damage = weapon_data["damage"]
    
    damage_mult = 1.0
    hit_mod = 0
    
    # Бонус от локации
    location_bonus = get_weapon_location_bonus(weapon_name, location)
    damage_mult += location_bonus["damage"] / 100
    hit_mod += location_bonus["hit"]
    
    # ✅ ИСПРАВЛЕНО: Бонус от части тела должен учитываться здесь!
    if body_part and location in BODY_PARTS and body_part in BODY_PARTS[location]:
        part_data = BODY_PARTS[location][body_part]
        damage_mult *= part_data["damage_mult"]
        hit_mod += part_data["hit_mod"]
        print(f"[BODY PART] {body_part}: урон x{part_data['damage_mult']}, попадание {part_data['hit_mod']}%")
    
    # Бонус от подкрадывания
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    mod = cur.execute("SELECT hit_bonus, damage_bonus FROM battle_mods WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if mod:
        hit_mod += mod[0]
        damage_mult += mod[1] / 100
    
    # Эффекты на игроке
    effects = get_battle_effects(user_id)
    
    if "damage_buff" in effects:
        damage_mult *= (1 + effects["damage_buff"]["value"] / 100)
        update_effect_duration(user_id, "damage_buff")
    
    if "hit_buff" in effects:
        hit_mod += effects["hit_buff"]["value"]
        update_effect_duration(user_id, "hit_buff")
    
    # Проклятие тёмное
    curse_mult = 1.0
    if "curse_dark" in effects:
        curse_mult = 2.0
        update_effect_duration(user_id, "curse_dark")
    
    final_damage = int(base_damage * damage_mult * curse_mult)
    
    # Способность оружия
    ability = weapon_data.get("ability")
    ability_chance = weapon_data.get("ability_chance", 0)
    ability_msg = ""
    extra_effect = None
    
    if ability and ability_chance > 0:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        state = cur.execute("SELECT ability_used FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        
        if state and state[0] == 0:
            if random.randint(1, 100) <= ability_chance:
                conn = sqlite3.connect("hunt.db")
                cur = conn.cursor()
                animal_hp = cur.execute("SELECT animal_hp FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()[0]
                conn.close()
                
                final_damage, ability_msg, extra_effect = apply_weapon_ability(ability, user_id, final_damage, animal_hp, location)
    
    return final_damage, ability_msg, extra_effect

# ================== УЯЗВИМОСТИ ЛОКАЦИЙ К ТИПАМ ОРУЖИЯ ==================
# love - любит (бонус), hate - не любит (штраф)
LOCATION_WEAPON_WEAKNESS = {
    "Тайга": {"love": ["огненные"], "hate": ["ледяные", "тёмные"]},
    "Саванна": {"love": ["ледяные"], "hate": ["огненные", "электрические"]},
    "Арктика": {"love": ["огненные"], "hate": ["ледяные", "ядовитые"]},
    "Джунгли": {"love": ["электрические"], "hate": ["ядовитые", "огненные"]},
    "Горы": {"love": ["ядовитые"], "hate": ["электрические", "ледяные"]},
    "Древний мир": {"love": ["священные"], "hate": ["тёмные", "электрические"]},
    "Подводный мир": {"love": ["электрические"], "hate": ["ледяные", "огненные"]},
    "Болото проклятых": {"love": ["огненные", "священные"], "hate": ["ядовитые", "тёмные"]},
    "Призрачный лес": {"love": ["священные", "электрические"], "hate": ["тёмные", "ядовитые"]},
    "Рад-зона": {"love": ["электрические", "священные"], "hate": ["ядовитые", "тёмные"]},
    "Грозовая бездна": {"love": ["ледяные", "тёмные"], "hate": ["электрические", "огненные"]},
    "Киберпанк": {"love": ["ядовитые", "электрические"], "hate": ["тёмные", "священные"]},
    "Инферно": {"love": ["ледяные", "священные"], "hate": ["огненные", "тёмные"]},
    "Космическая пустошь": {"love": ["тёмные", "электрические"], "hate": ["священные", "ледяные"]},
    "🐣 Пасхальная поляна": {"love": [], "hate": []},  # ивентовая локация - нейтральна
}

# Бонусы и штрафы для оружия
WEAPON_LOCATION_BONUS = {
    "love": {"hit": 15, "damage": 10, "coins": 10, "exp": 10},      # любит: +15% попадание, +10% урон, +10% монет, +10% опыт
    "hate": {"hit": -20, "damage": -15, "coins": -15, "exp": -15},   # не любит: -20% попадание, -15% урон, -15% монет, -15% опыт
}

# ================== ЧАСТИ ТЕЛА ДЛЯ КАЖДОЙ ЛОКАЦИИ ==================
BODY_PARTS = {
    "Тайга": {
        "🐻 Голова": {"damage_mult": 2.0, "hit_mod": -15, "effect": None},
        "🧥 Шкура": {"damage_mult": 1.0, "hit_mod": 5, "effect": None},
        "🦵 Лапы": {"damage_mult": 0.7, "hit_mod": 15, "effect": "slow"},
        "🫁 Брюхо": {"damage_mult": 1.3, "hit_mod": -5, "effect": None}
    },
    "Саванна": {
        "🦁 Голова": {"damage_mult": 2.2, "hit_mod": -20, "effect": None},
        "🧥 Спина": {"damage_mult": 1.0, "hit_mod": 10, "effect": None},
        "🦵 Ноги": {"damage_mult": 0.8, "hit_mod": 10, "effect": "trip"},
        "🫁 Живот": {"damage_mult": 1.4, "hit_mod": -10, "effect": None}
    },
    "Арктика": {
        "🐻‍❄️ Голова": {"damage_mult": 1.8, "hit_mod": -10, "effect": None},
        "🧥 Шуба": {"damage_mult": 1.0, "hit_mod": 0, "effect": None},
        "🦵 Ласты": {"damage_mult": 0.6, "hit_mod": 20, "effect": "freeze"},
        "🫁 Брюхо": {"damage_mult": 1.2, "hit_mod": 0, "effect": None}
    },
    "Джунгли": {
        "🐯 Голова": {"damage_mult": 2.0, "hit_mod": -15, "effect": None},
        "🧥 Шкура": {"damage_mult": 1.0, "hit_mod": 0, "effect": None},
        "🦵 Лапы": {"damage_mult": 0.7, "hit_mod": 15, "effect": "poison"},
        "🫁 Брюхо": {"damage_mult": 1.3, "hit_mod": -5, "effect": None}
    },
    "Горы": {
        "🦅 Голова": {"damage_mult": 2.5, "hit_mod": -25, "effect": None},
        "🧥 Крылья": {"damage_mult": 1.0, "hit_mod": 5, "effect": None},
        "🦵 Лапы": {"damage_mult": 0.5, "hit_mod": 20, "effect": "trip"},
        "🫁 Туловище": {"damage_mult": 1.2, "hit_mod": -5, "effect": None}
    },
    "Древний мир": {
        "🦕 Пасть": {"damage_mult": 2.0, "hit_mod": -15, "effect": None},
        "🧥 Спина": {"damage_mult": 1.0, "hit_mod": 0, "effect": None},
        "🦵 Ноги": {"damage_mult": 0.7, "hit_mod": 15, "effect": None},
        "🫁 Брюхо": {"damage_mult": 1.3, "hit_mod": -5, "effect": None}
    },
    "Подводный мир": {
        "🦈 Голова": {"damage_mult": 1.8, "hit_mod": -10, "effect": None},
        "🧥 Плавник": {"damage_mult": 1.0, "hit_mod": 10, "effect": None},
        "🦵 Хвост": {"damage_mult": 0.8, "hit_mod": 10, "effect": None},
        "🫁 Брюхо": {"damage_mult": 1.2, "hit_mod": 0, "effect": None}
    },
    "Болото проклятых": {
        "🧟 Голова": {"damage_mult": 2.0, "hit_mod": -15, "effect": None},
        "🧥 Гнилая плоть": {"damage_mult": 1.0, "hit_mod": -10, "effect": None},
        "🦵 Ноги": {"damage_mult": 0.7, "hit_mod": 15, "effect": None},
        "🫁 Живот": {"damage_mult": 1.3, "hit_mod": 0, "effect": None}
    },
    "Призрачный лес": {
        "👻 Голова": {"damage_mult": 2.0, "hit_mod": -20, "effect": None},
        "🧥 Тень": {"damage_mult": 1.0, "hit_mod": -10, "effect": None},
        "🦵 Ноги": {"damage_mult": 0.7, "hit_mod": 15, "effect": None},
        "🫁 Сердце": {"damage_mult": 1.5, "hit_mod": -10, "effect": None}
    },
    "Рад-зона": {
        "👾 Голова": {"damage_mult": 2.0, "hit_mod": -15, "effect": None},
        "🧥 Мутировавший орган": {"damage_mult": 0.8, "hit_mod": 10, "effect": None},
        "🦵 Ноги": {"damage_mult": 0.7, "hit_mod": 15, "effect": None},
        "🫁 Живот": {"damage_mult": 1.3, "hit_mod": -5, "effect": None}
    },
    "Грозовая бездна": {
        "⚡ Голова": {"damage_mult": 2.0, "hit_mod": -15, "effect": None},
        "🧥 Тело": {"damage_mult": 1.0, "hit_mod": 0, "effect": None},
        "🦵 Конечности": {"damage_mult": 0.7, "hit_mod": 15, "effect": "paralyze"},
        "🫁 Ядро": {"damage_mult": 1.3, "hit_mod": -5, "effect": None}
    },
    "Киберпанк": {
        "💻 Процессор": {"damage_mult": 2.5, "hit_mod": -20, "effect": None},
        "🧥 Броня": {"damage_mult": 0.8, "hit_mod": 10, "effect": None},
        "🦵 Механизмы": {"damage_mult": 0.6, "hit_mod": 15, "effect": "slow"},
        "🫁 Батарея": {"damage_mult": 1.5, "hit_mod": -10, "effect": None}
    },
    "Инферно": {
        "👹 Голова": {"damage_mult": 2.0, "hit_mod": -15, "effect": None},
        "🧥 Пламя": {"damage_mult": 1.0, "hit_mod": -10, "effect": None},
        "🦵 Ноги": {"damage_mult": 0.7, "hit_mod": 15, "effect": None},
        "🫁 Сердце": {"damage_mult": 1.3, "hit_mod": 0, "effect": None}
    },
    "Космическая пустошь": {
        "👽 Голова": {"damage_mult": 2.0, "hit_mod": -20, "effect": None},
        "🧥 Тело": {"damage_mult": 1.0, "hit_mod": 0, "effect": None},
        "🌌 Материя": {"damage_mult": 0.7, "hit_mod": 15, "effect": None},
        "🫁 Ядро": {"damage_mult": 1.3, "hit_mod": -5, "effect": None}
    },
    "🐣 Пасхальная поляна": {
        "🥚 Голова": {"damage_mult": 2.0, "hit_mod": -10, "effect": None},
        "🧥 Скорлупа": {"damage_mult": 1.0, "hit_mod": 10, "effect": None},
        "🦵 Ноги": {"damage_mult": 0.8, "hit_mod": 10, "effect": None},
        "🫁 Желток": {"damage_mult": 1.2, "hit_mod": 0, "effect": None}
    }
}

# ================== СПОСОБНОСТИ ТИТАНОВ (только с Древнего мира) ==================
TITAN_ABILITIES = {
    "Древний мир": {
        "name": "🕐 Закручивает время",
        "effect": "time_rewind",
        "chance": 20,
        "description": "20% шанс отбить атаку"
    },
    "Подводный мир": {
        "name": "🌊 Поток воды",
        "effect": "water_flow",
        "chance": 30,
        "description": "30% шанс отбить атаку"
    },
    "Болото проклятых": {
        "name": "🧪 Проклятие",
        "effect": "curse",
        "chance": 60,
        "description": "Следующая атака игрока -60% к попаданию"
    },
    "Призрачный лес": {
        "name": "👻 Порча",
        "effect": "corruption",
        "chance": 40,
        "description": "40% шанс не дать выстрелить"
    },
    "Рад-зона": {
        "name": "☢️ Радиация",
        "effect": "radiation",
        "chance": 100,
        "description": "Каждый ход -30 HP игроку"
    },
    "Грозовая бездна": {
        "name": "⚡ Молния",
        "effect": "lightning",
        "chance": 60,
        "description": "60% промах + -20 HP игроку"
    },
    "Киберпанк": {
        "name": "💾 Вирус",
        "effect": "virus",
        "chance": 40,
        "description": "40% шанс выстрелить в себя (-50 HP)"
    },
    "Инферно": {
        "name": "🔥 Струя огня",
        "effect": "fire_jet",
        "chance": 100,
        "description": "Каждый ход -40 HP игроку"
    },
    "Космическая пустошь": {
        "name": "🌀 Сингулярность",
        "effect": "singularity",
        "chance": 25,
        "description": "25% шанс мгновенной смерти"
    }
}

ANIMAL_ACTIONS = {
    "Опасн": [
        {"name": "🗡️ Атакует", "damage": 25, "hit_mod": 0, "chance": 60},
        {"name": "🛡️ Защищается", "damage": 0, "hit_mod": -10, "chance": 30},
        {"name": "🏃 Пытается убежать", "damage": 0, "hit_mod": 0, "chance": 10}
    ],
    "Тяжел": [
        {"name": "🗡️ Атакует", "damage": 50, "hit_mod": 0, "chance": 65},
        {"name": "🛡️ Защищается", "damage": 0, "hit_mod": -15, "chance": 35}
    ],
    "Титан": [
        {"name": "🗡️ Атакует", "damage": 75, "hit_mod": 0, "chance": 50},
        {"name": "🛡️ Защищается", "damage": 0, "hit_mod": -30, "chance": 25},
        {"name": "💚 Регенерирует", "damage": 0, "heal": 30, "chance": 25}
    ]
}

# ================== ФРАЗЫ ПРИ ПРОМАХЕ ==================
MISS_PHRASES = [
    "Пуля решила познакомиться с деревом вместо цели! 🌳 @Chatbothunt",
    "Животное сделало грациозный пируэт и уклонилось! 💃 @Chatbothunt",
    "Ваш выстрел был так же близко, как Луна к Земле! 🌙 @Chatbothunt",
    "Зверь проявил чудеса акробатики! 🤸 @Chatbothunt",
    "Пуля отправилась в самостоятельное путешествие! 🧭 @Chatbothunt",
    "Мимо! Но зато красивая траектория! ✨ @Chatbothunt",
    "Животное поймало вашу пулю на лету и вернуло! 🥎 @Chatbothunt",
    "Выстрел был эффектным, но не точным! 🎭 @Chatbothunt",
    "Зверь услышал выстрел и элегантно увернулся! 🕺 @Chatbothunt",
    "Ваша пуля решила, что сегодня ее выходной! 🏖️ @Chatbothunt",
    "Мишень оказалась мастером тай-чи! 🥋 @Chatbothunt",
    "Пуля предпочла полюбоваться пейзажем! 🏞️ @Chatbothunt",
    "Животное использовало технику 'невидимое поле'! 🛡️ @Chatbothunt",
    "Выстрел был близок, но не достаточно! 📏 @Chatbothunt",
    "Зверь продемонстрировал феноменальную реакцию! ⚡ @Chatbothunt",
    "Начался дождь из Пасхальных яиц, видимость нулевая. 🥚",
    "Вас отвлёк Пасхальный кролик 🐇"
]

# ================== СНАРЯЖЕНИЕ ==================
EQUIPMENT = {
    "Приманка": {
        "price": 1000,
        "description": "+5% к поиску опасных животных",
        "bonus": {"Опасн": 5}
    },
    "Маскировка": {
        "price": 3000,
        "description": "+5% к поиску опасных и +5% к поиску тяжелых животных",
        "bonus": {"Опасн": 5, "Тяжел": 5}
    },
    "Локатор": {
        "price": 12500,
        "description": "+10% к поиску опасных, +5% к поиску тяжелых и +3% к поиску титанов",
        "bonus": {"Опасн": 10, "Тяжел": 5, "Титан": 3}
    },
    "Рюкзак": {
        "price": 20000,
        "description": "+100 к максимальному здоровью",
        "bonus": {"health": 100}
    },
    "Улучшенные ловушки": {
        "price": 20000,
        "description": "Вы находите 5 животных вместо 3, при использовании ловушек",
        "bonus": {"traps": 5}
    },
    "Витамины": {
        "price": 5000,
        "description": "Увеличивает скорость восстановления здоровья в 1.5 раза",
        "bonus": {"healing_bonus": 1.5},
    }
#   "🐉 Драконья кровь": {
#     "price": 0,
#     "description": "+10% к шансу выпадения мутации",
#     "bonus": {"mutation_chance": 10}
# }
}

# ================== ПРЕДМЕТЫ ДЛЯ ВЫЖИВАНИЯ ==================
SURVIVAL_ITEMS = {
    # Тайга
    "Теплые варежки": {
        "location": "Тайга",
        "price": 500,
        "description": "+5% к поиску животных в Тайге",
        "bonus": {"search_bonus": 5}
    },
    "Компас охотника": {
        "location": "Тайга",
        "price": 1500,
        "description": "+3% ко всем шансам попадания в Тайге",
        "bonus": {"hit_bonus": 3}
    },
    
    # Саванна
    "Фляга с водой": {
        "location": "Саванна",
        "price": 2500,
        "description": "Защищает от жары в Саванне",
        "survival": True
    },
    "Шляпа от солнца": {
        "location": "Саванна",
        "price": 3500,
        "description": "+5% к поиску животных в Саванне",
        "bonus": {"search_bonus": 5}
    },
    
    # Арктика
    "Меховой костюм": {
        "location": "Арктика",
        "price": 4000,
        "description": "Защищает от холода в Арктике",
        "survival": True
    },
    "Термос": {
        "location": "Арктика",
        "price": 2500,
        "description": "+3% к опыту за животных в Арктике",
        "bonus": {"exp_bonus": 3}
    },
    
    # Джунгли
    "Анти сетка": {
        "location": "Джунгли",
        "price": 5000,
        "description": "Защищает от ядов в Джунглях",
        "survival": True
    },
    "Мачете": {
        "location": "Джунгли",
        "price": 4500,
        "description": "+5% к поиску животных в Джунглях",
        "bonus": {"search_bonus": 5}
    },

     # Горы
    "Кислород Б": {
        "location": "Горы",
        "price": 7000,
        "description": "Защищает от высотной болезни",
        "survival": True
    },
    "Ледоруб": {
        "location": "Горы",
        "price": 4000,
        "description": "+3% к шансу попадания в Горах",
        "bonus": {"hit_bonus": 3}
    },
    
    # Древний
    "Стабилизатор": {
        "location": "Древний мир",
        "price": 12500,
        "description": "Защищает от временных аномалий",
        "survival": True
    },

    "Арх Кисть": {
        "location": "Древний мир",
        "price": 8000,
        "description": "+5% к опыту за древних животных",
        "bonus": {"exp_bonus": 5}
    },
    
    # Подводный мир
    "Акваланг": {
        "location": "Подводный мир",
        "price": 15000,
        "description": "Позволяет дышать под водой",
        "survival": True
    },
    "Гидрокостюм": {
        "location": "Подводный мир",
        "price": 8000,
        "description": "+5% к поиску животных под водой",
        "bonus": {"search_bonus": 5}
    },

    # Болото проклятых
    "Талисман": {
        "location": "Болото проклятых",
        "price": 25000,
        "description": "Защищает от проклятий и ядовитых испарений",
        "survival": True
    },
    "Сапоги-ходунки": {
        "location": "Болото проклятых",
        "price": 15000,
        "description": "+5% к поиску животных в болоте",
        "bonus": {"search_bonus": 5}
    },
    
    # Призрачный лес
    "Амулет луны": {
        "location": "Призрачный лес",
        "price": 45000,
        "description": "Защищает от призрачных сущности",
        "survival": True
    },
    "Свеча души": {
        "location": "Призрачный лес",
        "price": 25000,
        "description": "+5% к шансу попадания по призрачным существам",
        "bonus": {"hit_bonus": 5}
    },

    # Рад-зона
    "Рад костюм": {
        "location": "Рад-зона",
        "price": 60000,
        "description": "Защищает от радиации",
        "survival": True
    },
    "Дозиметр": {
        "location": "Рад-зона",
        "price": 40000,
        "description": "+5% к поиску сущностей в рад-зоне",
        "bonus": {"search_bonus": 5}

    },

    # Грозовая бездна
    "Громоотвод": {
        "location": "Грозовая бездна",
        "price": 90000,
        "description": "Защищает от ударов молний и электрических разрядов",
        "survival": True
    },
    "Молниеотвод": {
        "location": "Грозовая бездна",
        "price": 50000,
        "description": "+10% к шансу попадания в Грозовой бездне",
        "bonus": {"hit_bonus": 10}
    },

    # Киберпанк
    "Антивирус": {
        "location": "Киберпанк",
        "price": 120000,
        "description": "Защищает от взломов",
        "survival": True
    },
    "Цифровая пуля": {
        "location": "Киберпанк",
        "price": 80000,
        "description": "+5% к шансу попадания по кибер существам",
        "bonus": {"hit_bonus": 5}
    },

    # Инферно
    "Обс доспехи": {
        "location": "Инферно",
        "price": 150000,
        "description": "Защищает от адского жара и лавовых потоков",
        "survival": True
    },
    "Глаз демона": {
        "location": "Инферно",
        "price": 100000,
        "description": "+10% к шансу попадания в Инферно",
        "bonus": {"hit_bonus": 10}
    },

    # Космическая пустошь
    "Скафандр": {
        "location": "Космическая пустошь",
        "price": 200000,
        "description": "Защищает от вакуума, радиации и перепадов температур",
        "survival": True
    },
    "Направлятель": {
        "location": "Космическая пустошь",
        "price": 120000,
        "description": "+10% к поиску животных в космической пустоши",
        "bonus": {"search_bonus": 10}
    }
}

# Фразы при потере HP из-за отсутствия предмета выживания
SURVIVAL_DAMAGE_PHRASES = {
    "Саванна": [
        "🔥 Невыносимая жара в Саванне иссушает ваши силы! -80HP",
        "☀️ Солнце палит нещадно! Без воды вы слабеете. -80HP"
    ],
    "Арктика": [
        "❄️ Лютый холод Арктики пронизывает до костей! -80HP",
        "🌬️ Ледяной ветер высасывает из вас тепло. -80HP"
    ],
    "Джунгли": [
        "🐍 Ядовитые испарения джунглей отравляют вас! -80HP",
        "🦟 Тропические болезни подрывают здоровье. -80HP"
    ],
    "Горы": [
        "⛰️ Высотная болезнь сжимает ваши легкие! -80HP",
        "💨 Нехватка кислорода на высоте ослабляет вас. -80HP"
    ],
    "Древний мир": [
        "🌀 Временные аномалии разрушают вашу сущность! -80HP",
        "⏳ Искажение времени сказывается на здоровье. -80HP"
    ],
    "Подводный мир": [
        "🌊 Без акваланга вы задыхаетесь под водой! -80HP",
        "💧 Давление воды разрушает ваш организм. -80HP"
    ],
    "Болото проклятых": [
        "🧪 Болотные испарения отравляют кровь! -80HP",
        "🦠 Ядовитая трясина разъедает кожу и плоть! -80HP",
        "👻 Проклятие болота высасывает жизненные силы прямо из души! -80HP"
    ],
    "Призрачный лес": [
        "👻 Призрачные сущности высасывают жизненную энергию! -80HP",
        "🕯️ Темная магия леса истощает ваши силы. -80HP"
    ],
    "Рад-зона": [
        "☣️ Высокий радиационный фон сжигает вас изнутри! -80HP",
        "☢️ Невидимое излучение разрушает ваши клетки! -80HP",
        "📟 Треск счетчика Гейгера предвещает беду. Лучевая болезнь прогрессирует! -80HP"
    ],
    "Грозовая бездна": [
        "⚡ Гигантская молния бьёт прямо в вас! -80HP",
        "🌩️ Грозовой разряд проходит через всё тело, оставляя ожоги! -80HP",
        "💥 Статическое электричество в воздухе разрывает ткань лёгких! -80HP"
    ],
    "Киберпанк": [
        "💾 Враждебный вирус взламывает вашу нейросеть! -80HP",
        "⚡ Цифровой удар выжигает ваши импланты и мозг. -80HP",
        "📡 Корпоративный софт-убийца перегревает ваш процессор. -80HP"
    ],
    "Инферно": [
        "🌋 Раскалённая лава вырывается из-под ног и обжигает вас! -80HP",
        "🔥 Адское пекло сжигает лёгкие при каждом вдохе! -80HP",
        "💨 Ядовитые серные газы разъедают горло и глаза! -80HP"
    ],
    "Космическая пустошь": [
        "🌠 Космическая радиация пронзает ваше тело насквозь! -80HP",
        "🌀 Микрометеоритный поток пробивает защиту! -80HP",
        "💀 Вакуум высасывает воздух из лёгких, давление разрывает капилляры! -80HP"
    ]

}

# Баффы (одноразовые)
BUFFS = {
    "Аптечка": {
        "price": 750,
        "description": "Восстанавливает 60 HP",
        "effect": "medkit"
    },
    "Золотая пуля": {
        "price": 2000,
        "description": "x2 шанс попадания в следующее животное (сгорает после выстрела)",
        "effect": "golden_bullet"
    },
    "Алмазная пуля": {
        "price": 5000,
        "description": "+20% шанс попасть в следующее животное",
        "effect": "diamond_bullet"
    },
    "Дрон": {
        "price": 2000,
        "description": "Находит 3 животных на выбор, +10% шанс найти выбранное животное на 30 мин",
        "effect": "drone"
    },
    "Ультра-звуковой дрон": {
        "price": 7000,
        "description": "Находит 4 животных (только Опасн/Тяжел/Титан). Шансы: Опасн 70%, Тяжел 25%, Титан 5%",
        "effect": "ultra_drone"
    },
    "Посох бессмертия": {
        "price": 4000,
        "description": "Защищает от контратаки следующего животного",
        "effect": "immortality_staff"
    },
    "Энергетик": {
        "price": 1000,
        "description": "Следующие 3 ханта без задержки по времени",
        "effect": "no_cooldown_charges",
        "charges": 3
    }

}

ANIMAL_ATTACK_PHRASES = {
    # Тайга
    "Кабан": ["Кабан яростно бросается на вас! -25HP", "Кабан бьет клыками! -25HP"],
    "Рысь": ["Рысь царапает когтями! -25HP", "Рысь прыгает на вас! -25HP"],
    "Росомаха": ["Росомаха впивается в руку! -25HP", "Росомаха атакует! -25HP"],
    "Серый волк": ["Волк впивается в руку! -25HP", "Волк стаей окружает вас! -25HP"],
    "Бурый медведь": ["Бурый медведь наносит сокрушительный удар! -25HP", "Бурый медведь сбивает с ног! -25HP"],
    "Гадюка": ["Гадюка молниеносно кусает за ногу! -25HP", "Ядовитая змея впивается в руку! -25HP"],
    "Гризли": ["Гризли раздирает когтями! -25HP", "Гризли сбивает с ног чудовищной лапой! -25HP"],
    "Баран": ["Баран бодает рогами! -25HP", "Баран сбивает с ног! -25HP"],
    "Зубр": ["Зубр бьёт мощными рогами! -50HP", "Зубр топчет вас могучими копытами! -50HP"],
    "Амурский Тигр": ["Амурский тигр прыгает из засады! -50HP", "Тигр впивается клыками в плечо! -50HP"],
    "Лось": ["Лось бьет рогами! -50HP", "Лось топчет копытами! -50HP"],
    "Оборотень": ["Оборотень впивается клыками в горло! -100HP", "Оборотень разрывает когтями! -100HP"],
    "Вендиго": ["Вендиго пронзает ледяным криком! -100HP", "Вендиго разрывает плоть костяными пальцами! -100HP"],
    "Василиск": ["Василиск обращает в камень вашу руку! -100HP", "Взгляд Василиска сковывает движения! -100HP"],

    # Саванна
    "Гиена": ["Гиена хватает за ногу! -25HP", "Гиена стаей нападает! -25HP"],
    "Пума": ["Пума прыгает на вас! -25HP", "Пума царапает! -25HP"],
    "Лев": ["Лев сбивает с ног ударом лапы! -25HP", "Лев впивается в плечо! -25HP"],
    "Леопард": ["Леопард обездвиживает вас хваткой! -25HP", "Леопард царапает когтями! -25HP"],
    "Гепард": ["Гепард сбивает с ног с разбега! -25HP", "Гепард молниеносно кусает за руку! -25HP"],
    "Мамба": ["Мамба атакует с невероятной скоростью! -25HP", "Яд мамбы обжигает вены! -25HP"],
    "Жираф": ["Жираф бьёт мощной шеей! -50HP", "Жираф сбивает ударом головы! -50HP"],
    "Буйвол": ["Буйвол топчет копытами! -50HP", "Буйвол бьет рогами! -50HP"],
    "Африканский Слон": ["Слон поднимает вас хоботом и бросает! -50HP", "Слон топчет! -50HP"],
    "Бегемот": ["Бегемот перекусывает вас пополам! -50HP", "Бегемот давит своей тушей! -50HP"],
    "Гротсланг": ["Гротсланг обвивает вас и сдавливает! -100HP", "Гротсланг кусает ядовитыми клыками! -100HP"],
    "Кикияон": ["Кикияон высасывает вашу жизненную силу! -100HP", "Кикияон погружает вас в вечный сон! -100HP"],
    "Нанди": ["Нанди разрывает жертву медвежьей хваткой! -100HP", "Нанди наносит смертельный удар лапой! -100HP"],

    # Арктика
    "Снежный барс": ["Снежный барс прыгает на вас! -25HP", "Снежный барс царапает! -25HP"],
    "Белый медведь": ["Белый медведь сбивает лапой! -25HP", "Белый медведь кусает! -25HP"],
    "Морской леопард": ["Морской леопард утаскивает под лёд! -25HP", "Морской леопард раздирает когтями! -25HP"],
    "Морж": ["Морж атакует клыками! -50HP", "Морж бьет туловищем! -50HP"],
    "Белуха": ["Белуха выпрыгивает из воды! -50HP", "Белуха таранит! -50HP"],
    "Овцебык": ["Овцебык таранит вас! -50HP", "Овцебык бьет рогами! -50HP"],
    "Косатка": ["Косатка выпрыгивает из воды! -50HP", "Косатка таранит! -50HP"],
    "Морской слон": ["Морской слон сминает вас своим весом! -50HP", "Морской слон кусает мощными челюстями! -50HP"],
    "Мамонт": ["Мамонт сминает под собой! -100HP", "Мамонт бьет бивнями! -100HP"],
    "Йети": ["Йети разрывает на части! -100HP", "Йети сдирает кожу! -100HP"],
    "Ледяной дракон": ["Ледяной дракон вымораживает вас до костей! -100HP", "Ледяной дракон пронзает сосульками! -100HP"],

    # Джунгли
    "Комодский варан": ["Комодский варан кусает ядовитыми зубами! -25HP", "Комодский варан бьет хвостом! -25HP"],
    "Крокодил": ["Крокодил хватает челюстями! -25HP", "Крокодил тащит под воду! -25HP"],
    "Анаконда": ["Анаконда обвивает и душит! -25HP", "Анаконда сжимает! -25HP"],
    "Ягуар": ["Ягуар нападает из засады! -25HP", "Ягуар впивается клыками! -25HP"],
    "Горилла": ["Горилла бьет кулаком! -25HP", "Горилла ломает кости! -25HP"],
    "Тигр": ["Тигр набрасывается на вас! -25HP", "Тигр разрывает когтями! -25HP"],
    "Пантера": ["Пантера прыгает со дерева! -25HP", "Пантера кусает за шею! -25HP"],
    "Носорог": ["Носорог пробивает брешь в защите! -50HP", "Носорог таранит! -50HP"],
    "Лесной Слон": ["Лесной слон вырывает деревья с корнем и бросает в вас! -50HP", "Лесной слон топчет вас! -50HP"],
    "Гаур": ["Гаур пронзает вас рогом! -50HP", "Гаур топчет копытами! -50HP"],
    "Чупакабра": ["Чупакабра высасывает всю кровь! -100HP", "Чупакабра разрывает плоть! -100HP"],
    "Бойтата": ["Бойтата обжигает огненным взглядом! -100HP", "Бойтата поджигает землю под вами! -100HP"],
    "Якумама": ["Якумама тянет вас в болотную пучину! -100HP", "Якумама душит водорослями! -100HP"],

    # Древний мир
    "Смилодон": ["Смилодон впивается клыками! -25HP", "Саблезубый тигр атакует! -25HP"],
    "Энтелодонт": ["Энтелодонт кусает мощными челюстями! -25HP", "Свино-медведь атакует! -25HP"],
    "Келенкен": ["Келенкен клюет огромным клювом! -25HP", "Исполинская птица атакует! -25HP"],
    "Гиенодон": ["Гиенодон разрывает плоть! -25HP", "Древний хищник нападает! -25HP"],
    "Трицератопс": ["Трицератопс атакует! -50HP", "Трицератопс прокалывает рогами! -50HP"],
    "Стегозавр": ["Стегозавр ударяет хвостом! -50HP", "Стегозавр бьет шипами! -50HP"],
    "Гадрозавр": ["Гадрозавр топчет! -50HP", "Утконосый динозавр атакует! -50HP"],
    "Эласмотерий": ["Эласмотерий бьет рогом! -50HP", "Гигантский носорог таранит! -50HP"],
    "Мегалания": ["Мегалания кусает! -50HP", "Гигантский ленивец атакует! -50HP"],
    "Шерстистый носорог": ["Шерстистый носорог бьет рогом! -50HP", "Шерстистый носорог ледникового периода атакует! -50HP"],
    "Тираннозавр": ["Тираннозавр хватает вас в пасть! -100HP", "Король динозавров дробит кости! -100HP"],
    "Брахиозавр": ["Брахиозавр наступает на вас! -100HP", "Гигантский зауропод давит! -100HP"],
    "Птеродактиль": ["Птеродактиль хватает и бросает с высоты! -100HP", "Летающий ящер клюет! -100HP"],
    "Годзилла": ["Годзилла испепеляет атомным дыханием! -100HP", "Годзилла сметает вас хвостом! -100HP"],

    # Горы
    "Сапсан": ["Сапсан пикирует на вас! -25HP", "Сокол клюет! -25HP"],
    "Беркут": ["Беркут хватает когтями! -25HP", "Золотой орел атакует! -25HP"],
    "Ястреб": ["Ястреб царапает когтями! -25HP", "Хищная птица нападает! -25HP"],
    "Бородач": ["Бородач сбрасывает кости с высоты! -25HP", "Бородач клюет в голову! -25HP"],
    "Черный гриф": ["Черный гриф клюет! -50HP", "Гриф-падальщик атакует! -50HP"],
    "Кондор": ["Кондор бьет крыльями! -50HP", "Гигантский кондор атакует! -50HP"],
    "Пеликан": ["Пеликан пытается проглотить вас целиком! -50HP", "Пеликан бьет мощным клювом! -50HP"],
    "Орел": ["Орел-великан хватает когтями! -100HP", "Гигантский орел уносит в небо! -100HP"],
    "Птица Рух": ["Рух хватает и поднимает на огромную высоту! -100HP", "Мифическая птица атакует! -100HP"],
    "Зиз": ["Зиз закрывает крыльями солнце и швыряет вас в пропасть! -100HP", "Зиз обрушивает на вас скалу! -100HP"],

    # Подводный мир
    "Удильщик": ["Удильщик кусает светящимися зубами! -25HP", "Глубоководный хищник атакует! -25HP"],
    "Мурена": ["Мурена впивается зубами! -25HP", "Электрическая мурена бьет током! -25HP"],
    "Барракуда": ["Барракуда пронзает скоростью! -25HP", "Барракуда кусает! -25HP"],
    "Крылатка": ["Крылатка впрыскивает яд в кровь! -25HP", "Крылатка атакует ядовитыми шипами! -25HP"],
    "Пиранья": ["Стая пираний обгладывает плоть заживо! -25HP", "Пиранья вырывает кусок мяса! -25HP"],
    "Манта": ["Манта бьет хвостом! -50HP", "Гигантский скат накрывает! -50HP"],
    "Кашалот": ["Кашалот оглушает звуком! -50HP", "Гигантский кит таранит! -50HP"],
    "Акула": ["Акула кусает! -50HP", "Большая белая акула атакует! -50HP"],
    "Кит": ["Кит хватает планктон вместе с вами! -50HP", "Кит бьет хвостом по воде! -50HP"],
    "Мегалодон": ["Мегалодон перекусывает пополам! -100HP", "Доисторическая акула пожирает! -100HP"],
    "Кракен": ["Кракен обвивает щупальцами! -100HP", "Морское чудовище тянет на дно! -100HP"],
    "Левиафан": ["Левиафан проглатывает целиком! -100HP", "Библейское чудовище разрушает! -100HP"],
    "Геликоприон": ["Геликоприон перемалывает вас спиралью зубов! -100HP", "Акула-пила атакует! -100HP"],

    # Призрачный лес
    "Вервольф": ["Вервольф впивается клыками! -25HP", "Оборотень-волк разрывает! -25HP"],
    "Теневой Ворон": ["Теневой Ворон клюет призрачным клювом! -25HP", "Темная птица атакует! -25HP"],
    "Призрак": ["Призрак проходит сквозь вас! -25HP", "Призрачная сущность высасывает жизненную силу! -25HP"],
    "Упырь": ["Упырь кусает вампирскими клыками! -25HP", "Ночной охотник атакует! -25HP"],
    "Вампир": ["Вампир высасывает кровь за секунды! -25HP", "Вампир гипнотизирует и впивается в шею! -25HP"],
    "Лорд Тумана": ["Лорд Тумана душит вас сгустком тьмы! -25HP", "Лорд Тумана вселяет кошмары в голову! -25HP"],
    "Проклятый рыцарь": ["Проклятый рыцарь пронзает мечом! -25HP", "Проклятый рыцарь топчет лошадью! -25HP"],
    "Энт": ["Энт бьет ветвями! -50HP", "Древодерево сокрушает! -50HP"],
    "Мантикора": ["Мантикора жалит ядовитым хвостом! -50HP", "Мифический зверь атакует! -50HP"],
    "Минотавр": ["Минотавр пронзает рогами! -50HP", "Минотавр сбрасывает с обрыва! -50HP"],
    "Горгулья": ["Горгулья бьет каменными крыльями! -50HP", "Горгулья хватает и поднимает в небо! -50HP"],
    "Владыка леса": ["Владыка леса насылает проклятие! -100HP", "Дух леса уничтожает! -100HP"],
    "Всадник": ["Всадник без головы проносится сквозь вас! -100HP", "Призрачный всадник атакует! -100HP"],
    "Великий лич": ["Великий лич вырывает вашу душу из тела! -100HP", "Великий лич воскрешает мертвецов вокруг вас! -100HP"],
    "Черный Дракон": ["Черный дракон испепеляет черным пламенем! -100HP", "Черный дракон разрывает когтями! -100HP"],

    # Рад-зона
    "Химера": ["Химера прыгает из тени! -25HP", "Двуглавая хищница разрывает когтями! -25HP"],
    "Излом": ["Излом бьет длинной рукой! -25HP", "Излом наносит сокрушительный удар! -25HP"],
    "Рад-волк": ["Рад-волк впивается в горло! -50HP", "Мутировавший волк терзает плоть! -50HP"],
    "Гигант": ["Гигант сотрясает землю топотом! -50HP", "Псевдогигант втаптывает вас в грязь! -50HP"],
    "Мутант": ["Ужасающий мутант крушит кости! -50HP", "Громадный мутант раздавливает вас! -50HP"],
    "Зверобой": ["Зверобой наносит смертельную рану! -50HP", "Зверобой уничтожает цель! -50HP"],
    "Кровосос": ["Кровосос впивается щупальцами в шею! -100HP", "Невидимый охотник наносит удар из засады! -100HP"],
    "Сталкер": ["Черный Сталкер стреляет точно в цель! -100HP", "Призрак Зоны наказывает за дерзость! -100HP"],

    # Киберпанк
    "Турель": ["Турель открывает шквальный огонь! -25HP", "Турель прошивает броню очередью! -25HP"],
    "Киборг": ["Киборг наносит удар стальным кулаком! -25HP", "Киборг атакует встроенным лезвием! -25HP"],
    "Терминатор": ["Терминатор ведет огонь на поражение! -25HP", "Терминатор идет напролом! -25HP"],
    "Лазер-волк": ["Лазер-волк прожигает обшивку лучом! -25HP", "Лазер-волк впивается челюстями! -25HP"],
    "Наемник": ["Наемник делает точный выстрел! -25HP", "Наемник бросает боевую гранату! -25HP"],
    "Боевой мех": ["Боевой мех дает залп из ракетниц! -50HP", "Боевой мех накрывает зону огнем! -50HP"],
    "Дрон-штурм": ["Штурмовой дрон сбрасывает заряд! -50HP", "Штурмовой дрон расстреливает из пушек! -50HP"],
    "Броневик": ["Броневик идет на таран! -50HP", "Броневик бьет прямой наводкой! -50HP"],
    "Паук-танк": ["Паук-танк палит из всех стволов! -50HP", "Паук-танк сокрушает укрытие! -50HP"],
    "ИИ": ["ИИ выжигает ваш мозг через сеть! -100HP", "ИИ стирает вашу личность! -100HP"],
    "Техно-дракон": ["Техно-дракон изрыгает поток плазмы! -100HP", "Техно-дракон превращает вас в пепел! -100HP"],

    # Болото проклятых
    "Болотный полоз": ["Болотный полоз обвивает ноги и тянет в трясину! -25HP", "Ядовитый полоз кусает за руку! -25HP"],
    "Ведьма-трясина": ["Ведьма-трясина затягивает вас в болотную пучину! -25HP", "Ведьма насылает порчу, тело покрывается язвами! -25HP"],
    "Трясинный волк": ["Трясинный волк выпрыгивает из грязи! -25HP", "Трясинный волк впивается клыками! -25HP"],
    "Мокрый упырь": ["Мокрый упырь высасывает жизненные силы! -25HP", "Мокрый упырь хватает ледяной рукой! -25HP"],
    "Когтистая трясина": ["Когтистая трясина хватает щупальцами! -25HP", "Трясина утаскивает под воду с невероятной силой! -25HP"],
    "Болотный тролль": ["Болотный тролль сокрушает дубиной! -50HP", "Тролль топчет вас в грязи! -50HP"],
    "Грязевой голем": ["Грязевой голем обрушивается на вас глыбой земли! -50HP", "Голем раздавливает вас своей массой! -50HP"],
    "Леший": ["Леший ломает кости ветками-руками! -50HP", "Леший заманивает в чащу и теряет сознание! -50HP"],
    "Гигантская жаба": ["Гигантская жаба облизывает вас ядовитой слизью! -50HP", "Жаба пытается проглотить вас языком! -50HP"],
    "Мать трясин": ["Мать трясин поглощает вас в пучину гнева! -100HP", "Мать трясин насылает проклятие вековой грязи! -100HP"],
    "Болотный царь": ["Болотный царь поднимает всю трясину против вас! -100HP", "Царь болота сокрушает корнями тысячелетних деревьев! -100HP"],
    "Дух болота": ["Дух болота испепеляет призрачным огнём! -100HP", "Дух болота забирает вашу душу в вечную топь! -100HP"],

    # Грозовая бездна 
    "Грозовой страж": ["Грозовой страж обрушивает молнию! -25HP", "Страж бьёт электрическим копьём! -25HP"],
    "Плазменный хищник": ["Плазменный хищник прожигает броню! -25HP", "Хищник выстреливает плазменным шаром! -25HP"],
    "Штормовой дух": ["Штормовой дух парализует разрядом! -25HP", "Дух обрушивает ураганный ветер! -25HP"],
    "Электрический виверн": ["Электрический виверн бьёт хвостом с зарядом! -25HP", "Виверн выдыхает цепную молнию! -25HP"],
    "Грозовой дракон": ["Грозовой дракон испепеляет потоком молний! -50HP", "Дракон обрушивает небесный гнев! -50HP"],
    "Молниевый гигант": ["Молниевый гигант сокрушает землю ударом! -50HP", "Гигант мечет громовые копья! -50HP"],
    "Плазменный левиафан": ["Плазменный левиафан накрывает энергетическим полем! -50HP", "Левиафан испаряет всё вокруг плазмой! -50HP"],
    "Штормовой голем": ["Штормовой голем сминает броню! -50HP", "Голем создаёт смерч вокруг вас! -50HP"],
    "Повелитель молний": ["Повелитель молний призывает грозу с небес! -100HP", "Повелитель превращает вас в пепел ударом бога! -100HP"],
    "Буревой бог": ["Буревой бог сдувает вас ураганом! -100HP", "Буревой бог разрывает пространство громом! -100HP"],
    "Разрушитель небес": ["Разрушитель небес обрушивает на вас небо! -100HP", "Разрушитель испепеляет вселенским разрядом! -100HP"],

    # Инферно
    "Инфернальный страж": ["Инфернальный страж обжигает адским пламенем! -25HP", "Страж бьет огненным мечом! -25HP"],
    "Пожиратель углей": ["Пожиратель углей высасывает тепло из тела! -25HP", "Пожиратель обжигает раскалёнными углями! -25HP"],
    "Магматический элементаль": ["Магматический элементаль заливает лавой! -25HP", "Элементаль разрывается потоком магмы! -25HP"],
    "Демон-копьеносец": ["Демон пронзает адским копьём! -25HP", "Демон сжигает демоническим огнём! -25HP"],
    "Пламенный виверн": ["Пламенный виверн испепеляет крыльями! -25HP", "Виверн изрыгает огненный смерч! -25HP"],
    "Лавовый гигант": ["Лавовый гигант обрушивает кулак из камня! -50HP", "Гигант топчет вас расплавленной ногой! -50HP"],
    "Баларог": ["Баларог хлещет огненным бичом! -50HP", "Баларог испепеляет демоническим пламенем! -50HP"],
    "Пожиратель душ": ["Пожиратель душ вырывает вашу сущность! -50HP", "Пожиратель превращает вас в пепел изнутри! -50HP"],
    "Цербер": ["Цербер рвет вас тремя головами! -50HP", "Цербер выдыхает адское пламя! -50HP"],
    "Повелитель пламени": ["Повелитель пламени сжигает дотла! -100HP", "Повелитель призывает огненный дождь! -100HP"],
    "Адский дракон": ["Адский дракон испепеляет всё живое! -100HP", "Адский дракон обрушивает метеоритный дождь! -100HP"],
    "Ифрит-император": ["Ифрит-император взрывает пространство вокруг! -100HP", "Ифрит отправляет вас в адскую бездну! -100HP"],

    # Космическая пустошь
    "Космодесантник-отступник": ["Космодесантник расстреливает из болтера! -25HP", "Отступник разрывает цепным мечом! -25HP"],
    "Чёрный карлик": ["Чёрный карлик сжимает гравитацией! -25HP", "Карлик выбрасывает поток тёмной материи! -25HP"],
    "Гравитационный хищник": ["Гравитационный хищник раздавливает полем! -25HP", "Хищник создаёт чёрную микро-дыру! -25HP"],
    "Пожиратель энергии": ["Пожиратель высасывает энергию тела! -25HP", "Пожиратель оставляет вас без сил! -25HP"],
    "Звёздный левиафан": ["Звёздный левиафан проглатывает космической пастью! -50HP", "Левиафан сминает гравитационным полем! -50HP"],
    "Космический титан": ["Космический титан сокрушает планетарным ударом! -50HP", "Титан бросает в вас астероид! -50HP"],
    "Чёрная Дыра": ["Чёрная дыра разрывает пространство вокруг вас! -50HP", "Дыра засасывает вас в сингулярность! -50HP"],
    "Некро-колосс": ["Некро-колосс сминает вас костяными пальцами! -50HP", "Колосс выпускает волну некро-энергии! -50HP"],
    "Пожиратель галактик": ["Пожиратель галактик уничтожает реальность вокруг! -100HP", "Пожиратель стирает вас из существования! -100HP"],
    "Космический дракон": ["Космический дракон сжигает звёздным огнём! -100HP", "Дракон разрывает ткань пространства! -100HP"],
    "Властелин Пустоты": ["Властелин Пустоты отправляет вас в небытие! -100HP", "Властелин аннигилирует вашу материю! -100HP"],
}


CONTRATTACK_DAMAGE = {
    "Опасн": 25,
    "Тяжел": 50, 
    "Титан": 75
}

# HP животных
ANIMAL_HP = {
    "Мелочь": 1,
    "Средн": 1,
    "Опасн": 100,
    "Тяжел": 200,
    "Титан": 300
}

# Урон от провала подкрадывания
SNEAK_FAIL_DAMAGE = {
    "Средн": 20,
    "Опасн": 50,
    "Тяжел": 75,
    "Титан": 100
}

# Шанс убежать (игрок)
ESCAPE_CHANCES = {
    "Опасн": 100,
    "Тяжел": 75,
    "Титан": 10
}

# Шанс стаи для мелочи (25%)
PACK_CHANCE = 25
PACK_SIZE = (3, 4)  # от 3 до 4 особей

# Шанс успеха "Поймать стаю"
CATCH_PACK_SUCCESS_CHANCE = 25

# ================== НАГРАДЫ ЗА ПРЕСТИЖ ==================
PRESTIGE_REWARDS = {
    1: {
        "name": "🥉 Бронза",
        "reward_coins": 5000,
        "reward_exp": 2000,
        "bonus": {"exp_bonus": 5}
    },
    2: {
        "name": "🥈 Серебро",
        "reward_coins": 10000,
        "reward_exp": 5000,
        "bonus": {"coins_bonus": 10}
    },
    3: {
        "name": "🥇 Золото",
        "reward_coins": 25000,
        "reward_exp": 10000,
        "bonus": {"exp_bonus": 15, "coins_bonus": 10},
        "special": "golden_bullet:5"
    },
    4: {
        "name": "💎 Платина",
        "reward_coins": 50000,
        "reward_exp": 20000,
        "bonus": {"collectible_chance": 10}
    },
    5: {
        "name": "🔮 Сапфир",
        "reward_coins": 75000,
        "reward_exp": 30000,
        "bonus": {"titan_hit": 20},
        "special": "sapphire_sight"
    },
    6: {
        "name": "❄️ Кристалл",
        "reward_coins": 100000,
        "reward_exp": 40000,
        "bonus": {"discount": 15}
    },
    7: {
        "name": "🌙 Обсидиан",
        "reward_coins": 150000,
        "reward_exp": 50000,
        "bonus": {"healing_bonus": 25},
        "special": "obsidian_amulet"
    },
    8: {
        "name": "☀️ Аметист",
        "reward_coins": 200000,
        "reward_exp": 75000,
        "bonus": {"collectible_chance": 100}
    },
    9: {
        "name": "⭐ Топаз",
        "reward_coins": 300000,
        "reward_exp": 100000,
        "bonus": {"exp_bonus": 30, "coins_bonus": 20},
        "special": "topaz_heart"
    },
    10: {
        "name": "👑 Алмаз",
        "reward_coins": 500000,
        "reward_exp": 150000,
        "bonus": {"all_bonus": 50},
        "special": "imperial_crown"
    }
}

# ================== ДОСТИЖЕНИЯ ==================
ACHIEVEMENTS = {
    "🐇Зайчья шкура": {
        "description": "Убить 20 зайцев",
        "reward_coins": 500,
        "reward_exp": 1000,
        "title": "🐇 Зайцелов",
        "condition_type": "animal_kills",
        "condition_value": ("Заяц", 20)
    },
    "💎Титановый бог": {
        "description": "Убить 3 титана",
        "reward_coins": 10000,
        "reward_exp": 5000,
        "title": "🔪 Киллер",
        "condition_type": "titan_kills",
        "condition_value": 3
    },
    "🤑Богач": {
        "description": "Накопить 50,000 монет",
        "reward_coins": 10000,
        "reward_exp": 0,
        "title": "💰 Богач",
        "condition_type": "coins",
        "condition_value": 50000
    },
    "📚Коллекционер": {
        "description": "Убить 75 разных видов животных",
        "reward_coins": 15000,
        "reward_exp": 1500,
        "title": "📚 Коллекционер",
        "condition_type": "unique_animals",
        "condition_value": 75
    },
    "🔫Снайпер": {
        "description": "7 успешных выстрелов подряд без промаха",
        "reward_coins": 5000,
        "reward_exp": 350,
        "title": "🔫 Снайпер",
        "condition_type": "streak",
        "condition_value": 7
    },
    "💪 Здоровяк": {
        "description": "Иметь 200 максимального HP",
        "reward_coins": 2500,
        "reward_exp": 200,
        "title": "💪 Качок",
        "condition_type": "max_health",
        "condition_value": 200
    },
    "🛡️ Непробиваемый": {
        "description": "Выдержать 7 контратак подряд без лечения",
        "reward_coins": 5000,
        "reward_exp": 500,
        "title": "🛡️ Непробиваемый",
        "condition_type": "counterattack_streak",
        "condition_value": 7
    },
    "🏃 Мастер побега": {
        "description": "Убежать от 3 титанов подряд",
        "reward_coins": 20000,
        "reward_exp": 1500,
        "title": "👻 Призрак",
        "condition_type": "titan_escape_streak",
        "condition_value": 3
    },
    "💀 Смертник": {
        "description": "Умереть 15 раз",
        "reward_coins": 4000,
        "reward_exp": 1,
        "title": "🪖 Павший воин",
        "condition_type": "deaths",
        "condition_value": 15
    },
    "🎯 Ловец удачи": {
        "description": "Поймать тяжёлое животное в ловушку",
        "reward_coins": 4000,
        "reward_exp": 500,
        "title": "🎯 Счастливчик",
        "condition_type": "trap_heavy",
        "condition_value": 1
    },
    "🐟 Рыбак": {
        "description": "Использовать ловушки 30 дней подряд",
        "reward_coins": 8000,
        "reward_exp": 1000,
        "title": "🐟 Рыбак",
        "condition_type": "trap_days_streak",
        "condition_value": 30
    },
    "⚡ Быстрая рука": {
        "description": "Использовать хант 750 раз",
        "reward_coins": 7500,
        "reward_exp": 2000,
        "title": "⚡ Молния",
        "condition_type": "hunt_count",
        "condition_value": 750
    },
    "🎖️ Ветеран": {
        "description": "Достичь 500 уровня",
        "reward_coins": 25000,
        "reward_exp": 10000,
        "title": "🎖️ Ветеран охоты",
        "condition_type": "level",
        "condition_value": 500
    },
    "👑 Повелитель оружия": {
        "description": "Купить все виды оружия",
        "reward_coins": 100000,
        "reward_exp": 10000,
        "title": "🧝‍♂️ Оружейный маг",
        "condition_type": "all_weapons",
        "condition_value": 7
    },
    "🐏 Баран": {
        "description": "Убить 20 баранов",
        "reward_coins": 5000,
        "reward_exp": 2000,
        "title": "🐏 Баран",
        "condition_type": "animal_kills",
        "condition_value": ("Баран", 20)
    },
    "🦇 Упырь": {
        "description": "Убить 20 упырей",
        "reward_coins": 5000,
        "reward_exp": 2000,
        "title": "🦇 Упырь",
        "condition_type": "animal_kills",
        "condition_value": ("Упырь", 20)

    },
    "🦈 Акула": {
        "description": "Убить 10 акул",
        "reward_coins": 5000,
        "reward_exp": 2000,
        "title": "🦈 Акула",
        "condition_type": "animal_kills",
        "condition_value": ("Акула", 10)

    },
    "🏅Особые заслуги": {
        "description": "Выдаётся администратором за особые заслуги",
        "reward_coins": 10000,
        "reward_exp": 7500,
        "title": "💎 Уникальный",
        "condition_type": "animal_kills",
        "condition_value": ("ИИ", 99999)
    }
}

RANKS = {
    0: {"name": "🐣 Новичок", "bonus_exp": 0, "bonus_coins": 0},
    20: {"name": "🎯 Начинающий охотник", "bonus_exp": 1, "bonus_coins": 0},
    50: {"name": "🏹 Продвинутый охотник", "bonus_exp": 3, "bonus_coins": 0},
    100: {"name": "⚔️ Мастер охоты", "bonus_exp": 5, "bonus_coins": 2},
    250: {"name": "🐉 Легендарный охотник", "bonus_exp": 10, "bonus_coins": 5},
    500: {"name": "👑 Король зверей", "bonus_exp": 15, "bonus_coins": 8},
    1000: {"name": "✨ Божество охоты", "bonus_exp": 20, "bonus_coins": 10},
    3000: {"name": "🔥 Властелин дикой природы", "bonus_exp": 35, "bonus_coins": 15},
    5000: {"name": "🌌 Повелитель бездны", "bonus_exp": 50, "bonus_coins": 25},
    10000: {"name": "🪐 Межгалактический Хищник", "bonus_exp": 75, "bonus_coins": 50},
    50000: {"name": "♾️ Воплощение Смерти", "bonus_exp": 150, "bonus_coins": 100},
    100000: {"name": "👁️ Истинный Кошмар Мироздания", "bonus_exp": 400, "bonus_coins": 250}
}

PRESTIGES = {
    1: {"name": "🥉 Бронза", "requirements": {"level": 45, "kills": 150, "coins": 50000}},
    2: {"name": "🥈 Серебро", "requirements": {"level": 75, "kills": 250, "coins": 100000, "unique_animals": 15}},
    3: {"name": "🥇 Золото", "requirements": {"level": 150, "kills": 500, "coins": 200000, "titans": 1}},
    4: {"name": "💎 Платина", "requirements": {"level": 300, "kills": 750, "coins": 300000, "dangerous": 5}},
    5: {"name": "🔮 Сапфир", "requirements": {"level": 500, "kills": 1000, "coins": 400000, "titans": 3}},
    6: {"name": "❄️ Кристалл", "requirements": {"level": 1000, "kills": 1500, "coins": 500000, "arctic": 20}},
    7: {"name": "🌙 Обсидиан", "requirements": {"level": 2000, "kills": 2000, "coins": 750000, "all_locations": True}},
    8: {"name": "☀️ Аметист", "requirements": {"level": 3500, "kills": 3000, "coins": 1000000, "titans": 15}},
    9: {"name": "⭐ Топаз", "requirements": {"level": 7000, "kills": 5000, "coins": 2000000, "all_weapons": True}},
    10: {"name": "👑 Алмаз", "requirements": {"level": 20000, "kills": 10000, "coins": 5000000, "all_titans": 5}}
}

# ================== ЕЖЕДНЕВНАЯ СЕРИЯ ==================
DAILY_STREAK_REWARDS = {
    1: {"coins": 100, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    2: {"coins": 100, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    3: {"coins": 100, "exp": 50, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    4: {"coins": 150, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    5: {"coins": 150, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    6: {"coins": 200, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    7: {"coins": 300, "exp": 0, "item": "medkit", "status": None, "title": None, "quote": None, "artifact": None},
    8: {"coins": 200, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    9: {"coins": 200, "exp": 100, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    10: {"coins": 400, "exp": 0, "item": "golden_bullet", "status": None, "title": None, "quote": None, "artifact": None},
    11: {"coins": 250, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    12: {"coins": 250, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    13: {"coins": 250, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    14: {"coins": 250, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    15: {"coins": 500, "exp": 0, "item": "diamond_bullet", "status": None, "title": None, "quote": None, "artifact": None},
    16: {"coins": 300, "exp": 100, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    17: {"coins": 300, "exp": 100, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    18: {"coins": 300, "exp": 100, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    19: {"coins": 300, "exp": 100, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    20: {"coins": 600, "exp": 0, "item": "drone", "status": None, "title": None, "quote": None, "artifact": None},
    21: {"coins": 350, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    22: {"coins": 350, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    23: {"coins": 350, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    24: {"coins": 350, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    25: {"coins": 350, "exp": 0, "item": "energy_drink", "status": None, "title": None, "quote": None, "artifact": None},
    26: {"coins": 350, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    27: {"coins": 350, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    28: {"coins": 350, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    29: {"coins": 350, "exp": 0, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    30: {"coins": 1000, "exp": 500, "item": None, "status": "Пугает зверей 🏹", "title": None, "quote": None, "artifact": None},
    31: {"coins": 400, "exp": 150, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    32: {"coins": 400, "exp": 150, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    33: {"coins": 400, "exp": 150, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    34: {"coins": 400, "exp": 150, "item": "medkit", "status": None, "title": None, "quote": None, "artifact": None},
    35: {"coins": 400, "exp": 150, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    36: {"coins": 400, "exp": 150, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    37: {"coins": 400, "exp": 150, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    38: {"coins": 400, "exp": 150, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    39: {"coins": 400, "exp": 150, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    40: {"coins": 1200, "exp": 550, "item": "immortality_staff", "status": None, "title": None, "quote": None, "artifact": None},
    41: {"coins": 450, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    42: {"coins": 450, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    43: {"coins": 450, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    44: {"coins": 450, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    45: {"coins": 450, "exp": 200, "item": "ultra_drone", "status": None, "title": None, "quote": None, "artifact": None},
    46: {"coins": 450, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    47: {"coins": 450, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    48: {"coins": 450, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    49: {"coins": 450, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    50: {"coins": 2000, "exp": 750, "item": "medkit", "status": None, "title": "🎉50🎁50🎂50", "quote": None, "artifact": None, "extra_items": ["golden_bullet"]},
    51: {"coins": 500, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    52: {"coins": 500, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    53: {"coins": 500, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    54: {"coins": 500, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    55: {"coins": 500, "exp": 200, "item": "golden_bullet", "status": None, "title": None, "quote": None, "artifact": None},
    56: {"coins": 500, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    57: {"coins": 500, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    58: {"coins": 500, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    59: {"coins": 500, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    60: {"coins": 2500, "exp": 100, "item": "diamond_bullet", "status": None, "title": None, "quote": None, "artifact": None, "extra_items": ["drone"]},
    61: {"coins": 550, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    62: {"coins": 550, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    63: {"coins": 550, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    64: {"coins": 550, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    65: {"coins": 550, "exp": 200, "item": "energy_drink", "status": None, "title": None, "quote": None, "artifact": None},
    66: {"coins": 550, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    67: {"coins": 550, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    68: {"coins": 550, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    69: {"coins": 550, "exp": 200, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    70: {"coins": 3000, "exp": 1250, "item": "immortality_staff", "status": None, "title": None, "quote": None, "artifact": None, "extra_items": ["medkit"]},
    71: {"coins": 600, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    72: {"coins": 600, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    73: {"coins": 600, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    74: {"coins": 600, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    75: {"coins": 600, "exp": 250, "item": "ultra_drone", "status": None, "title": None, "quote": None, "artifact": None},
    76: {"coins": 600, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    77: {"coins": 600, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    78: {"coins": 600, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    79: {"coins": 600, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    80: {"coins": 3500, "exp": 1500, "item": "golden_bullet", "status": None, "title": None, "quote": None, "artifact": None, "extra_items": ["diamond_bullet"]},
    81: {"coins": 650, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    82: {"coins": 650, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    83: {"coins": 650, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    84: {"coins": 650, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    85: {"coins": 650, "exp": 250, "item": "medkit", "status": None, "title": None, "quote": None, "artifact": None},
    86: {"coins": 650, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    87: {"coins": 650, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    88: {"coins": 650, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    89: {"coins": 650, "exp": 250, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    90: {"coins": 4000, "exp": 1750, "item": "drone", "status": None, "title": None, "quote": None, "artifact": None, "extra_items": ["immortality_staff"]},
    91: {"coins": 700, "exp": 300, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    92: {"coins": 700, "exp": 300, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    93: {"coins": 700, "exp": 300, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    94: {"coins": 700, "exp": 300, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    95: {"coins": 700, "exp": 300, "item": "energy_drink", "status": None, "title": None, "quote": None, "artifact": None},
    96: {"coins": 700, "exp": 300, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    97: {"coins": 700, "exp": 300, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    98: {"coins": 700, "exp": 300, "item": None, "status": None, "title": None, "quote": None, "artifact": None},
    99: {"coins": 7000, "exp": 2000, "item": None, "status": "Выживает 99 ночей в тёмном лесу 🌲", "title": None, "quote": None, "artifact": None},
    100: {"coins": 2000, "exp": 5000, "item": None, "status": None, "title": None, "quote": "100 дней я учился стрелять. 100 дней звери учились убегать. По крайней мере, мне так казалось", "artifact": "dragon_blood"}
}

# ================== БАЗА ДАННЫХ ==================
import threading

_thread_local = threading.local()

def get_db():
    """Получить соединение с БД для текущего потока"""
    if not hasattr(_thread_local, 'db'):
        _thread_local.db = sqlite3.connect("hunt.db", check_same_thread=False, isolation_level=None)
        _thread_local.db.row_factory = sqlite3.Row
    return _thread_local.db

def get_cursor():
    """Получить курсор для текущего потока"""
    return get_db().cursor()

# Для обратной совместимости, но НЕ ИСПОЛЬЗУЙТЕ глобальный sql!
db = get_db()
sql = get_cursor()

def get_db_connection():
    """Создает новое соединение с БД"""
    conn = sqlite3.connect("hunt.db")
    return conn, conn.cursor()

# Создание таблиц с полной структурой
sql.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    coins INTEGER DEFAULT 0,
    exp INTEGER DEFAULT 0,
    weapon TEXT DEFAULT 'Револьвер',
    location TEXT DEFAULT 'Тайга',
    last_hunt INTEGER DEFAULT 0,
    daily_kills INTEGER DEFAULT 0,
    total_kills INTEGER DEFAULT 0,
    username TEXT,
    current_title TEXT DEFAULT '',
    prestige INTEGER DEFAULT 0,
    achievement_streak INTEGER DEFAULT 0,
    achievements_completed TEXT DEFAULT '{}',
    health INTEGER DEFAULT 150,
    max_health INTEGER DEFAULT 150,
    deaths INTEGER DEFAULT 0,
    counterattack_streak INTEGER DEFAULT 0,
    titan_escape_streak INTEGER DEFAULT 0,
    trap_days_streak INTEGER DEFAULT 0,
    last_trap_use INTEGER DEFAULT 0,
    traps_used INTEGER DEFAULT 0,
    heavy_traps INTEGER DEFAULT 0,
    last_achievement_check INTEGER DEFAULT 0,
    golden_bullet INTEGER DEFAULT 0,
    drone_target TEXT DEFAULT '',
    drone_expires INTEGER DEFAULT 0,
    last_daily_gift INTEGER DEFAULT 0,
    survival_hunt_count INTEGER DEFAULT 0,
    survival_damage_count INTEGER DEFAULT 0,
    diamond_bullet INTEGER DEFAULT 0,
    immortality_staff INTEGER DEFAULT 0,
    energy_drink INTEGER DEFAULT 0,
    hunt_counter INTEGER DEFAULT 0,
    event_eggs INTEGER DEFAULT 0,
    event_quest INTEGER DEFAULT 0,
    event_egg_claim INTEGER DEFAULT 0,
    no_cooldown_charges INTEGER DEFAULT 0
)
""")

sql.execute("""
CREATE TABLE IF NOT EXISTS trophies (
    user_id INTEGER,
    animal TEXT,
    count INTEGER DEFAULT 0,
    UNIQUE(user_id, animal),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

sql.execute("""
CREATE TABLE IF NOT EXISTS user_weapons (
    user_id INTEGER,
    weapon TEXT,
    UNIQUE(user_id, weapon),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

sql.execute("""
CREATE TABLE IF NOT EXISTS user_equipment (
    user_id INTEGER,
    equipment TEXT,
    UNIQUE(user_id, equipment),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

sql.execute("""
CREATE TABLE IF NOT EXISTS stats_daily (
    user_id INTEGER,
    date TEXT,
    kills INTEGER DEFAULT 0,
    UNIQUE(user_id, date),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

sql.execute("""
CREATE TABLE IF NOT EXISTS survival_items (
    user_id INTEGER,
    item_name TEXT,
    location TEXT,
    UNIQUE(user_id, item_name),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для топа ивента
sql.execute("""
CREATE TABLE IF NOT EXISTS event_top (
    user_id INTEGER,
    eggs INTEGER DEFAULT 0,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для статистики убийств по локациям
sql.execute("""
CREATE TABLE IF NOT EXISTS location_stats (
    user_id INTEGER,
    location TEXT,
    kills INTEGER DEFAULT 0,
    UNIQUE(user_id, location),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для достижений локаций
sql.execute("""
CREATE TABLE IF NOT EXISTS location_achievements (
    user_id INTEGER,
    location TEXT,
    achievement_type TEXT,
    completed INTEGER DEFAULT 0,
    completed_at INTEGER DEFAULT 0,
    UNIQUE(user_id, location, achievement_type),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для мутаций в трофеях
sql.execute("""
CREATE TABLE IF NOT EXISTS trophy_mutations (
    user_id INTEGER,
    animal TEXT,
    mutation TEXT,
    count INTEGER DEFAULT 0,
    UNIQUE(user_id, animal, mutation),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для цитат
sql.execute("""
CREATE TABLE IF NOT EXISTS user_quotes (
    user_id INTEGER,
    quote_id TEXT,
    quote_text TEXT,
    UNIQUE(user_id, quote_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для временных данных охоты (решение проблемы BUTTON_DATA_INVALID)
sql.execute("""
CREATE TABLE IF NOT EXISTS temp_hunt (
    hunt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    group_name TEXT,
    animal_id TEXT,
    mutation TEXT,
    created_at INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для коротких ID животных (добавить в создание таблиц)
sql.execute("""
CREATE TABLE IF NOT EXISTS animal_ids (
    animal_id TEXT PRIMARY KEY,
    location TEXT,
    group_name TEXT,
    animal TEXT
)
""")

sql.execute("""
CREATE TABLE IF NOT EXISTS user_buffs (
    user_id INTEGER,
    buff_name TEXT,
    count INTEGER DEFAULT 0,
    UNIQUE(user_id, buff_name),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")
db.commit()

# Добавьте в раздел создания таблиц (после других CREATE TABLE)
sql.execute("""
CREATE TABLE IF NOT EXISTS temp_shop_data (
    user_id INTEGER,
    data_type TEXT,
    data_key TEXT,
    data_value TEXT,
    created_at INTEGER,
    PRIMARY KEY (user_id, data_type, data_key)
)
""")
db.commit()

# Таблица для коллекционных предметов
sql.execute("""
CREATE TABLE IF NOT EXISTS user_collectibles (
    user_id INTEGER,
    location TEXT,
    group_name TEXT,
    item_name TEXT,
    count INTEGER DEFAULT 0,
    UNIQUE(user_id, location, group_name, item_name),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для разблокированных скинов профиля
sql.execute("""
CREATE TABLE IF NOT EXISTS user_themes (
    user_id INTEGER,
    theme_name TEXT,
    unlocked INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, theme_name),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для активного боя
sql.execute("""
CREATE TABLE IF NOT EXISTS battle_state (
    user_id INTEGER PRIMARY KEY,
    animal_id TEXT,
    animal_name TEXT,
    group_name TEXT,
    animal_hp INTEGER,
    animal_max_hp INTEGER,
    is_pack BOOLEAN DEFAULT 0,
    pack_size INTEGER DEFAULT 1,
    ability_used BOOLEAN DEFAULT 0,
    turn INTEGER DEFAULT 0,
    sneak_bonus INTEGER DEFAULT 0,
    created_at INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для эффектов в бою (замедление, отравление и т.д.)
sql.execute("""
CREATE TABLE IF NOT EXISTS battle_effects (
    user_id INTEGER,
    effect_name TEXT,
    duration INTEGER,
    value INTEGER,
    PRIMARY KEY (user_id, effect_name),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для модификаторов боя (бонусы от подкрадывания и т.д.)
sql.execute("""
CREATE TABLE IF NOT EXISTS battle_mods (
    user_id INTEGER PRIMARY KEY,
    hit_bonus INTEGER DEFAULT 0,
    damage_bonus INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица для хранения принудительного животного
sql.execute("""
CREATE TABLE IF NOT EXISTS admin_forced_animal (
    user_id INTEGER PRIMARY KEY,
    animal_name TEXT,
    enabled INTEGER DEFAULT 0
)
""")
db.commit()


# ================== АВТОМАТИЧЕСКОЕ ВОССТАНОВЛЕНИЕ HP ==================
class HealthRegenerator:
    """Класс для автоматического восстановления здоровья"""
    
    def __init__(self):
        self.is_running = False
        self.regeneration_thread = None
    
    def start_regeneration(self):
        """Запуск потока восстановления здоровья"""
        if self.is_running:
            return
        
        self.is_running = True
        self.regeneration_thread = threading.Thread(target=self._regeneration_loop, daemon=True)
        self.regeneration_thread.start()
        print("🩺 Автоматическое восстановление HP запущено")
    
    def stop_regeneration(self):
        """Остановка восстановления здоровья"""
        self.is_running = False
        if self.regeneration_thread:
            self.regeneration_thread.join(timeout=2)
        print("🩺 Автоматическое восстановление HP остановлено")
    
    def _regeneration_loop(self):
        """Основной цикл восстановления здоровья"""
        while self.is_running:
            try:
                self._regenerate_all_players()
                time.sleep(60)  # Ждем 1 минуту
            except Exception as e:
                print(f"❌ Ошибка в восстановлении HP: {e}")
                time.sleep(60)
    
    def _regenerate_all_players(self):
        try:
            all_users = sql.execute("SELECT user_id, health, max_health, was_dead FROM users").fetchall()
            
            for user in all_users:
                user_id, current_hp, max_hp, was_dead = user
                
                # Скорость восстановления: 1% от макс HP в минуту
                healing_rate = max(1, int(max_hp * 0.01))
                
                equipment = get_user_equipment(user_id)
                if "Витамины" in equipment:
                    healing_rate = int(healing_rate * 1.5)
                
                if current_hp < max_hp:
                    new_hp = current_hp + healing_rate
                    if new_hp > max_hp:
                        new_hp = max_hp
                    
                    sql.execute("UPDATE users SET health = ? WHERE user_id = ?", (new_hp, user_id))
                    
                    # Если восстановились до 150+ и были мертвы - снимаем флаг
                    if was_dead == 1 and new_hp >= 150:
                        sql.execute("UPDATE users SET was_dead = 0 WHERE user_id = ?", (user_id,))
                        print(f"💚 Игрок {user_id} восстановился после смерти")
            
            db.commit()
        except Exception as e:
            print(f"❌ Ошибка при восстановлении HP: {e}")
            db.rollback()

# Создаем экземпляр восстановителя здоровья
health_regenerator = HealthRegenerator()

# ================== ФУНКЦИИ ==================
def get_level(exp: int) -> int:
    return exp // EXP_PER_LEVEL

def get_streak_emoji(streak: int) -> str:
    """Возвращает эмодзи в зависимости от дня серии"""
    if streak <= 10:
        return "🌱"
    elif streak <= 20:
        return "⭐"
    elif streak <= 30:
        return "⚡"
    elif streak <= 50:
        return "🔥"
    elif streak <= 70:
        return "🪙"
    elif streak <= 99:
        return "🐉"
    elif streak <= 200:
        return "👑"
    elif streak <= 500:
        return "💎"
    elif streak <= 999:
        return "🌌"
    else:
        return "♾️"

def log_error_detailed(error: Exception, context: str = ""):
    """Подробное логирование ошибки с выводом в консоль"""
    error_type = type(error).__name__
    error_msg = str(error)
    
    # Получаем полный traceback
    tb = traceback.format_exc()
    
    print("\n" + "="*80)
    print(f"🔴 ОШИБКА в {context}")
    print(f"📌 Тип: {error_type}")
    print(f"📌 Сообщение: {error_msg}")
    print(f"\n📌 Полный traceback:\n{tb}")
    print("="*80 + "\n")
    
    # Также пишем в файл
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Контекст: {context}\n")
        f.write(f"Тип: {error_type}\n")
        f.write(f"Сообщение: {error_msg}\n")
        f.write(f"Traceback:\n{tb}\n")

def get_animal_mutation(user_id=None):
    """Возвращает название мутации и её данные. Если обычный — (None, None)"""
    # Базовая логика шансов
    if user_id:
        # Проверяем наличие артефакта "Драконья кровь"
        has_dragon_blood = sql.execute("SELECT 1 FROM user_equipment WHERE user_id = ? AND equipment = ?", 
                                       (user_id, "🐉 Драконья кровь")).fetchone()
        if has_dragon_blood:
            # Увеличенные шансы
            MUTATIONS_MOD = {
                "🔥Гигант": {"chance": 20, "coins_mult": 1.5, "exp_mult": 1.0},
                "🤍Альбинос": {"chance": 10, "coins_mult": 1.0, "exp_mult": 7.0},
                "👑Вожак": {"chance": 3, "coins_mult": 3.0, "exp_mult": 12.0}
            }
        else:
            MUTATIONS_MOD = MUTATIONS
    else:
        MUTATIONS_MOD = MUTATIONS
    
    rand = random.randint(1, 100)
    cumulative = 0
    for mut_name, mut_data in MUTATIONS_MOD.items():
        cumulative += mut_data["chance"]
        if rand <= cumulative:
            return mut_name, mut_data
    return None, None

# def migrate_old_trophies():
 #   """Переносит старые трофеи в location_stats и trophy_mutations"""
 #   print("🔄 Перенос старых трофеев...")
    
    # Получаем всех пользователей ДО начала цикла
    #users = sql.execute("SELECT user_id FROM users").fetchall()
  #
   # for (user_id,) in users:
        # Получаем трофеи пользователя
       # trophies = sql.execute("SELECT animal, count FROM trophies WHERE user_id = ?", (user_id,)).fetchall()
        
        # ВРЕМЕННЫЙ СЛОВАРЬ для локаций
      #  location_kills_temp = {}
        
        #for animal, count in trophies:
            # Определяем локацию животного
          #  location = None
           # for loc_name, loc_data in LOCATIONS.items():
              #  for group_animals in loc_data["animals"].values():
                 #   if animal in group_animals:
                   #     location = loc_name
                    #    break
             #   if location:
             #       break
            
            ##if location:
            #    location_kills_temp[location] = location_kills_temp.get(location, 0) + count
        
        # Сохраняем в location_stats
      #  for location, kills in location_kills_temp.items():
         #   existing = sql.execute("SELECT kills FROM location_stats WHERE user_id = ? AND location = ?", 
                         #          (user_id, location)).fetchone()
          #  if existing:
             #   sql.execute("UPDATE location_stats SET kills = kills + ? WHERE user_id = ? AND location = ?",
                         #  (kills, user_id, location))
          #  else:
              #  sql.execute("INSERT INTO location_stats (user_id, location, kills) VALUES (?, ?, ?)",
                      #     (user_id, location, kills))
        
        # Перенос мутаций (пока нет данных, просто создаём структуру)
        # Мутации будем заполнять при следующих убийствах
    
  #  db.commit()
   # print("✅ Перенос старых трофеев завершён!")

import hashlib

def has_survival_item(user_id: int, location: str):
    """Проверить, есть ли у игрока предмет выживания для локации"""
    survival_items = get_user_survival_items(user_id)
    
    for item_name in survival_items:
        if item_name in SURVIVAL_ITEMS and SURVIVAL_ITEMS[item_name].get("location") == location:
            if SURVIVAL_ITEMS[item_name].get("survival", False):
                return True, item_name
    
    return False, None
    
def get_short_animal_id(location: str, group: str, animal: str) -> str:
    """Генерирует короткий 8-символьный ID для животного"""
    data = f"{location}|{group}|{animal}"
    return hashlib.md5(data.encode()).hexdigest()[:8]

def get_animal_by_id(animal_id: str):
    """Возвращает животное по ID"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    result = cur.execute(
        "SELECT location, group_name, animal FROM animal_ids WHERE animal_id = ?",
        (animal_id,)
    ).fetchone()
    conn.close()
    if result:
        return {"location": result[0], "group": result[1], "animal": result[2]}
    return None

def ensure_user(user_id: int, username: str = None):
    """Безопасная версия - всегда использует НОВОЕ соединение"""
    conn = None
    try:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        
        # Проверяем существование всех нужных колонок
        columns = [
            "daily_streak", "last_daily_claim", "current_status", "current_quote",
            "profile_theme", "was_dead", "no_cooldown_charges"
        ]
        
        for col in columns:
            try:
                cur.execute(f"SELECT {col} FROM users LIMIT 1")
            except sqlite3.OperationalError:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col} DEFAULT 0")
                conn.commit()
                print(f"✅ Добавлена колонка {col}")
        
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cur.fetchone()
        
        if not user:
            cur.execute("""
                INSERT INTO users 
                (user_id, username, coins, exp, weapon, location, last_hunt, 
                 daily_kills, total_kills, current_title, prestige, 
                 achievement_streak, achievements_completed, health, max_health,
                 deaths, counterattack_streak, titan_escape_streak, trap_days_streak,
                 last_trap_use, traps_used, heavy_traps, last_achievement_check,
                 golden_bullet, drone_target, drone_expires, last_daily_gift,
                 survival_hunt_count, survival_damage_count, diamond_bullet,
                 immortality_staff, energy_drink, hunt_counter, event_eggs, 
                 event_quest, event_egg_claim, daily_streak, last_daily_claim,
                 current_status, current_quote, profile_theme, was_dead, no_cooldown_charges) 
                VALUES (?, ?, 0, 0, 'Револьвер', 'Тайга', 0, 0, 0, '', 0, 0, '{}', 
                        150, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 
                        0, 0, 0, 0, 0, 0, 'На охоте🏹', 
                        'Я начинающий охотник, и я иду к своей цели', 'standard', 0, 0)""",
                (user_id, username)
            )
            cur.execute("INSERT OR IGNORE INTO user_weapons VALUES (?, ?)", (user_id, "Револьвер"))
            conn.commit()
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cur.fetchone()
        elif username and user[8] != username:
            cur.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
            conn.commit()
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cur.fetchone()
        
        return user
    except Exception as e:
        print(f"Ошибка в ensure_user: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if conn:
            conn.close()

def get_user_health(user_id: int):
    """Получить текущее и максимальное здоровье игрока"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    user = cur.execute("SELECT health, max_health FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return user[0], user[1]
    return 150, 150

def update_health(user_id: int, change: int):
    """Изменить здоровье игрока (может быть отрицательным) - БЕЗ рекурсивных курсоров"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    
    # Получаем текущие данные
    user_data = cur.execute("SELECT health, max_health, immortality_staff FROM users WHERE user_id = ?", (user_id,)).fetchone()
    
    if not user_data:
        conn.close()
        return 0
    
    current_hp, max_hp, immortality = user_data
    
    new_hp = current_hp + change
    
    # Проверяем бессмертие
    if change < 0 and immortality == 1:
        cur.execute("UPDATE users SET immortality_staff = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return current_hp
    
    if new_hp > max_hp:
        new_hp = max_hp
    
    # При смерти: HP = 0, ставим флаг was_dead = 1
    if new_hp <= 0:
        new_hp = 0
        cur.execute("UPDATE users SET health = ?, was_dead = 1 WHERE user_id = ?", (new_hp, user_id))
    else:
        cur.execute("UPDATE users SET health = ? WHERE user_id = ?", (new_hp, user_id))
    
    conn.commit()
    conn.close()
    return new_hp

def heal_user(user_id: int, amount: int = None):
    """Вылечить игрока"""
    user = ensure_user(user_id)
    max_hp = user[14]
    current_hp = user[13]
    
    if amount is None:
        # Полное лечение
        sql.execute("UPDATE users SET health = ? WHERE user_id = ?", (max_hp, user_id))
    else:
        # Лечение на указанное количество (аптечка = 50)
        new_hp = current_hp + amount
        if new_hp > max_hp:
            new_hp = max_hp
        sql.execute("UPDATE users SET health = ? WHERE user_id = ?", (new_hp, user_id))
    
    db.commit()

def can_hunt(user_id: int) -> tuple:
    """Проверить, может ли игрок охотиться"""
    try:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        result = cur.execute("SELECT health, max_health, was_dead FROM users WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        
        if not result:
            return True, "✅ Можно охотиться"
        
        current_hp, max_hp, was_dead = result
        
        # Если игрок не умирал - можно охотиться с любым HP (хоть 1)
        if was_dead == 0 or was_dead is None:
            return True, "✅ Можно охотиться"
        
        # Если умирал - нужно восстановиться до 150 HP
        if current_hp < 150:
            need = 150 - current_hp
            healing_rate = max(1, int(max_hp * 0.01))
            minutes = int(need / healing_rate) + (1 if need % healing_rate > 0 else 0)
            return False, f"💀 **После смерти нужно восстановиться до 150 HP!**\n\n❤️ Сейчас: {current_hp}/{max_hp}\n📈 Нужно: {need} HP\n⏳ Примерно через {minutes} мин"
        
        # Достиг 150 - снимаем флаг смерти
        cur2 = get_cursor()
        cur2.execute("UPDATE users SET was_dead = 0 WHERE user_id = ?", (user_id,))
        db.commit()
        return True, "✅ Можно охотиться"
        
    except Exception as e:
        print(f"Ошибка can_hunt: {e}")
        return True, "✅ Можно охотиться"

def can_hunt_after_death(user_id: int) -> tuple:
    """Проверить, может ли игрок охотиться (учитывая порог после смерти)"""
    try:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        result = cur.execute("SELECT health, max_health, was_dead FROM users WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        
        if not result:
            return True, "✅ Можно охотиться"
        
        current_hp, max_hp, was_dead = result
        
        if was_dead == 0:
            return True, "✅ Можно охотиться"
        
        if current_hp < 150:
            need = 150 - current_hp
            healing_rate = max(1, int(max_hp * 0.01))
            minutes = int(need / healing_rate)
            return False, f"💀 После смерти нужно восстановиться до 150 HP.\n❤️ Сейчас: {current_hp}/{max_hp}\n📈 Нужно восстановить: {need} HP\n🕐 Примерно через {minutes} мин"
        
        return True, "✅ Можно охотиться"
    except Exception as e:
        print(f"Ошибка can_hunt_after_death: {e}")
        return True, "✅ Можно охотиться"


def get_current_animal_hp(user_id: int) -> int:
    """Получить текущее HP животного из БД"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    result = cur.execute("SELECT animal_hp FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return result[0] if result else 0


def get_weapon_location_bonus(weapon_name: str, location: str) -> dict:
    weapon_group = get_weapon_group(weapon_name)
    weakness = LOCATION_WEAPON_WEAKNESS.get(location, {"love": [], "hate": []})
    if weapon_group in weakness.get("love", []):
        return WEAPON_LOCATION_BONUS["love"].copy()
    elif weapon_group in weakness.get("hate", []):
        return WEAPON_LOCATION_BONUS["hate"].copy()
    return {"hit": 0, "damage": 0, "coins": 0, "exp": 0}

def get_user_equipment(user_id: int):
    """Получить снаряжение игрока (безопасная версия)"""
    try:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        equipment = cur.execute(
            "SELECT equipment FROM user_equipment WHERE user_id = ?", 
            (user_id,)
        ).fetchall()
        conn.close()
        return [eq[0] for eq in equipment]
    except Exception as e:
        print(f"Ошибка get_user_equipment: {e}")
        return []

async def refresh_buffs_menu(call: CallbackQuery):
    """Обновить меню баффов"""
    user_id = call.from_user.id
    user_buffs = get_user_buffs(user_id)
    
    # Фильтруем только баффы с количеством > 0
    user_buffs = {name: count for name, count in user_buffs.items() if count > 0}
    
    if not user_buffs:
        await call.message.edit_text("📦 У вас нет купленных баффов.\n\nКупить их можно в магазине → ⚡ Баффы")
        return
    
    buttons = []
    for buff_name, count in user_buffs.items():
        buttons.append([InlineKeyboardButton(
            text=f"{buff_name} x{count}",
            callback_data=f"activate_buff:{user_id}:{buff_name}"
        )])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text("📦 **Ваши баффы:**\n\nНажмите на бафф, чтобы активировать.", reply_markup=kb, parse_mode="Markdown")


def add_user_buff(user_id: int, buff_name: str, count: int = 1):
    """Добавляет бафф в инвентарь игрока"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_buffs (user_id, buff_name, count) 
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, buff_name) DO UPDATE SET count = count + ?
    """, (user_id, buff_name, count, count))
    conn.commit()
    conn.close()

def remove_user_buff(user_id: int, buff_name: str, count: int = 1):
    """Удаляет бафф из инвентаря (при активации)"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_buffs SET count = count - ? 
        WHERE user_id = ? AND buff_name = ? AND count > 0
    """, (count, user_id, buff_name))
    conn.commit()
    conn.close()

def get_user_buffs(user_id: int) -> dict:
    """Возвращает словарь {название_баффа: количество}"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    result = cur.execute("SELECT buff_name, count FROM user_buffs WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return {row[0]: row[1] for row in result}

# ================== КОЛЛЕКЦИОННЫЕ ПРЕДМЕТЫ ==================
def get_user_collectibles(user_id: int, location: str = None) -> dict:
    """Получить коллекционные предметы игрока"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    
    if location:
        result = cur.execute(
            "SELECT group_name, item_name, count FROM user_collectibles WHERE user_id = ? AND location = ?",
            (user_id, location)
        ).fetchall()
    else:
        result = cur.execute(
            "SELECT location, group_name, item_name, count FROM user_collectibles WHERE user_id = ?",
            (user_id,)
        ).fetchall()
    
    conn.close()
    
    # Формируем словарь для удобного доступа
    collectibles = {}
    for row in result:
        if location:
            group, item, count = row
            if group not in collectibles:
                collectibles[group] = {}
            collectibles[group][item] = count
        else:
            loc, group, item, count = row
            if loc not in collectibles:
                collectibles[loc] = {}
            if group not in collectibles[loc]:
                collectibles[loc][group] = {}
            collectibles[loc][group][item] = count
    
    return collectibles

def add_collectible(user_id: int, location: str, group: str, item_name: str):
    """Добавить коллекционный предмет (или увеличить счётчик)"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO user_collectibles (user_id, location, group_name, item_name, count)
        VALUES (?, ?, ?, ?, 1)
        ON CONFLICT(user_id, location, group_name, item_name)
        DO UPDATE SET count = count + 1
    """, (user_id, location, group, item_name))
    
    conn.commit()
    conn.close()
    
    # Проверяем, не собрал ли игрок все 10 предметов в локации
    check_full_collection(user_id, location)

def check_full_collection(user_id: int, location: str):
    """Проверить, собраны ли все 10 предметов в локации, и выдать награду"""
    # Получаем все предметы игрока в этой локации
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    
    result = cur.execute(
        "SELECT COUNT(DISTINCT item_name) FROM user_collectibles WHERE user_id = ? AND location = ?",
        (user_id, location)
    ).fetchone()
    
    collected_count = result[0] if result else 0
    
    # Всего предметов в локации: 5 групп × 2 предмета = 10
    if collected_count >= 10:
        # Проверяем, не выдано ли уже достижение
        existing = cur.execute(
            "SELECT 1 FROM location_achievements WHERE user_id = ? AND location = ? AND achievement_type = 'full_collection'",
            (user_id, location)
        ).fetchone()
        
        if not existing:
            # Выдаём награду за полную коллекцию
            # Награда: 5000 монет, 1000 опыта
            cur.execute("UPDATE users SET coins = coins + 5000, exp = exp + 1000 WHERE user_id = ?", (user_id,))
            
            # Записываем достижение
            cur.execute("""
                INSERT INTO location_achievements (user_id, location, achievement_type, completed, completed_at)
                VALUES (?, ?, 'full_collection', 1, ?)
            """, (user_id, location, int(time.time())))
            
            conn.commit()
            
            # Разблокируем скин профиля (добавим позже)
            # Здесь просто запомним, что скин разблокирован
            cur.execute("""
                INSERT OR REPLACE INTO user_themes (user_id, theme_name, unlocked)
                VALUES (?, ?, 1)
            """, (user_id, location.lower()))
            conn.commit()
            
            # Уведомление будет отправлено в месте вызова
    
    conn.close()

def get_collection_progress(user_id: int, location: str) -> tuple:
    """Получить прогресс коллекции: (собрано_предметов, всего_предметов)"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    
    result = cur.execute(
        "SELECT COUNT(DISTINCT item_name) FROM user_collectibles WHERE user_id = ? AND location = ?",
        (user_id, location)
    ).fetchone()
    
    collected = result[0] if result else 0
    conn.close()
    
    return collected, 10  # всего 10 предметов в локации

def get_equipment_bonuses(user_id: int):
    equipment = get_user_equipment(user_id)
    bonuses = {"Мелочь": 0, "Средн": 0, "Опасн": 0, "Тяжел": 0, "Титан": 0}
    
    for eq_name in equipment:
        if eq_name in EQUIPMENT:
            for group, bonus in EQUIPMENT[eq_name].get("bonus", {}).items():
                if group in bonuses:
                    bonuses[group] += bonus
    return bonuses

def get_max_health_from_equipment(user_id: int):
    """Получить бонус к максимальному здоровью от снаряжения"""
    equipment = get_user_equipment(user_id)
    bonus_hp = 150  # базовое здоровье
    
    for eq_name in equipment:
        if eq_name in EQUIPMENT and "bonus" in EQUIPMENT[eq_name]:
            if "health" in EQUIPMENT[eq_name]["bonus"]:
                bonus_hp += EQUIPMENT[eq_name]["bonus"]["health"]
    
    return bonus_hp

def update_max_health(user_id: int):
    """Обновить максимальное здоровье на основе снаряжения"""
    new_max_hp = get_max_health_from_equipment(user_id)
    sql.execute("UPDATE users SET max_health = ? WHERE user_id = ?", (new_max_hp, user_id))
    
    current_hp, _ = get_user_health(user_id)
    if current_hp > new_max_hp:
        sql.execute("UPDATE users SET health = ? WHERE user_id = ?", (new_max_hp, user_id))
    
    db.commit()
    return new_max_hp

def choose_animal(location: str, user_id: int):
    # ===== ПРОВЕРКА ПРИНУДИТЕЛЬНОГО ЖИВОТНОГО =====
    forced = sql.execute(
        "SELECT animal_name FROM admin_forced_animal WHERE user_id = ? AND enabled = 1",
        (user_id,)
    ).fetchone()
    
    if forced:
        animal_name = forced[0]
        
        # Находим группу этого животного
        for loc_name, loc_data in LOCATIONS.items():
            for group_name, animals_list in loc_data["animals"].items():
                if animal_name in animals_list:
                    mutation_name, mutation_data = get_animal_mutation(user_id)
                    animal_id = get_short_animal_id(location, group_name, animal_name)
                    
                    sql.execute("""
                        INSERT OR REPLACE INTO animal_ids (animal_id, location, group_name, animal) 
                        VALUES (?, ?, ?, ?)
                    """, (animal_id, location, group_name, animal_name))
                    db.commit()
                    
                    return group_name, animal_name, mutation_name, animal_id
        
        # Если вдруг животное не найдено (не должно случиться)
        print(f"⚠️ Принудительное животное {animal_name} не найдено в локациях для user_id={user_id}")
        # Продолжаем обычный поиск
        
    available_groups = [g for g in SEARCH_CHANCES if LOCATIONS[location]["animals"].get(g) and LOCATIONS[location]["animals"][g]]
    if not available_groups:
            return None, None, None, None  # <--- 4 значения
    
    bonuses = get_equipment_bonuses(user_id)
    equipment = get_user_equipment(user_id)
    
    # Проверяем дрон-бонус
    user = ensure_user(user_id)
    drone_target = user[24] if len(user) > 24 else ''
    drone_expires = user[25] if len(user) > 25 else 0
    
    if drone_target and drone_expires > int(time.time()):
        # Проверяем, есть ли целевое животное в этой локации
        target_in_location = False
        target_group = None
        for group, animals in LOCATIONS[location]["animals"].items():
            if drone_target in animals:
                target_in_location = True
                target_group = group
                break
        
        if target_in_location:
            # Увеличиваем шанс найти целевое животное на 10%
            if random.randint(1, 100) <= 10:
                mutation_name, mutation_data = get_animal_mutation(user_id)
                animal_id = get_short_animal_id(location, target_group, drone_target)
                # Сохраняем ID в таблицу
                sql.execute("""
                    INSERT OR REPLACE INTO animal_ids (animal_id, location, group_name, animal) 
                    VALUES (?, ?, ?, ?)
                """, (animal_id, location, target_group, drone_target))
                db.commit()
                return target_group, drone_target, mutation_name, animal_id  # <--- 4 значения
    
    # Продвинутый искатель - гарантированно находим животное
    if "Продвинутый искатель" in equipment:
        group = random.choice(available_groups)
        animal = random.choice(LOCATIONS[location]["animals"][group])
        mutation_name, mutation_data = get_animal_mutation(user_id)
        animal_id = get_short_animal_id(location, group, animal)
        sql.execute("""
            INSERT OR REPLACE INTO animal_ids (animal_id, location, group_name, animal) 
            VALUES (?, ?, ?, ?)
        """, (animal_id, location, group, animal))
        db.commit()
        return group, animal, mutation_name, animal_id  # <--- 4 значения
    
         # Обычный поиск с учетом бонусов и погоды
    weights = []
    weather_effects = WEATHER_EFFECTS.get(current_weather, {})
    
    for g in available_groups:
        base_chance = SEARCH_CHANCES[g]
        bonus = bonuses.get(g, 0)
        
        # Добавляем бонус от погоды для поиска
        weather_bonus = 0
        if g == "Тяжел" and weather_effects.get("find_heavy", 0):
            weather_bonus = weather_effects["find_heavy"]
        elif g == "Опасн" and weather_effects.get("find_dangerous", 0):
            weather_bonus = weather_effects["find_dangerous"]
        
        # Ветер даёт общий бонус к поиску
        if weather_effects.get("search", 0):
            weather_bonus += weather_effects["search"]
        
        weights.append(base_chance + bonus + weather_bonus)
    
    group = random.choices(available_groups, weights=weights)[0]
    
    search_chance = SEARCH_CHANCES[group] + bonuses.get(group, 0)
    
    # Добавляем бонус погоды к поиску
    if weather_effects.get("search", 0):
        search_chance += weather_effects["search"]
    
    if random.randint(1, 100) > search_chance:
        return None, None, None, None  # <--- 4 значения, а не 3!
    
    animal = random.choice(LOCATIONS[location]["animals"][group])
    mutation_name, mutation_data = get_animal_mutation(user_id)
        # Генерируем короткий ID
    animal_id = get_short_animal_id(location, group, animal)
    
    # Сохраняем ID в таблицу
    sql.execute("""
        INSERT OR REPLACE INTO animal_ids (animal_id, location, group_name, animal) 
        VALUES (?, ?, ?, ?)
    """, (animal_id, location, group, animal))
    db.commit()
    
    return group, animal, mutation_name, animal_id

def check_hit(weapon: str, group: str, user_id: int = None, location: str = None):
    groups = ["Мелочь", "Средн", "Опасн", "Тяжел", "Титан"]
    if group not in groups:
        return False
    
    idx = groups.index(group)
    
    weapon_data = get_weapon_data(weapon)
    base_chance = weapon_data["chances"][idx]
    
    final_chance = base_chance
    
    # Погода
    weather_effects = WEATHER_EFFECTS.get(current_weather, {})
    hit_bonus = weather_effects.get("hit", 0)
    
    # Для тумана - отдельная логика
    if current_weather == "🌫️ Туманно":
        final_chance = final_chance * 0.9
    else:
        final_chance += hit_bonus
    
    # Бонус от локации
    if location:
        location_bonus = get_weapon_location_bonus(weapon, location)
        final_chance += location_bonus["hit"]
    
    # Баффы игрока
    if user_id:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        user_data = cur.execute("SELECT golden_bullet, diamond_bullet FROM users WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        
        if user_data:
            has_golden_bullet, has_diamond_bullet = user_data
            if has_golden_bullet and has_golden_bullet > 0:
                final_chance *= 2
            if has_diamond_bullet and has_diamond_bullet > 0:
                final_chance += 20
    
    # Ограничиваем шанс
    final_chance = max(1, min(99, final_chance))
    
    # ✅ ОТЛАДКА - выводим в консоль (можно убрать после проверки)
    print(f"[HIT] Оружие: {weapon}, Группа: {group}, Базовый шанс: {base_chance}%, Итоговый: {final_chance}%")
    
    # ✅ ИСПРАВЛЕНО: используем random.randint вместо uniform
    # random.randint(1, 100) даёт целые числа, что проще для отладки
    roll = random.randint(1, 100)
    result = roll <= final_chance
    
    print(f"[HIT] Выброшено: {roll}, Результат: {'ПОПАЛ' if result else 'ПРОМАХ'}")
    
    # ===== ПРОВЕРКА ПРОКЛЯТИЯ (curse_dark) =====
    effects = get_battle_effects(user_id)
    if "curse_dark" in effects:
        # Проклятие: следующий удар x2 урона (не влияет на шанс)
        pass  # Шанс не меняется, только урон
    
    # ===== ПРОВЕРКА ПРОКЛЯТИЯ ТИТАНА (curse) =====
    if "curse" in effects:
        final_chance = int(final_chance * (1 - effects["curse"]["value"] / 100))
        final_chance = max(1, final_chance)
        update_effect_duration(user_id, "curse")
    
    return result

def can_use_location(user_level: int, location_name: str) -> bool:
    return user_level >= LOCATIONS[location_name]["level"]

def reset_daily_stats():
    today = datetime.now().strftime("%Y-%m-%d")
    sql.execute("UPDATE users SET daily_kills = 0")
    sql.execute("DELETE FROM stats_daily WHERE date != ?", (today,))
    db.commit()

def get_user_rank(total_kills: int):
    sorted_thresholds = sorted(RANKS.keys(), reverse=True)
    for threshold in sorted_thresholds:
        if total_kills >= threshold:
            return RANKS[threshold]
    return RANKS[0]

def get_completed_achievements(user_id: int):
    result = sql.execute("SELECT achievements_completed FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if result and result[0]:
        try:
            return eval(result[0])
        except:
            return {}
    return {}

def check_prestige_requirements(user_id: int, prestige_level: int):
    if prestige_level not in PRESTIGES:
        return False, "Неизвестный уровень престижа"
    
    user = ensure_user(user_id)
    requirements = PRESTIGES[prestige_level]["requirements"]
    total_kills = user[7]
    level = get_level(user[2])
    coins = user[1]
    
    if level < requirements.get("level", 0):
        return False, f"Требуется уровень {requirements.get('level', 0)}"
    if total_kills < requirements.get("kills", 0):
        return False, f"Требуется {requirements.get('kills', 0)} убийств"
    if coins < requirements.get("coins", 0):
        return False, f"Требуется {requirements.get('coins', 0)} монет"
    
    if "unique_animals" in requirements:
        unique_count = len(sql.execute("SELECT DISTINCT animal FROM trophies WHERE user_id = ?", (user_id,)).fetchall())
        if unique_count < requirements["unique_animals"]:
            return False, f"Требуется {requirements['unique_animals']} уникальных животных"
    
    if "titans" in requirements:
        titan_animals = []
        for loc in LOCATIONS.values():
            titan_animals.extend(loc["animals"].get("Титан", []))
        titan_kills = 0
        for animal in titan_animals:
            result = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", (user_id, animal)).fetchone()
            if result:
                titan_kills += result[0]
        if titan_kills < requirements["titans"]:
            return False, f"Требуется убить {requirements['titans']} титанов"
    
    if "all_locations" in requirements and requirements["all_locations"]:
        locations_visited = set()
        for animal_data in sql.execute("SELECT animal FROM trophies WHERE user_id = ?", (user_id,)).fetchall():
            animal = animal_data[0]
            for loc_name, loc_data in LOCATIONS.items():
                for group_animals in loc_data["animals"].values():
                    if animal in group_animals:
                        locations_visited.add(loc_name)
                        break
        if len(locations_visited) < len(LOCATIONS):
            return False, "Требуется побывать во всех локациях"
    
    if "all_weapons" in requirements and requirements["all_weapons"]:
        user_weapons = sql.execute("SELECT COUNT(DISTINCT weapon) FROM user_weapons WHERE user_id = ?", (user_id,)).fetchone()[0]
        if user_weapons < len(WEAPONS_DATA):
            return False, "Требуется купить все виды оружия"
    
    return True, "Все требования выполнены"

def update_effect_duration(user_id: int, effect_name: str):
    """Уменьшает длительность эффекта на 1 и удаляет если duration <= 0"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE battle_effects SET duration = duration - 1 
        WHERE user_id = ? AND effect_name = ? AND duration > 0
    """, (user_id, effect_name))
    cur.execute("DELETE FROM battle_effects WHERE user_id = ? AND duration <= 0", (user_id,))
    conn.commit()
    conn.close()

def use_traps(user_id: int):
    now = int(time.time())
    user = ensure_user(user_id)
    last_use = user[19] if len(user) > 19 else 0
    
    if last_use > 0 and (now - last_use) < 43200:
        hours_left = (43200 - (now - last_use)) // 3600
        minutes_left = ((43200 - (now - last_use)) % 3600) // 60
        return False, f"⏳ Ловушки можно использовать через {hours_left}ч {minutes_left}м"
    
    # Проверяем улучшенные ловушки через прямое соединение
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    has_upgraded = cur.execute(
        "SELECT 1 FROM user_equipment WHERE user_id = ? AND equipment = ?", 
        (user_id, "Улучшенные ловушки")
    ).fetchone() is not None
    conn.close()
    
    animal_count = 5 if has_upgraded else 3
    
    location = user[4]
    caught_animals = []
    
    for _ in range(animal_count):
        rand = random.randint(1, 100)
        if rand <= 50:
            group = "Мелочь"
        elif rand <= 90:
            group = "Средн"
        elif rand <= 98:
            group = "Опасн"
        else:
            group = "Тяжел"
        
        if group in LOCATIONS[location]["animals"] and LOCATIONS[location]["animals"][group]:
            animal = random.choice(LOCATIONS[location]["animals"][group])
            caught_animals.append((group, animal))
            
            if group == "Тяжел":
                sql.execute("UPDATE users SET heavy_traps = heavy_traps + 1 WHERE user_id = ?", (user_id,))
    
    sql.execute("UPDATE users SET last_trap_use = ?, traps_used = traps_used + 1, trap_days_streak = trap_days_streak + 1 WHERE user_id = ?", 
                (now, user_id))
    db.commit()
    
    return True, caught_animals

def add_user_equipment(user_id, equipment_name):
    """Добавляет снаряжение через отдельное соединение"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO user_equipment (user_id, equipment) VALUES (?, ?)", (user_id, equipment_name))
    conn.commit()
    conn.close()

def get_animal_attack_phrase(animal: str) -> str:
    """Получить фразу атаки для конкретного животного"""

    if isinstance(animal, dict):
        animal = animal.get('animal', str(animal))
    elif not isinstance(animal, str):
        animal = str(animal)

    phrases = ANIMAL_ATTACK_PHRASES.get(animal, [])
    if phrases:
        return random.choice(phrases)
    
    # Если нет специальной фразы, создаем общую
    group = None
    for loc in LOCATIONS.values():
        for g, animals in loc["animals"].items():
            if animal in animals:
                group = g
                break
        if group:
            break
    
    damage = CONTRATTACK_DAMAGE.get(group, 25)
    return f"{animal} атакует! -{damage}HP"

def update_battle_hp(user_id: int, change: int):
    """Изменить HP животного (может быть отрицательным = лечение)"""
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("UPDATE battle_state SET animal_hp = animal_hp + ? WHERE user_id = ?", (change, user_id))
    conn.commit()
    conn.close()

def check_achievements(user_id: int):
    """Проверить и выдать достижения игроку"""
    user = ensure_user(user_id)
    completed = get_completed_achievements(user_id)
    new_achievements = []
    
    # Получаем текущие данные игрока
    coins = user[1]
    exp = user[2]
    total_kills = user[7]
    current_hp, max_hp = get_user_health(user_id)
    deaths = user[15] if len(user) > 15 else 0
    counterattack_streak = user[16] if len(user) > 16 else 0
    titan_escape_streak = user[17] if len(user) > 17 else 0
    trap_days_streak = user[18] if len(user) > 18 else 0
    heavy_traps = user[21] if len(user) > 21 else 0
    achievement_streak = user[11] if len(user) > 11 else 0
    level = get_level(exp)
    hunt_counter = user[32] if len(user) > 32 else 0
    
    # Уникальные животные (исправленная версия)
    unique_animals_result = sql.execute("SELECT COUNT(DISTINCT animal) FROM trophies WHERE user_id = ?", (user_id,)).fetchone()
    unique_animals = unique_animals_result[0] if unique_animals_result else 0
    
    # Все оружия
    user_weapons_result = sql.execute("SELECT COUNT(DISTINCT weapon) FROM user_weapons WHERE user_id = ?", (user_id,)).fetchone()
    all_weapons = user_weapons_result[0] if user_weapons_result else 0
    
    # Все локации
    locations_visited = set()
    for animal_data in sql.execute("SELECT animal FROM trophies WHERE user_id = ?", (user_id,)).fetchall():
        animal = animal_data[0]
        for loc_name, loc_data in LOCATIONS.items():
            for group_animals in loc_data["animals"].values():
                if animal in group_animals:
                    locations_visited.add(loc_name)
                    break
    
    all_locations_count = len(locations_visited)
    
    # Убийства по локациям
    location_kills = {}
    for loc_name in LOCATIONS:
        location_kills[loc_name] = 0
    
    for animal_data, count in sql.execute("SELECT animal, count FROM trophies WHERE user_id = ?", (user_id,)).fetchall():
        animal = animal_data
        for loc_name, loc_data in LOCATIONS.items():
            for group_animals in loc_data["animals"].values():
                if animal in group_animals:
                    location_kills[loc_name] += count
                    break
    
    # Проверяем все достижения
    for achievement_name, achievement_data in ACHIEVEMENTS.items():
        if achievement_name in completed:
            continue
            
        condition_met = False
        
        if achievement_data["condition_type"] == "animal_kills":
            animal_name, required_count = achievement_data["condition_value"]
            result = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", (user_id, animal_name)).fetchone()
            if result and result[0] >= required_count:
                condition_met = True
                
        elif achievement_data["condition_type"] == "titan_kills":
            titan_animals = []
            for loc in LOCATIONS.values():
                titan_animals.extend(loc["animals"].get("Титан", []))
            titan_kills = 0
            for animal in titan_animals:
                result = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", (user_id, animal)).fetchone()
                if result:
                    titan_kills += result[0]
            if titan_kills >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "coins":
            if coins >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "location_kills":
            location_name, required_count = achievement_data["condition_value"]
            if location_kills.get(location_name, 0) >= required_count:
                condition_met = True
                
        elif achievement_data["condition_type"] == "unique_animals":
            if unique_animals >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "streak":
            if achievement_streak >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "max_health":
            if max_hp >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "counterattack_streak":
            if counterattack_streak >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "titan_escape_streak":
            if titan_escape_streak >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "deaths":
            if deaths >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "trap_heavy":
            if heavy_traps >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "trap_days_streak":
            if trap_days_streak >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "hunt_count":
            if hunt_counter >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "level":
            if level >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "all_weapons":
            if all_weapons >= achievement_data["condition_value"]:
                condition_met = True
                
        elif achievement_data["condition_type"] == "all_locations":
            if all_locations_count >= achievement_data["condition_value"]:
                condition_met = True
        
        # Если условие выполнено, выдаем достижение
        if condition_met:
            # Добавляем в список выполненных
            completed[achievement_name] = {
                "completed_at": int(time.time()),
                "reward_coins": achievement_data["reward_coins"],
                "reward_exp": achievement_data["reward_exp"],
                "title": achievement_data["title"]
            }
            
            # Выдаем награды
            sql.execute("UPDATE users SET coins = coins + ?, exp = exp + ? WHERE user_id = ?", 
                       (achievement_data["reward_coins"], achievement_data["reward_exp"], user_id))
            
            new_achievements.append(achievement_name)
    
    # Обновляем список выполненных достижений
    if new_achievements:
        sql.execute("UPDATE users SET achievements_completed = ? WHERE user_id = ?", 
                   (str(completed), user_id))
        sql.execute("UPDATE users SET last_achievement_check = ? WHERE user_id = ?", 
                   (int(time.time()), user_id))
        db.commit()
    
    return new_achievements

def check_location_achievements(user_id: int, location: str, kills: int):
    """Проверяет и выдаёт достижения локации с наградами"""
    
    new_achievements = []
    
    # Получаем РЕАЛЬНОЕ количество убийств из БД
    real_stats = sql.execute("SELECT kills FROM location_stats WHERE user_id = ? AND location = ?", 
                            (user_id, location)).fetchone()
    real_kills = real_stats[0] if real_stats else 0
    
    # ========== 1. Достижение "60 убийств" ==========
    if real_kills >= 60:
        existing = sql.execute("SELECT completed FROM location_achievements WHERE user_id = ? AND location = ? AND achievement_type = '60_kills'",
                               (user_id, location)).fetchone()
        if not existing or existing[0] == 0:
            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(location, {}).get("60_kills", {})
            rewards = []
            
            if ach_data.get("coins_reward", 0) > 0:
                sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (ach_data["coins_reward"], user_id))
                rewards.append(f"💰 +{ach_data['coins_reward']} монет")
            if ach_data.get("exp_reward", 0) > 0:
                sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (ach_data["exp_reward"], user_id))
                rewards.append(f"⭐ +{ach_data['exp_reward']} опыта")
            if ach_data.get("title"):
                current_title = sql.execute("SELECT current_title FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
                if not current_title:
                    sql.execute("UPDATE users SET current_title = ? WHERE user_id = ?", (ach_data["title"], user_id))
                    rewards.append(f"👑 Титул: {ach_data['title']}")
                else:
                    rewards.append(f"👑 Титул: {ach_data['title']} (добавлен в коллекцию)")
            
            sql.execute("INSERT OR REPLACE INTO location_achievements (user_id, location, achievement_type, completed, completed_at) VALUES (?, ?, '60_kills', 1, ?)",
                       (user_id, location, int(time.time())))
            db.commit()
            new_achievements.append(("60_kills", location, rewards))
    
    # ========== 2. Достижение "250 убийств" ==========
    if real_kills >= 250:
        existing = sql.execute("SELECT completed FROM location_achievements WHERE user_id = ? AND location = ? AND achievement_type = '250_kills'",
                               (user_id, location)).fetchone()
        if not existing or existing[0] == 0:
            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(location, {}).get("250_kills", {})
            rewards = []
            
            if ach_data.get("coins_reward", 0) > 0:
                sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (ach_data["coins_reward"], user_id))
                rewards.append(f"💰 +{ach_data['coins_reward']} монет")
            if ach_data.get("exp_reward", 0) > 0:
                sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (ach_data["exp_reward"], user_id))
                rewards.append(f"⭐ +{ach_data['exp_reward']} опыта")
            if ach_data.get("quote"):
                current_quote = sql.execute("SELECT current_quote FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
                if not current_quote or current_quote == "Я начинающий охотник, и я иду к своей цели":
                    sql.execute("UPDATE users SET current_quote = ? WHERE user_id = ?", (ach_data["quote"], user_id))
                    rewards.append(f"💬 Новая цитата!")
                else:
                    rewards.append(f"💬 Цитата добавлена в коллекцию")
            
            sql.execute("INSERT OR REPLACE INTO location_achievements (user_id, location, achievement_type, completed, completed_at) VALUES (?, ?, '250_kills', 1, ?)",
                       (user_id, location, int(time.time())))
            db.commit()
            new_achievements.append(("250_kills", location, rewards))
    
    # ========== 3. Достижение "90% видов" (вместо 100%) ==========
    existing_all = sql.execute("SELECT completed FROM location_achievements WHERE user_id = ? AND location = ? AND achievement_type = 'all_species'",
                               (user_id, location)).fetchone()
    if not existing_all or existing_all[0] == 0:
        # Получаем ВСЕХ животных в локации
        all_animals = []
        for animals_list in LOCATIONS[location]["animals"].values():
            all_animals.extend(animals_list)
        
        total_animals = len(all_animals)
        
        # 90% (округляем вверх, чтобы 90%+)
        # Например: 25 * 0.9 = 22.5 → нужно 23
        required_count = (total_animals * 9 + 9) // 10  # округление вверх
        
        # Получаем уникальных животных, которых убил игрок
        killed_animals = sql.execute("SELECT DISTINCT animal FROM trophies WHERE user_id = ?", (user_id,)).fetchall()
        killed_animals = [a[0] for a in killed_animals]
        
        # Считаем, сколько видов из локации убито
        killed_count = 0
        for animal in all_animals:
            if animal in killed_animals:
                killed_count += 1
        
        # ОТЛАДКА (удали после проверки)
        print(f"🏆 {location}: всего={total_animals}, нужно={required_count}, убито={killed_count}")
        
        # Если убито >= 90% — выдаём достижение
        if killed_count >= required_count:
            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(location, {}).get("all_species", {})
            rewards = []
            
            if ach_data.get("coins_reward", 0) > 0:
                sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (ach_data["coins_reward"], user_id))
                rewards.append(f"💰 +{ach_data['coins_reward']} монет")
            if ach_data.get("exp_reward", 0) > 0:
                sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (ach_data["exp_reward"], user_id))
                rewards.append(f"⭐ +{ach_data['exp_reward']} опыта")
            if ach_data.get("status"):
                current_status = sql.execute("SELECT current_status FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
                if not current_status or current_status == "На охоте🏹":
                    sql.execute("UPDATE users SET current_status = ? WHERE user_id = ?", (ach_data["status"], user_id))
                    rewards.append(f"🏷️ Статус: {ach_data['status']}")
                else:
                    rewards.append(f"🏷️ Статус: {ach_data['status']} (добавлен в коллекцию)")
            
            sql.execute("INSERT OR REPLACE INTO location_achievements (user_id, location, achievement_type, completed, completed_at) VALUES (?, ?, 'all_species', 1, ?)",
                       (user_id, location, int(time.time())))
            db.commit()
            new_achievements.append(("all_species", location, rewards))
    
    return new_achievements

def get_weapon_data(weapon_name: str) -> dict:
    """Получить данные об оружии по имени"""
    return WEAPONS_DATA.get(weapon_name, WEAPONS_DATA["Револьвер"])

def get_weapon_chances(weapon_name: str, group_index: int) -> float:
    """Получить шанс попадания для конкретной группы животных"""
    weapon = get_weapon_data(weapon_name)
    chances = weapon["chances"]
    if group_index < len(chances):
        return chances[group_index]
    return 0

def get_weapon_damage(weapon_name: str) -> int:
    """Получить урон оружия"""
    return get_weapon_data(weapon_name)["damage"]

def get_weapon_ability(weapon_name: str) -> tuple:
    """Получить способность оружия: (название_способности, описание, шанс)"""
    weapon = get_weapon_data(weapon_name)
    return weapon.get("ability"), weapon.get("ability_desc"), weapon.get("ability_chance", 0)

def get_weapon_level_req(weapon_name: str) -> int:
    """Получить минимальный уровень для использования оружия"""
    return get_weapon_data(weapon_name)["level_req"]

def get_weapon_group(weapon_name: str) -> str:
    return WEAPONS_DATA.get(weapon_name, {}).get("group", "обычные")

def get_weapon_obtain(weapon_name: str) -> dict:
    """Получить информацию о получении оружия"""
    return get_weapon_data(weapon_name)["obtain"]

def get_weapon_price(weapon_name: str) -> int:
    """Получить цену оружия (если покупается за монеты)"""
    obtain = get_weapon_obtain(weapon_name)
    if obtain.get("type") == "shop":
        return obtain.get("price", 0)
    return 0

def get_available_weapons(user_level: int) -> dict:
    """Получить оружие, доступное по уровню, сгруппированное"""
    available = {}
    for group_name, group_data in WEAPON_GROUPS.items():
        if user_level >= group_data["level_req"]:
            available[group_name] = group_data["weapons"]
    return available

def get_weapon_group_by_name(weapon_name: str) -> str:
    """Определить группу оружия по названию"""
    for group_name, group_data in WEAPON_GROUPS.items():
        if weapon_name in group_data["weapons"]:
            return group_name
    return "обычные"

def claim_daily_streak(user_id: int):
    """Получить награду за серию (каждые 12 часов)"""
    user = ensure_user(user_id)
    now = int(time.time())
    
    # Получаем current_streak и last_claim из БД
    result = sql.execute("SELECT daily_streak, last_daily_claim FROM users WHERE user_id = ?", (user_id,)).fetchone()
    
    if result:
        current_streak = result[0] if result[0] is not None else 0
        last_claim = result[1] if result[1] is not None else 0
    else:
        current_streak = 0
        last_claim = 0
    
    # Проверяем, прошло ли 12 часов (43200 секунд)
    if last_claim > 0 and (now - last_claim) < 43200:
        hours_left = (43200 - (now - last_claim)) // 3600
        minutes_left = ((43200 - (now - last_claim)) % 3600) // 60
        return False, f"⏳ Следующая награда через {hours_left}ч {minutes_left}м", 0, []
    
    # Увеличиваем серию
    new_streak = current_streak + 1
    
    # Получаем награду за текущий день
    if new_streak <= 100:
        reward = DAILY_STREAK_REWARDS.get(new_streak, {"coins": 350, "exp": 0, "item": None})
    else:
        # Случайная награда после 100 дня
        random_rewards = [
            {"coins": 300, "exp": 0},
            {"coins": 400, "exp": 0},
            {"coins": 500, "exp": 0},
            {"coins": 0, "exp": 500},
            {"coins": 0, "exp": 400},
            {"coins": 0, "exp": 450},
            {"coins": 0, "exp": 600},
            {"coins": 500, "exp": 400}
        ]
        reward = random.choice(random_rewards)
        reward["item"] = None
        reward["status"] = None
        reward["title"] = None
        reward["quote"] = None
        reward["artifact"] = None
        reward["extra_items"] = None
    
    # Если день 100, дальше не увеличиваем (но можно идти дальше, просто награды случайные)
    # Убираем ограничение на 100, можно идти до бесконечности
    
    # Выдаём награды
    rewards_text = []
    
    # Монеты
    if reward.get("coins", 0) > 0:
        sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (reward["coins"], user_id))
        rewards_text.append(f"💰 +{reward['coins']} монет")
    
    # Опыт
    if reward.get("exp", 0) > 0:
        sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (reward["exp"], user_id))
        rewards_text.append(f"⭐ +{reward['exp']} опыта")
        
    
    if reward.get("item"):
        if reward["item"] == "medkit":
            # Аптечка - добавляем в инвентарь баффов
            add_user_buff(user_id, "Аптечка", 1)
            rewards_text.append("📦 Аптечка (добавлена в инвентарь баффов)")
        
        elif reward["item"] == "golden_bullet":
            add_user_buff(user_id, "Золотая пуля", 1)
            rewards_text.append("📦 Золотая пуля (добавлена в инвентарь баффов)")
        
        elif reward["item"] == "diamond_bullet":
            add_user_buff(user_id, "Алмазная пуля", 1)
            rewards_text.append("📦 Алмазная пуля (добавлена в инвентарь баффов)")
        
        elif reward["item"] == "drone":
            add_user_buff(user_id, "Дрон", 1)
            rewards_text.append("📦 Дрон (добавлен в инвентарь баффов)")
        
        elif reward["item"] == "ultra_drone":
            add_user_buff(user_id, "Ультра-звуковой дрон", 1)
            rewards_text.append("📦 Ультра-звуковой дрон (добавлен в инвентарь баффов)")
        
        elif reward["item"] == "energy_drink":
            add_user_buff(user_id, "Энергетик", 1)
            rewards_text.append("📦 Энергетик (добавлен в инвентарь баффов)")
        
        elif reward["item"] == "immortality_staff":
            add_user_buff(user_id, "Посох бессмертия", 1)
            rewards_text.append("📦 Посох бессмертия (добавлен в инвентарь баффов)")  
              
    # Статус
    if reward.get("status"):
        sql.execute("UPDATE users SET current_status = ? WHERE user_id = ?", (reward["status"], user_id))
        rewards_text.append(f"🏷️ Статус: {reward['status']}")
    
    # Титул
    if reward.get("title"):
        sql.execute("UPDATE users SET current_title = ? WHERE user_id = ?", (reward["title"], user_id))
        rewards_text.append(f"👑 Титул: {reward['title']}")
    
    # Цитата
    if reward.get("quote"):
        sql.execute("UPDATE users SET current_quote = ? WHERE user_id = ?", (reward["quote"], user_id))
        rewards_text.append(f"💬 Новая цитата!")
    
    # Артефакт (Драконья кровь)
    if reward.get("artifact") == "dragon_blood":
        owned = sql.execute("SELECT 1 FROM user_equipment WHERE user_id = ? AND equipment = ?", 
                           (user_id, "🐉 Драконья кровь")).fetchone()
        if not owned:
            sql.execute("INSERT INTO user_equipment VALUES (?, ?)", (user_id, "🐉 Драконья кровь"))
            rewards_text.append("🐉 Артефакт: Драконья кровь (+10% шанс мутации)")
    
    # Обновляем серию и время последнего получения
    sql.execute("UPDATE users SET daily_streak = ?, last_daily_claim = ? WHERE user_id = ?", 
               (new_streak, now, user_id))
    db.commit()
    
    # Получаем эмодзи для текущего дня
    streak_emoji = get_streak_emoji(new_streak)
    
    # Формируем сообщение
    result_text = f"🎁 **Ежедневная серия!**\n\n"
    result_text += f"📅 День {new_streak} {streak_emoji}\n\n"
    result_text += "Награда:\n" + "\n".join(rewards_text)
    
    return True, result_text, new_streak, rewards_text


# ================== ФУНКЦИИ ВЫЖИВАНИЯ ==================
def get_user_survival_items(user_id: int):
    """Получить предметы выживания игрока (безопасная версия)"""
    try:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        items = cur.execute(
            "SELECT item_name FROM survival_items WHERE user_id = ?", 
            (user_id,)
        ).fetchall()
        conn.close()
        return [item[0] for item in items]
    except Exception as e:
        print(f"Ошибка get_user_survival_items: {e}")
        return []

def check_survival_damage(user_id: int, location: str):
    """Проверить и нанести урон за отсутствие предмета выживания - ровно каждые 3 охоты"""
    if location == "Тайга":
        return False, None
    
    has_item, item_name = has_survival_item(user_id, location)
    
    if not has_item:
        user = ensure_user(user_id)
        survival_hunt_count = user[27] if len(user) > 27 else 0
        
        survival_hunt_count += 1
        
        if survival_hunt_count >= 3:
            survival_hunt_count = 0
            
            damage = 80
            update_health(user_id, -damage)
            
            phrases = SURVIVAL_DAMAGE_PHRASES.get(location, ["Окружающая среда вредит вашему здоровью! -80HP"])
            phrase = random.choice(phrases)
            
            sql.execute("UPDATE users SET survival_hunt_count = ? WHERE user_id = ?",
                       (survival_hunt_count, user_id))
            db.commit()
            
            return True, phrase
        else:
            sql.execute("UPDATE users SET survival_hunt_count = ? WHERE user_id = ?",
                       (survival_hunt_count, user_id))
            db.commit()
            return False, None
    else:
        sql.execute("UPDATE users SET survival_hunt_count = 0 WHERE user_id = ?", (user_id,))
        db.commit()
        return False, None

# ================== ФУНКЦИИ ИВЕНТА ==================
def is_event_active() -> bool:
    """Проверяет, активен ли ивент"""
    return EVENT_ACTIVE

def get_event_quest_progress(user_id: int) -> int:
    """Получить текущий прогресс заданий"""
    user = sql.execute("SELECT event_quest FROM users WHERE user_id = ?", (user_id,)).fetchone()
    return user[0] if user else 0

def update_event_quest(user_id: int, eggs: int):
    """Обновить прогресс заданий - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    try:
        # Получаем текущий прогресс
        result = sql.execute("SELECT event_quest FROM users WHERE user_id = ?", (user_id,)).fetchone()
        current_quest = result[0] if result else 0
        
        rewards_given = []
        
        for i in range(current_quest, len(EVENT_QUESTS)):
            quest = EVENT_QUESTS[i]
            if eggs >= quest["need"]:
                # Выдаём награду
                if quest["reward_coins"] > 0:
                    sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (quest["reward_coins"], user_id))
                    rewards_given.append(f"💰 +{quest['reward_coins']} монет")
                
                if quest["reward_exp"] > 0:
                    sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (quest["reward_exp"], user_id))
                    rewards_given.append(f"⭐ +{quest['reward_exp']} опыта")
                
                if quest["reward_item"] == "golden_bullet":
                    sql.execute("UPDATE users SET golden_bullet = golden_bullet + 1 WHERE user_id = ?", (user_id,))
                    rewards_given.append(f"💫 +1 Золотая пуля")
                
                if quest["reward_item"] == "diamond_bullet":
                    sql.execute("UPDATE users SET diamond_bullet = diamond_bullet + 1 WHERE user_id = ?", (user_id,))
                    rewards_given.append(f"💎 +1 Алмазная пуля")
                
                if quest["reward_item"] == "drone":
                    expires = int(time.time()) + 1800
                    sql.execute("UPDATE users SET drone_target = 'random', drone_expires = ? WHERE user_id = ?", (expires, user_id))
                    rewards_given.append(f"🛸 +1 Дрон (активирован на 30 мин)")
                
                if quest["reward_item"] == "title" and quest["title_name"]:
                    sql.execute("UPDATE users SET current_title = ? WHERE user_id = ?", (quest["title_name"], user_id))
                    rewards_given.append(f"👑 Титул: {quest['title_name']}")
                
                # Обновляем номер выполненного задания
                sql.execute("UPDATE users SET event_quest = ? WHERE user_id = ?", (i + 1, user_id))
                db.commit()
                return True, i + 1, quest, rewards_given
        
        return False, current_quest, None, []
        
    except Exception as e:
        print(f"Ошибка в update_event_quest: {e}")
        db.rollback()
        return False, 0, None, []
        
def add_event_egg(user_id: int, amount: int):
    """Добавить яйца игроку - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    try:
        # Проверяем и создаём колонки если нужно
        try:
            sql.execute("SELECT event_eggs FROM users LIMIT 1")
        except sqlite3.OperationalError:
            sql.execute("ALTER TABLE users ADD COLUMN event_eggs INTEGER DEFAULT 0")
            sql.execute("ALTER TABLE users ADD COLUMN event_quest INTEGER DEFAULT 0")
            sql.execute("ALTER TABLE users ADD COLUMN event_egg_claim INTEGER DEFAULT 0")
            db.commit()
        
        # Добавляем яйца
        sql.execute("UPDATE users SET event_eggs = event_eggs + ? WHERE user_id = ?", (amount, user_id))
        
        # Обновляем топ
        sql.execute("""
            INSERT INTO event_top (user_id, eggs) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET eggs = eggs + ?
        """, (user_id, amount, amount))
        
        # Получаем новое количество
        result = sql.execute("SELECT event_eggs FROM users WHERE user_id = ?", (user_id,)).fetchone()
        new_eggs = result[0] if result else amount
        
        db.commit()
        
        # Проверяем задания (с защитой от ошибок)
        completed = False
        quest_num = 0
        quest_data = None
        rewards = []
        
        try:
            completed, quest_num, quest_data, rewards = update_event_quest(user_id, new_eggs)
        except Exception as e:
            print(f"Ошибка проверки заданий: {e}")
        
        return new_eggs, completed, quest_num, quest_data, rewards
        
    except Exception as e:
        print(f"Ошибка в add_event_egg: {e}")
        db.rollback()
        return 0, False, 0, None, []

# ================== ФУНКЦИИ БОЕВОЙ СИСТЕМЫ ==================

def start_battle(user_id: int, animal_id: str, animal_name: str, group_name: str, is_pack: bool = False, pack_size: int = 1, sneak_bonus: int = 0):
    """Начинает новый бой"""
    max_hp = ANIMAL_HP.get(group_name, 1)
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO battle_state 
        (user_id, animal_id, animal_name, group_name, animal_hp, animal_max_hp, is_pack, pack_size, ability_used, turn, sneak_bonus, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, animal_id, animal_name, group_name, max_hp, max_hp, is_pack, pack_size, 0, 0, sneak_bonus, int(time.time())))
    conn.commit()
    conn.close()

def get_battle_state(user_id: int):
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    state = cur.execute("SELECT * FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return state

def update_battle_hp(user_id: int, damage: int):
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("UPDATE battle_state SET animal_hp = animal_hp - ? WHERE user_id = ?", (damage, user_id))
    conn.commit()
    conn.close()

def update_battle_ability_used(user_id: int):
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("UPDATE battle_state SET ability_used = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def end_battle(user_id: int):
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM battle_state WHERE user_id = ?", (user_id,))
    cur.execute("DELETE FROM battle_effects WHERE user_id = ?", (user_id,))
    cur.execute("DELETE FROM battle_mods WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def add_battle_effect(user_id: int, effect_name: str, duration: int, value: int = 0):
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO battle_effects (user_id, effect_name, duration, value)
        VALUES (?, ?, ?, ?)
    """, (user_id, effect_name, duration, value))
    conn.commit()
    conn.close()

def get_battle_effects(user_id: int):
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    effects = cur.execute("SELECT effect_name, duration, value FROM battle_effects WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return {e[0]: {"duration": e[1], "value": e[2]} for e in effects}

def apply_titan_ability(location: str, user_id: int) -> tuple:
    """
    Применяет способность титана.
    Возвращает: (заблокирован_ли_выстрел, сообщение, доп_урон)
    """
    if location not in TITAN_ABILITIES:
        return False, "", 0
    
    ability = TITAN_ABILITIES[location]
    if random.randint(1, 100) > ability["chance"]:
        return False, "", 0
    
    effect = ability["effect"]
    
    if effect == "time_rewind":
        return True, "🕐 Титан закрутил время! Твоя атака отбита!", 0
    
    elif effect == "water_flow":
        return True, "🌊 Поток воды отбил твой выстрел!", 0
    
    elif effect == "curse":
        add_battle_effect(user_id, "curse", 1, 60)
        return False, "🧪 Ты проклят! Следующая атака -60% к попаданию!", 0
    
    elif effect == "corruption":
        if random.randint(1, 100) <= 40:
            return True, "👻 Порча не дала тебе выстрелить!", 0
        return False, "", 0
    
    elif effect == "radiation":
        damage = 30
        update_health(user_id, -damage)
        return False, f"☢️ Радиация сжигает тебя! -{damage} HP", damage
    
    elif effect == "lightning":
        damage = 20
        update_health(user_id, -damage)
        if random.randint(1, 100) <= 60:
            return True, f"⚡ Молния ударила в тебя! Атака провалена, -{damage} HP", damage
        return False, f"⚡ Молния ударила рядом! -{damage} HP", damage
    
    elif effect == "virus":
        if random.randint(1, 100) <= 40:
            damage = 50
            update_health(user_id, -damage)
            return True, f"💾 Вирус заставил выстрелить в себя! -{damage} HP", damage
        return False, "", 0
    
    elif effect == "fire_jet":
        damage = 40
        update_health(user_id, -damage)
        return False, f"🔥 Струя огня опалила тебя! -{damage} HP", damage
    
    elif effect == "singularity":
        if random.randint(1, 100) <= 25:
            update_health(user_id, -999)
            return True, "🌀 Сингулярность разорвала тебя на части! Ты погиб!", 999
        return False, "", 0
    
    return False, "", 0

def animal_action(user_id: int, group: str, location: str) -> tuple:
    """
    Обрабатывает ход животного.
    Возвращает: (урон_игроку, сообщение, убежало_ли, модификатор_попадания)
    """
    effects = get_battle_effects(user_id)
    
    # ========== ЭФФЕКТЫ ==========
    if "burn" in effects:
        burn_damage = effects["burn"]["value"]
        update_battle_hp(user_id, -burn_damage)
        update_effect_duration(user_id, "burn")
        return 0, f"🔥 Животное горит! -{burn_damage} HP", False, 0
    
    if "decay" in effects:
        decay_damage = effects["decay"]["value"]
        update_battle_hp(user_id, -decay_damage)
        update_effect_duration(user_id, "decay")
        return 0, f"💀 Гниение разъедает плоть! -{decay_damage} HP", False, 0
    
    if "death_poison" in effects:
        duration = effects["death_poison"]["duration"]
        if duration <= 1:
            update_battle_hp(user_id, 999999)
            update_effect_duration(user_id, "death_poison")
            return 0, "💀 Смертельный яд скорпиона убил животное!", True, 0
        else:
            update_effect_duration(user_id, "death_poison")
            return 0, f"💀 Животное отравлено! Умрёт через {duration-1} хода", False, 0
    
    if "fear" in effects:
        update_effect_duration(user_id, "fear")
        return 0, "😱 Животное в страхе убегает, оставляя награду!", True, 0
    
    if "freeze" in effects:
        update_effect_duration(user_id, "freeze")
        return 0, "❄️ Животное заморожено и не может атаковать!", False, 0
    
    if "stun" in effects:
        update_effect_duration(user_id, "stun")
        return 0, "⚡ Животное оглушено и не может атаковать!", False, 0
    
    if "paralyze" in effects:
        update_effect_duration(user_id, "paralyze")
        return 0, "🧪 Животное парализовано и не может двигаться!", False, 0
    
    # Замедление
    if "slow" in effects:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        turn = cur.execute("SELECT turn FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        if turn and turn[0] % 2 == 1:
            return 0, "🐢 Животное замедлено и пропускает ход!", False, 0
    
    # ========== СПОСОБНОСТИ ТИТАНОВ (срабатывают ДО выбора действия) ==========
    if group == "Титан" and location in TITAN_ABILITIES:
        ability = TITAN_ABILITIES[location]
        chance = ability["chance"]
        
        if random.randint(1, 100) <= chance:
            effect = ability["effect"]
            
            if effect == "time_rewind":
                return 0, f"🕐 {ability['name']}! Твоя атака отбита!", False, 0
            
            elif effect == "water_flow":
                return 0, f"🌊 {ability['name']}! Твой выстрел отбит!", False, 0
            
            elif effect == "curse":
                add_battle_effect(user_id, "curse", 1, 60)
                return 0, f"🧪 {ability['name']}! Ты проклят! -60% к попаданию в следующем ходу!", False, 0
            
            elif effect == "corruption":
                return 0, f"👻 {ability['name']}! Ты не можешь выстрелить в этом ходу!", False, 0
            
            elif effect == "radiation":
                damage = 30
                update_health(user_id, -damage)
                return damage, f"☢️ {ability['name']}! Радиация сжигает тебя! -{damage} HP", False, 0
            
            elif effect == "lightning":
                damage = 20
                update_health(user_id, -damage)
                return damage, f"⚡ {ability['name']}! Молния ударила в тебя! -{damage} HP", False, 0
            
            elif effect == "virus":
                damage = 50
                update_health(user_id, -damage)
                return damage, f"💾 {ability['name']}! Вирус заставил выстрелить в себя! -{damage} HP", False, 0
            
            elif effect == "fire_jet":
                damage = 40
                update_health(user_id, -damage)
                return damage, f"🔥 {ability['name']}! Струя огня опалила тебя! -{damage} HP", False, 0
            
            elif effect == "singularity":
                damage = 999
                update_health(user_id, -damage)
                return damage, f"🌀 {ability['name']}! Сингулярность разорвала тебя на части! Ты погиб!", False, 0
    
    # ========== ВЫБОР ДЕЙСТВИЯ ДЛЯ ГРУППЫ ==========
    actions = ANIMAL_ACTIONS.get(group, [])
    if not actions:
        return 0, "", False, 0
    
    total_chance = sum(a["chance"] for a in actions)
    rand = random.randint(1, total_chance)
    cumulative = 0
    
    for action in actions:
        cumulative += action["chance"]
        if rand <= cumulative:
            damage = action.get("damage", 0)
            heal = action.get("heal", 0)
            hit_mod = action.get("hit_mod", 0)
            action_name = action["name"]
            
            # Регенерация
            if heal > 0:
                update_battle_hp(user_id, -heal)
                return 0, f"💚 {action_name} +{heal} HP", False, 0
            
            # Попытка убежать
            if "убежать" in action_name.lower() or "убегает" in action_name.lower():
                infection = effects.get("infection")
                if infection and random.randint(1, 100) <= infection.get("value", 0):
                    update_battle_hp(user_id, 999999)
                    update_effect_duration(user_id, "infection")
                    return 0, "🦠 Инфекция убила животное при попытке побега!", True, 0
                
                if random.randint(1, 100) <= 20:
                    return 0, f"🏃 {action_name}!", True, 0
                return 0, f"🏃 {action_name}, но неудачно!", False, 0
            
            # Атака
            if damage > 0:
                if "invincible" in effects:
                    update_effect_duration(user_id, "invincible")
                    return 0, f"🛡️ Щит веры защитил вас! {action_name} (0 HP)", False, 0
                
                if "stone_skin" in effects:
                    damage = int(damage * (1 - effects["stone_skin"]["value"] / 100))
                
                return damage, f"{action_name} -{damage} HP", False, 0
            
            # Защита
            if hit_mod != 0:
                return 0, f"🛡️ {action_name} (штраф к попаданию {abs(hit_mod)}%)", False, hit_mod
            
            return 0, action_name, False, 0
    
    return 0, "", False, 0

def calculate_damage(weapon_name: str, group: str, location: str, body_part: str = None, user_id: int = None) -> tuple:
    """Возвращает (урон, сообщение_о_способности)"""
    weapon_data = get_weapon_data(weapon_name)
    base_damage = weapon_data["damage"]
    
    damage_mult = 1.0
    hit_mod = 0
    
    # Бонус от локации
    location_bonus = get_weapon_location_bonus(weapon_name, location)
    damage_mult += location_bonus["damage"] / 100
    hit_mod += location_bonus["hit"]
    
    # Бонус от части тела
    if body_part and location in BODY_PARTS and body_part in BODY_PARTS[location]:
        part_data = BODY_PARTS[location][body_part]
        damage_mult *= part_data["damage_mult"]
        hit_mod += part_data["hit_mod"]
    
    # Бонус от подкрадывания
    if user_id:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        mod = cur.execute("SELECT hit_bonus, damage_bonus FROM battle_mods WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        if mod:
            hit_mod += mod[0]
            damage_mult += mod[1] / 100
    
    final_damage = int(base_damage * damage_mult)
    
    # Способность оружия (только если есть)
    ability, ability_desc, ability_chance = get_weapon_ability(weapon_name)
    ability_text = ""
    if ability and user_id:
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        state = cur.execute("SELECT ability_used FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        if state and state[0] == 0:
            if random.randint(1, 100) <= ability_chance:
                ability_text = f"\n✨ Сработала способность: {ability_desc}!"
                # Эффекты способностей добавляются отдельно
    
    return final_damage, ability_text

# ================== БОТ ==================
bot = Bot(TOKEN)
dp = Dispatcher()

# ===== MIDDLEWARE ДЛЯ ЛОГИРОВАНИЯ ОШИБОК =====
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
import logging
import traceback

# Настройка логирования (добавьте в начало файла, но после импортов)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_errors.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ErrorLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            error_text = f"""
🔴 ОШИБКА:
Тип: {type(e).__name__}
Сообщение: {str(e)}
Traceback:
{traceback.format_exc()}
"""
            logger.error(error_text)
            
            if hasattr(event, 'answer'):
                try:
                    await event.answer("❌ Произошла ошибка", show_alert=True)
                except:
                    pass
            raise



# ================== ПОГОДА 1 ==================
WEATHER_CHAT_IDS = [
    -1002945494656,  # Ваш первый чат
    -1002008310880,  # Второй чат (замените на реальный ID)
     # Третий чат (опционально)
]

async def update_weather():
    """Обновляет погоду каждый час и отправляет красивое уведомление в указанные чаты"""
    global current_weather, last_weather_change
    now = int(time.time())
    
    if now - last_weather_change >= 3600:  # каждый час
        old_weather = current_weather
        current_weather = random.choice(WEATHER_TYPES)
        last_weather_change = now
        
        # КРАСИВЫЕ ФРАЗЫ ДЛЯ КАЖДОЙ ПОГОДЫ
        weather_messages = {
            "☀️ Солнечно": {
                "phrase": "☀️ **СОЛНЦЕ ПРОСНУЛОСЬ!** ☀️\n\nЗолотые лучи пробиваются сквозь листву, звери вышли погреться на поляны.",
                "bonus": "✅ +10% к попаданию\n✅ +5% к монетам\n✅ +5% к опыту"
            },
            "☁️ Облачно": {
                "phrase": "☁️ **НЕБО ЗАТЯНУЛО ОБЛАКАМИ** ☁️\n\nПрохлада опустилась на лес. Ничто не мешает охоте.",
                "bonus": "➖ Без изменений"
            },
            "🌧️ Дождь": {
                "phrase": "🌧️ **ХЛЮПАЕТ ДОЖДЬ** 🌧️\n\nКапли барабанят по листьям, следы тяжелых зверей становятся заметнее.",
                "bonus": "⚠️ -7% к попаданию\n✅ +15% к монетам\n✅ +10% к опыту\n✅ +10% найти тяжёлого"
            },
            "⛈️ Гроза": {
                "phrase": "⛈️ **ГРЯНУЛА ГРОЗА!** ⛈️\n\nМолнии сверкают, гром гремит! Опасные хищники покидают укрытия.",
                "bonus": "⚠️ -10% к попаданию\n✅ +15% найти опасного\n✅ +30% к монетам"
            },
            "🌫️ Туманно": {
                "phrase": "🌫️ **ГУСТОЙ ТУМАН ОКУТАЛ ЛЕС** 🌫️\n\nВидимость почти нулевая. Самое время для скрытной охоты...",
                "bonus": "⚠️ -10% к попаданию\n⚠️ -10% найти животное"
            },
            "💨 Ветер": {
                "phrase": "💨 **ПОДУЛ СИЛЬНЫЙ ВЕТЕР!** 💨\n\nВетер шумит в кронах, запахи разносятся далеко по лесу.",
                "bonus": "✅ +20% найти животное\n⚠️ -10% к попаданию"
            }
        }
        
        data = weather_messages.get(current_weather, {
            "phrase": f"🌤️ Погода изменилась на {current_weather}",
            "bonus": ""
        })
        
        # Формируем сообщение
        message = f"{data['phrase']}\n\n📊 **Эффекты погоды:**\n{data['bonus']}"
        
        # Отправляем во ВСЕ чаты из списка
        for chat_id in WEATHER_CHAT_IDS:
            try:
                await bot.send_message(chat_id, message, parse_mode="Markdown")
                print(f"🌦️ Погода отправлена в чат {chat_id}: {old_weather} → {current_weather}")
            except Exception as e:
                print(f"❌ Ошибка отправки погоды в чат {chat_id}: {e}")
        
        return True
    return False

# ================== ЧАТ АЙДИ ==================

@dp.message(Command("айди"))
async def get_chat_id(msg: Message):
    await msg.answer(f"🆔 ID этого чата: `{msg.chat.id}`", parse_mode="Markdown") 
    
# ================== ПОГОДА 2 ==================
@dp.message(lambda msg: msg.text and msg.text.lower() == "погода")
async def show_weather(msg: Message):
    """Показать текущую погоду с красивым описанием"""
    global current_weather
    
    # Описания для каждой погоды
    weather_descriptions = {
        "☀️ Солнечно": {
            "emoji": "☀️",
            "title": "Ясный день",
            "description": "Солнце светит ярко, видимость отличная. Звери вышли погреться.",
            "effects": "+10% к шансу попадания"
        },
        "☁️ Облачно": {
            "emoji": "☁️",
            "title": "Пасмурно",
            "description": "Небо затянуто облаками, но охоте ничего не мешает.",
            "effects": "Никаких особых эффектов"
        },
        "🌧️ Дождь": {
            "emoji": "🌧️",
            "title": "Дождливо",
            "description": "Моросит дождь. Следы тяжелых зверей видны лучше, но стрелять сложнее.",
            "effects": "+10% найти тяжёлого, -7% к попаданию"
        },
        "⛈️ Гроза": {
            "emoji": "⛈️",
            "title": "Гроза",
            "description": "Гремит гром, сверкают молнии. Опасные звери выходят из укрытий.",
            "effects": "+15% найти опасного, -10% к попаданию"
        },
        "🌫️ Туманно": {
            "emoji": "🌫️",
            "title": "Туман",
            "description": "Густой туман окутал лес. Почти ничего не видно.",
            "effects": "Шанс попадания снижается на 10% от текущего значения"
        },
        "💨 Ветер": {
            "emoji": "💨",
            "title": "Ветрено",
            "description": "Сильный ветер шумит в кронах. Животных сложнее услышать, но проще найти по следам.",
            "effects": "+20% к шансу найти животное"
        }
    }
    
    weather_data = weather_descriptions.get(current_weather, weather_descriptions["☁️ Облачно"])
    effects = WEATHER_EFFECTS[current_weather]
    
    text = f"""
{weather_data['emoji']} **{weather_data['title']}** {weather_data['emoji']}

*{weather_data['description']}*

📊 **Эффекты:**
• {weather_data['effects']}

🌡️ **Текущая погода:** {current_weather}
"""
    
    await msg.answer(text, parse_mode="Markdown")


# ================== АДМИН КОМАНДЫ ==================
@dp.message(lambda msg: msg.text and msg.text.startswith("дипскип"))
async def admin_skip(msg: Message):
    """Сбросить таймер охоты для игрока"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        
        if len(parts) >= 2 and parts[1].lower() == "алл":
            # Сброс для всех игроков
            sql.execute("UPDATE users SET last_hunt = 0")
            db.commit()
            await msg.answer("✅ Таймер охоты сброшен для ВСЕХ игроков!")
            print(f"🔧 Админ {msg.from_user.id} сбросил таймер для ВСЕХ игроков")
            
            # Уведомляем всех игроков
            all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
            for user_id, username in all_users:
                try:
                    await bot.send_message(user_id, "🔄 Ваш таймер охоты был сброшен администратором!")
                except:
                    pass
                    
        elif len(parts) >= 2 and "@" in parts[1]:
            username = parts[1].replace("@", "").strip()
            user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
            if user:
                sql.execute("UPDATE users SET last_hunt = 0 WHERE user_id = ?", (user[0],))
                db.commit()
                await msg.answer(f"✅ Таймер охоты сброшен для @{username}")
                print(f"🔧 Админ {msg.from_user.id} сбросил таймер для @{username}")
                
                # Уведомляем игрока
                try:
                    await bot.send_message(user[0], "🔄 Ваш таймер охоты был сброшен администратором!")
                except:
                    pass
            else:
                await msg.answer(f"❌ Пользователь @{username} не найден в базе")
        else:
            await msg.answer("❌ Используйте: дипскип @username\nИли: дипскип алл - для всех игроков")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

# ================== АДМИН КОМАНДА ОТБОРА ==================

@dp.message(lambda msg: msg.text and msg.text.startswith("дипотбор"))
async def admin_take_item(msg: Message):
    """Отобрать предмет/снаряжение/титул у игрока
    Форматы:
    дипотбор @username титул
    дипотбор @username статус
    дипотбор @username цитата
    дипотбор @username снаряжение "Название"
    дипотбор @username предмет "Название"
    дипотбор @username яйца 50
    дипотбор @username монеты 1000
    дипотбор @username опыт 500
    дипотбор @username уровни 5
    дипотбор @username оружие "Название"
    """
    try:
        # Проверка прав админа
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        parts = msg.text.split(maxsplit=3)
        
        if len(parts) < 3:
            await msg.answer(
                "❌ Используйте:\n"
                "дипотбор @username титул\n"
                "дипотбор @username статус\n"
                "дипотбор @username цитата\n"
                "дипотбор @username снаряжение \"Название\"\n"
                "дипотбор @username предмет \"Название\"\n"
                "дипотбор @username яйца <кол-во>\n"
                "дипотбор @username монеты <кол-во>\n"
                "дипотбор @username опыт <кол-во>\n"
                "дипотбор @username уровни <кол-во>\n"
                "дипотбор @username оружие \"Название\""
            )
            return
        
        username = parts[1].replace("@", "").strip()
        action = parts[2].lower()
        
        # Ищем пользователя
        user = sql.execute("SELECT user_id, username FROM users WHERE username = ?", (username,)).fetchone()
        if not user:
            await msg.answer(f"❌ Пользователь @{username} не найден в базе")
            return
        
        user_id = user[0]
        user_username = user[1]
        
        # ===== ОТБОР ТИТУЛА =====
        if action == "титул":
            sql.execute("UPDATE users SET current_title = '' WHERE user_id = ?", (user_id,))
            db.commit()
            await msg.answer(f"✅ У @{user_username} отобран титул")
            try:
                await bot.send_message(user_id, "👑 Администратор отобрал ваш титул!")
            except:
                pass
            return
        
        # ===== ОТБОР СТАТУСА =====
        if action == "статус":
            sql.execute("UPDATE users SET current_status = 'На охоте🏹' WHERE user_id = ?", (user_id,))
            db.commit()
            await msg.answer(f"✅ У @{user_username} отобран статус (установлен стандартный)")
            try:
                await bot.send_message(user_id, "🏷️ Администратор отобрал ваш статус!")
            except:
                pass
            return
        
        # ===== ОТБОР ЦИТАТЫ =====
        if action == "цитата":
            sql.execute("UPDATE users SET current_quote = 'Я начинающий охотник, и я иду к своей цели' WHERE user_id = ?", (user_id,))
            db.commit()
            await msg.answer(f"✅ У @{user_username} отобрана цитата (установлена стандартная)")
            try:
                await bot.send_message(user_id, "💬 Администратор отобрал вашу цитату!")
            except:
                pass
            return
        
        # ===== ОТБОР СНАРЯЖЕНИЯ =====
        if action == "снаряжение":
            if len(parts) < 4:
                await msg.answer("❌ Укажите название снаряжения в кавычках\nПример: дипотбор @user снаряжение \"Рюкзак\"")
                return
            
            item_name = parts[3].strip('"\'')
            
            # Проверяем, есть ли такой предмет в EQUIPMENT
            if item_name not in EQUIPMENT:
                await msg.answer(f"❌ Снаряжение '{item_name}' не найдено в игре")
                return
            
            # Проверяем, есть ли предмет у игрока
            owned = sql.execute("SELECT 1 FROM user_equipment WHERE user_id = ? AND equipment = ?", 
                               (user_id, item_name)).fetchone()
            
            if not owned:
                await msg.answer(f"❌ У @{user_username} нет снаряжения '{item_name}'")
                return
            
            # Отбираем
            sql.execute("DELETE FROM user_equipment WHERE user_id = ? AND equipment = ?", (user_id, item_name))
            
            # Если отбираем рюкзак, обновляем максимальное здоровье
            if item_name == "Рюкзак":
                update_max_health(user_id)
            
            db.commit()
            await msg.answer(f"✅ У @{user_username} отобрано снаряжение '{item_name}'")
            try:
                await bot.send_message(user_id, f"🎩 Администратор отобрал у вас снаряжение: {item_name}")
            except:
                pass
            return
        
        # ===== ОТБОР ПРЕДМЕТА ВЫЖИВАНИЯ =====
        if action == "предмет":
            if len(parts) < 4:
                await msg.answer("❌ Укажите название предмета в кавычках\nПример: дипотбор @user предмет \"Фляга с водой\"")
                return
            
            item_name = parts[3].strip('"\'')
            
            # Проверяем, есть ли такой предмет в SURVIVAL_ITEMS
            if item_name not in SURVIVAL_ITEMS:
                await msg.answer(f"❌ Предмет '{item_name}' не найден в игре")
                return
            
            # Проверяем, есть ли предмет у игрока
            owned = sql.execute("SELECT 1 FROM survival_items WHERE user_id = ? AND item_name = ?", 
                               (user_id, item_name)).fetchone()
            
            if not owned:
                await msg.answer(f"❌ У @{user_username} нет предмета '{item_name}'")
                return
            
            # Отбираем
            sql.execute("DELETE FROM survival_items WHERE user_id = ? AND item_name = ?", (user_id, item_name))
            db.commit()
            await msg.answer(f"✅ У @{user_username} отобран предмет '{item_name}'")
            try:
                await bot.send_message(user_id, f"🛡️ Администратор отобрал у вас предмет: {item_name}")
            except:
                pass
            return
        
        # ===== ОТБОР ЯИЦ (ивент) =====
        if action == "яйца":
            if len(parts) < 4:
                await msg.answer("❌ Укажите количество яиц\nПример: дипотбор @user яйца 50")
                return
            
            try:
                amount = int(parts[3])
                if amount <= 0:
                    await msg.answer("❌ Количество должно быть больше 0")
                    return
            except ValueError:
                await msg.answer("❌ Количество должно быть числом")
                return
            
            current = sql.execute("SELECT event_eggs FROM users WHERE user_id = ?", (user_id,)).fetchone()
            current_eggs = current[0] if current else 0
            
            if current_eggs < amount:
                await msg.answer(f"❌ У @{user_username} только {current_eggs} яиц, нельзя отобрать {amount}")
                return
            
            sql.execute("UPDATE users SET event_eggs = event_eggs - ? WHERE user_id = ?", (amount, user_id))
            sql.execute("UPDATE event_top SET eggs = eggs - ? WHERE user_id = ?", (amount, user_id))
            db.commit()
            
            await msg.answer(f"✅ У @{user_username} отобрано {amount} яиц\nБыло: {current_eggs} → Стало: {current_eggs - amount}")
            try:
                await bot.send_message(user_id, f"🥚 Администратор отобрал у вас {amount} яиц!")
            except:
                pass
            return
        
        # ===== ОТБОР МОНЕТ =====
        if action == "монеты":
            if len(parts) < 4:
                await msg.answer("❌ Укажите количество монет\nПример: дипотбор @user монеты 1000")
                return
            
            try:
                amount = int(parts[3])
                if amount <= 0:
                    await msg.answer("❌ Количество должно быть больше 0")
                    return
            except ValueError:
                await msg.answer("❌ Количество должно быть числом")
                return
            
            current = sql.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,)).fetchone()
            current_coins = current[0] if current else 0
            
            if current_coins < amount:
                await msg.answer(f"❌ У @{user_username} только {current_coins} монет, нельзя отобрать {amount}")
                return
            
            sql.execute("UPDATE users SET coins = coins - ? WHERE user_id = ?", (amount, user_id))
            db.commit()
            
            await msg.answer(f"✅ У @{user_username} отобрано {amount} монет\nБыло: {current_coins} → Стало: {current_coins - amount}")
            try:
                await bot.send_message(user_id, f"💰 Администратор отобрал у вас {amount} монет!")
            except:
                pass
            return
        
        # ===== ОТБОР ОПЫТА =====
        if action == "опыт":
            if len(parts) < 4:
                await msg.answer("❌ Укажите количество опыта\nПример: дипотбор @user опыт 500")
                return
            
            try:
                amount = int(parts[3])
                if amount <= 0:
                    await msg.answer("❌ Количество должно быть больше 0")
                    return
            except ValueError:
                await msg.answer("❌ Количество должно быть числом")
                return
            
            current = sql.execute("SELECT exp FROM users WHERE user_id = ?", (user_id,)).fetchone()
            current_exp = current[0] if current else 0
            
            if current_exp < amount:
                await msg.answer(f"❌ У @{user_username} только {current_exp} опыта, нельзя отобрать {amount}")
                return
            
            sql.execute("UPDATE users SET exp = exp - ? WHERE user_id = ?", (amount, user_id))
            db.commit()
            
            await msg.answer(f"✅ У @{user_username} отобрано {amount} опыта\nБыло: {current_exp} → Стало: {current_exp - amount}")
            try:
                await bot.send_message(user_id, f"⭐ Администратор отобрал у вас {amount} опыта!")
            except:
                pass
            return
        
        # ===== ОТБОР УРОВНЕЙ (уменьшение опыта) =====
        if action == "уровни":
            if len(parts) < 4:
                await msg.answer("❌ Укажите количество уровней\nПример: дипотбор @user уровни 5")
                return
            
            try:
                levels = int(parts[3])
                if levels <= 0:
                    await msg.answer("❌ Количество должно быть больше 0")
                    return
            except ValueError:
                await msg.answer("❌ Количество должно быть числом")
                return
            
            exp_to_remove = levels * EXP_PER_LEVEL
            
            current = sql.execute("SELECT exp FROM users WHERE user_id = ?", (user_id,)).fetchone()
            current_exp = current[0] if current else 0
            
            if current_exp < exp_to_remove:
                await msg.answer(f"❌ У @{user_username} недостаточно опыта для снятия {levels} уровней")
                return
            
            sql.execute("UPDATE users SET exp = exp - ? WHERE user_id = ?", (exp_to_remove, user_id))
            db.commit()
            
            await msg.answer(f"✅ У @{user_username} отобрано {levels} уровней ({exp_to_remove} опыта)")
            try:
                await bot.send_message(user_id, f"📉 Администратор отобрал у вас {levels} уровней!")
            except:
                pass
            return
        
        # ===== ОТБОР ОРУЖИЯ =====
        if action == "оружие":
            if len(parts) < 4:
                await msg.answer("❌ Укажите название оружия в кавычках\nПример: дипотбор @user оружие \"Снайперка\"")
                return
            
            weapon_name = parts[3].strip('"\'')
            
            # Проверяем, есть ли такое оружие в WEAPONS
            if weapon_name not in WEAPONS_DATA:
                await msg.answer(f"❌ Оружие '{weapon_name}' не найдено в игре")
                return
            
            # Нельзя отобрать револьвер (стартовое оружие)
            if weapon_name == "Револьвер":
                await msg.answer("❌ Нельзя отобрать стартовое оружие 'Револьвер'")
                return
            
            # Проверяем, есть ли оружие у игрока
            owned = sql.execute("SELECT 1 FROM user_weapons WHERE user_id = ? AND weapon = ?", 
                               (user_id, weapon_name)).fetchone()
            
            if not owned:
                await msg.answer(f"❌ У @{user_username} нет оружия '{weapon_name}'")
                return
            
            # Проверяем, не экипировано ли оно сейчас
            current_weapon = sql.execute("SELECT weapon FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if current_weapon and current_weapon[0] == weapon_name:
                # Меняем на револьвер
                sql.execute("UPDATE users SET weapon = 'Револьвер' WHERE user_id = ?", (user_id,))
            
            # Отбираем
            sql.execute("DELETE FROM user_weapons WHERE user_id = ? AND weapon = ?", (user_id, weapon_name))
            db.commit()
            
            await msg.answer(f"✅ У @{user_username} отобрано оружие '{weapon_name}'")
            try:
                await bot.send_message(user_id, f"🔫 Администратор отобрал у вас оружие: {weapon_name}")
            except:
                pass
            return
        
        await msg.answer(f"❌ Неизвестная команда: {action}\nДоступно: титул, статус, цитата, снаряжение, предмет, яйца, монеты, опыт, уровни, оружие")
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")
        
@dp.message(lambda msg: msg.text and msg.text.startswith("дипресчетполный"))
async def admin_full_recalc(msg: Message):
    """Полностью пересчитать location_stats из trophies для всех игроков"""
    try:
        # ПРОВЕРКА НА АДМИНА - ОБЯЗАТЕЛЬНО
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды!\n\n"
                           "Эта команда доступна только администратору бота.")
            return
        
        await msg.answer("🔄 ПОЛНЫЙ ПЕРЕСЧЕТ СТАТИСТИКИ ДЛЯ ВСЕХ ИГРОКОВ...\n⏳ Это может занять время, пожалуйста, подождите.")
        
        users = sql.execute("SELECT user_id FROM users").fetchall()
        total_users = len(users)
        
        for (user_id,) in users:
            # Очищаем старую статистику
            sql.execute("DELETE FROM location_stats WHERE user_id = ?", (user_id,))
            
            # Получаем трофеи
            trophies = sql.execute("SELECT animal, count FROM trophies WHERE user_id = ?", (user_id,)).fetchall()
            
            # Пересчитываем
            location_kills = {}
            for animal, count in trophies:
                for loc_name, loc_data in LOCATIONS.items():
                    found = False
                    for animals_list in loc_data["animals"].values():
                        if animal in animals_list:
                            location_kills[loc_name] = location_kills.get(loc_name, 0) + count
                            found = True
                            break
                    if found:
                        break
            
            # Сохраняем
            for loc_name, kills in location_kills.items():
                sql.execute("INSERT INTO location_stats (user_id, location, kills) VALUES (?, ?, ?)",
                           (user_id, loc_name, kills))
            
            # Обновляем total_kills
            total = sum(location_kills.values())
            sql.execute("UPDATE users SET total_kills = ? WHERE user_id = ?", (total, user_id))
            
            # Очищаем достижения локаций
            sql.execute("DELETE FROM location_achievements WHERE user_id = ?", (user_id,))
            
            db.commit()
        
        await msg.answer(f"✅ ПЕРЕСЧЕТ ЗАВЕРШЕН!\n\n"
                        f"📊 Обработано игроков: {total_users}\n"
                        f"⚠️ Достижения локаций сброшены у всех игроков.\n"
                        f"✅ Они выдадутся заново при достижении условий (60/250 убийств).")
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка при пересчете: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.lower().startswith("дипиввал"))
async def admin_event_currency(msg: Message):
    """Выдать ивентовую валюту (яйца) игроку
    Форматы:
    дипиввал @username количество
    дипиввал алл количество
    Пример: дипиввал @krrgrg 100
    """
    try:
        # Проверка прав админа
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        # Проверка активности ивента
        if not EVENT_ACTIVE:
            await msg.answer("❌ Ивент не активен! Сначала включите EVENT_ACTIVE = True")
            return
        
        parts = msg.text.split()
        
        if len(parts) < 3:
            await msg.answer("❌ Используйте:\n"
                           "дипиввал @username количество\n"
                           "дипиввал алл количество\n"
                           "Пример: дипиввал @krrgrg 100")
            return
        
        # Парсим количество
        try:
            amount = int(parts[2])
            if amount <= 0:
                await msg.answer("❌ Количество должно быть больше 0")
                return
            if amount > 10000:
                await msg.answer("❌ Максимальное количество за раз - 10000")
                return
        except ValueError:
            await msg.answer("❌ Количество должно быть числом")
            return
        
        # ===== ВАРИАНТ: ВСЕМ ИГРОКАМ =====
        if parts[1].lower() == "алл":
            all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
            
            if not all_users:
                await msg.answer("❌ Нет зарегистрированных пользователей!")
                return
            
            success_count = 0
            total_eggs_given = 0
            
            await msg.answer(f"📤 Выдаю {amount} {EVENT_CURRENCY} {len(all_users)} игрокам...")
            
            for user_id, username in all_users:
                try:
                    new_eggs, completed, quest_num, quest_data, rewards = add_event_egg(user_id, amount)
                    total_eggs_given += amount
                    success_count += 1
                    
                    # Уведомляем игрока в ЛС
                    try:
                        await bot.send_message(user_id, f"🎁 Администратор выдал всем игрокам {amount} {EVENT_CURRENCY}!\n"
                                                       f"Теперь у вас: {new_eggs} {EVENT_CURRENCY}")
                    except:
                        pass
                    
                    await asyncio.sleep(0.05)  # небольшая задержка
                    
                except Exception as e:
                    print(f"Ошибка при выдаче игроку {user_id}: {e}")
            
            await msg.answer(f"✅ Выдано {amount} {EVENT_CURRENCY} {success_count} игрокам!\n"
                           f"📊 Всего выдано: {total_eggs_given} {EVENT_CURRENCY}")
            
            print(f"🔧 Админ {msg.from_user.id} выдал {amount} {EVENT_CURRENCY} ВСЕМ игрокам")
            return
        
        # ===== ВАРИАНТ: КОНКРЕТНОМУ ИГРОКУ =====
        username_part = parts[1]
        if not username_part.startswith("@"):
            await msg.answer("❌ Укажите @username\nПример: дипиввал @krrgrg 100")
            return
        
        username = username_part[1:].strip()
        
        # Ищем пользователя
        user = sql.execute("SELECT user_id, username FROM users WHERE username = ?", (username,)).fetchone()
        
        if not user:
            await msg.answer(f"❌ Пользователь @{username} не найден в базе!")
            return
        
        user_id = user[0]
        user_username = user[1]
        
        # Получаем текущее количество яиц
        current_eggs = sql.execute("SELECT event_eggs FROM users WHERE user_id = ?", (user_id,)).fetchone()
        current_eggs = current_eggs[0] if current_eggs else 0
        
        # Добавляем яйца
        new_eggs, completed, quest_num, quest_data, rewards = add_event_egg(user_id, amount)
        
        # Проверяем задания (автоматически)
        rewards_text = ""
        if completed and rewards:
            rewards_text = f"\n\n🎉 Задание {quest_num} выполнено!\n" + "\n".join(rewards)
        
        await msg.answer(f"✅ Пользователю @{user_username} выдано {amount} {EVENT_CURRENCY}!\n\n"
                        f"Было: {current_eggs}\n"
                        f"Стало: {new_eggs}{rewards_text}")
        
        # Уведомляем игрока в ЛС
        try:
            await bot.send_message(user_id, f"🎁 Администратор выдал вам {amount} {EVENT_CURRENCY}!\n"
                                           f"Теперь у вас: {new_eggs} {EVENT_CURRENCY}")
        except:
            pass
        
        print(f"🔧 Админ {msg.from_user.id} выдал {amount} {EVENT_CURRENCY} @{user_username}")
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")
        
@dp.message(lambda msg: msg.text and msg.text.startswith("дипглаз"))
async def admin_view_inventory(msg: Message):
    """Показать полный инвентарь игрока (админ-команда)
    Формат: дипглаз @username
    """
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        parts = msg.text.split()
        if len(parts) < 2:
            await msg.answer("❌ Используйте: дипглаз @username")
            return
        
        username = parts[1].replace("@", "").strip()
        
        # Ищем пользователя
        user_data = sql.execute("SELECT user_id, username, coins, exp, weapon, location, total_kills, current_title, prestige, health, max_health, deaths, event_eggs FROM users WHERE username = ?", 
                               (username,)).fetchone()
        
        if not user_data:
            await msg.answer(f"❌ Пользователь @{username} не найден")
            return
        
        user_id = user_data[0]
        user_name = user_data[1]
        coins = user_data[2]
        exp = user_data[3]
        weapon = user_data[4]
        location = user_data[5]
        total_kills = user_data[6]
        current_title = user_data[7] or "❌ нет"
        prestige = user_data[8] or 0
        current_hp = user_data[9]
        max_hp = user_data[10]
        deaths = user_data[11] or 0
        event_eggs = user_data[12] or 0
        
        level = get_level(exp)
        
        # Получаем снаряжение
        equipment = get_user_equipment(user_id)
        equipment_str = ", ".join(equipment) if equipment else "❌ нет"
        
        # Получаем оружие
        weapons = sql.execute("SELECT weapon FROM user_weapons WHERE user_id = ?", (user_id,)).fetchall()
        weapons_str = ", ".join([w[0] for w in weapons]) if weapons else "Револьвер"
        
        # Получаем предметы выживания
        survival_items = get_user_survival_items(user_id)
        survival_str = ", ".join(survival_items) if survival_items else "❌ нет"
        
        # Получаем баффы
        buffs_data = sql.execute("SELECT golden_bullet, diamond_bullet, immortality_staff FROM users WHERE user_id = ?", (user_id,)).fetchone()
        golden = buffs_data[0] if buffs_data else 0
        diamond = buffs_data[1] if buffs_data else 0
        staff = buffs_data[2] if buffs_data else 0
        
        # Получаем достижения (обычные)
        completed = get_completed_achievements(user_id)
        achievements_done = list(completed.keys()) if completed else []
        
        # Получаем достижения локаций
        loc_achievements = sql.execute("SELECT location, achievement_type FROM location_achievements WHERE user_id = ? AND completed = 1", 
                                       (user_id,)).fetchall()
        
        # Группируем достижения локаций
        loc_60 = []
        loc_250 = []
        loc_all = []
        
        for loc, ach_type in loc_achievements:
            if ach_type == "60_kills":
                loc_60.append(loc)
            elif ach_type == "250_kills":
                loc_250.append(loc)
            elif ach_type == "all_species":
                loc_all.append(loc)
        
        # Проверяем локации, где 90%+ но достижение ещё не выдано
        loc_near_90 = []
        for location_name, location_data in LOCATIONS.items():
            if location_name in loc_all:
                continue
            
            # Получаем всех животных в локации
            all_animals = []
            for animals_list in location_data["animals"].values():
                all_animals.extend(animals_list)
            
            total_animals = len(all_animals)
            if total_animals == 0:
                continue
            
            required_count = (total_animals * 9 + 9) // 10  # 90% округление вверх
            
            # Получаем убитых животных
            killed_animals = sql.execute("SELECT DISTINCT animal FROM trophies WHERE user_id = ?", (user_id,)).fetchall()
            killed_animals = [a[0] for a in killed_animals]
            
            killed_count = sum(1 for a in all_animals if a in killed_animals)
            
            if killed_count >= required_count:
                percent = int(killed_count / total_animals * 100)
                loc_near_90.append(f"{location_name} ({killed_count}/{total_animals} - {percent}%)")
        
        # Получаем статистику убийств по локациям
        location_stats = sql.execute("SELECT location, kills FROM location_stats WHERE user_id = ? ORDER BY kills DESC", (user_id,)).fetchall()
        
        loc_stats_str = ""
        for loc, kills in location_stats[:10]:
            has_60 = "✅" if loc in loc_60 else ("⏳" if kills >= 60 else "❌")
            has_250 = "✅" if loc in loc_250 else ("⏳" if kills >= 250 else "❌")
            has_all = "✅" if loc in loc_all else "❌"
            loc_stats_str += f"• {loc}: {kills} убийств [60:{has_60} | 250:{has_250} | 90% видов:{has_all}]\n"
        
        if not location_stats:
            loc_stats_str = "❌ нет данных"
        
        # Получаем топ животных по убийствам
        top_animals = sql.execute("SELECT animal, count FROM trophies WHERE user_id = ? ORDER BY count DESC LIMIT 10", (user_id,)).fetchall()
        animals_str = ""
        for animal, count in top_animals:
            animals_str += f"• {animal}: {count}\n"
        
        if not top_animals:
            animals_str = "❌ нет данных"
        
        # Получаем текущий статус и цитату
        status_quote = sql.execute("SELECT current_status, current_quote FROM users WHERE user_id = ?", (user_id,)).fetchone()
        current_status = status_quote[0] if status_quote and status_quote[0] else "На охоте🏹"
        current_quote = status_quote[1] if status_quote and status_quote[1] else "Я начинающий охотник, и я иду к своей цели"
        
        # ========== ВСЕ ДОСТУПНЫЕ ТИТУЛЫ У ИГРОКА ==========
        load_custom_items()
        
        # Получаем ID титулов, которые есть у игрока
        available_title_ids = []
        
        # Титулы из достижений
        for ach_name, ach_data in ACHIEVEMENTS.items():
            if ach_name in completed and ach_data.get('title'):
                for tid, title in TITLES_DICT.items():
                    if title == ach_data['title']:
                        available_title_ids.append(tid)
                        break
        
        # Титулы из локаций
        for loc, ach_type in loc_achievements:
            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(loc, {}).get(ach_type, {})
            if ach_data.get('title'):
                for tid, title in TITLES_DICT.items():
                    if title == ach_data['title']:
                        available_title_ids.append(tid)
                        break
        
        available_title_ids = list(set(available_title_ids))
        available_titles = [TITLES_DICT[tid] for tid in available_title_ids if tid in TITLES_DICT]
        
        # ========== ВСЕ ДОСТУПНЫЕ СТАТУСЫ У ИГРОКА ==========
        available_status_ids = []
        
        # Статусы из локаций
        for loc, ach_type in loc_achievements:
            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(loc, {}).get(ach_type, {})
            if ach_data.get('status'):
                for sid, status in STATUSES_DICT.items():
                    if status == ach_data['status']:
                        available_status_ids.append(sid)
                        break
        
        # Базовые статусы всегда доступны
        for sid, status in STATUSES_DICT.items():
            if status in ["На охоте🏹", "Дома🏠"]:
                available_status_ids.append(sid)
        
        available_status_ids = list(set(available_status_ids))
        available_statuses = [STATUSES_DICT[sid] for sid in available_status_ids if sid in STATUSES_DICT]
        
        # ========== ВСЕ ДОСТУПНЫЕ ЦИТАТЫ У ИГРОКА ==========
        available_quote_ids = []
        
        # Цитаты из локаций
        for loc, ach_type in loc_achievements:
            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(loc, {}).get(ach_type, {})
            if ach_data.get('quote'):
                for qid, quote in QUOTES_DICT.items():
                    if quote == ach_data['quote']:
                        available_quote_ids.append(qid)
                        break
        
        # Базовая цитата всегда доступна
        for qid, quote in QUOTES_DICT.items():
            if quote == "Я начинающий охотник, и я иду к своей цели":
                available_quote_ids.append(qid)
                break
        
        available_quote_ids = list(set(available_quote_ids))
        available_quotes = [QUOTES_DICT[qid] for qid in available_quote_ids if qid in QUOTES_DICT]
        
        # Формируем ответ
        text = f"👁️ **ИНВЕНТАРЬ ИГРОКА**\n\n"
        text += f"🎮 **@{user_name}**\n"
        text += f"🏷️ Текущий титул: {current_title}\n"
        text += f"💬 Текущая цитата: {current_quote}\n"
        text += f"🏷️ Текущий статус: {current_status}\n"
        text += f"⭐ Уровень: {level} | Престиж: {prestige}\n"
        text += f"❤️ Здоровье: {current_hp}/{max_hp}\n"
        text += f"💀 Смертей: {deaths}\n"
        text += f"💰 Монеты: {coins}\n"
        text += f"🎯 Всего убийств: {total_kills}\n"
        text += f"🔫 Оружие: {weapon}\n"
        text += f"📍 Локация: {location}\n"
        
        if EVENT_ACTIVE:
            text += f"🥚 {EVENT_CURRENCY}: {event_eggs}\n"
        
        text += f"\n🎩 **Снаряжение:**\n{equipment_str}\n"
        text += f"\n🔫 **Доступное оружие:**\n{weapons_str}\n"
        text += f"\n🛡️ **Выживание:**\n{survival_str}\n"
        text += f"\n⚡ **Баффы:**\n"
        text += f"• Золотые пули: {golden}\n"
        text += f"• Алмазные пули: {diamond}\n"
        text += f"• Посохи бессмертия: {staff}\n"
        
        text += f"\n🏆 **Достижения ({len(achievements_done)}/{len(ACHIEVEMENTS)}):**\n"
        if achievements_done:
            text += "• " + "\n• ".join(achievements_done)
        else:
            text += "❌ нет"
        
        text += f"\n\n👑 **Все доступные титулы ({len(available_titles)}):**\n"
        if available_titles:
            text += "• " + "\n• ".join(available_titles)
        else:
            text += "❌ нет"
        
        text += f"\n\n🏷️ **Все доступные статусы ({len(available_statuses)}):**\n"
        if available_statuses:
            text += "• " + "\n• ".join(available_statuses)
        else:
            text += "❌ нет"
        
        text += f"\n\n💬 **Все доступные цитаты ({len(available_quotes)}):**\n"
        if available_quotes:
            short_quotes = []
            for q in available_quotes:
                if len(q) > 60:
                    short_quotes.append(q[:57] + "...")
                else:
                    short_quotes.append(q)
            text += "• " + "\n• ".join(short_quotes)
        else:
            text += "❌ нет"
        
        text += f"\n\n🗺️ **Достижения локаций:**\n"
        text += f"• 60 убийств: {', '.join(loc_60) if loc_60 else '❌ нет'}\n"
        text += f"• 250 убийств: {', '.join(loc_250) if loc_250 else '❌ нет'}\n"
        text += f"• 90% видов: {', '.join(loc_all) if loc_all else '❌ нет'}\n"
        
        if loc_near_90:
            text += f"\n⏳ **Готово к выдаче (нужен 1 хант):**\n"
            for loc_info in loc_near_90:
                text += f"   • {loc_info}\n"
        
        text += f"\n📊 **Статистика по локациям (топ-10):**\n{loc_stats_str}\n"
        text += f"\n🐾 **Топ животных (по количеству):**\n{animals_str}"
        
        # Отправляем сообщение (разбиваем если слишком длинное)
        if len(text) > 4000:
            parts_text = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for i, part in enumerate(parts_text):
                await msg.answer(part)
        else:
            await msg.answer(text)
            
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")
        import traceback
        traceback.print_exc()

@dp.message(lambda msg: msg.text and msg.text.startswith("дипоткат250"))
async def admin_revoke_250_achievements(msg: Message):
    """Отозвать все неправильно выданные достижения 250_kills
    Формат: дипоткат250
    """
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        # Получаем все достижения 250_kills
        achievements = sql.execute("SELECT user_id, location, completed_at FROM location_achievements WHERE achievement_type = '250_kills' AND completed = 1").fetchall()
        
        if not achievements:
            await msg.answer("❌ Нет выданных достижений 250_kills")
            return
        
        revoked_count = 0
        
        for user_id, location, completed_at in achievements:
            # Проверяем реальное количество убийств в локации
            stats = sql.execute("SELECT kills FROM location_stats WHERE user_id = ? AND location = ?", 
                               (user_id, location)).fetchone()
            kills = stats[0] if stats else 0
            
            # Если убийств меньше 250 - отзываем достижение
            if kills < 250:
                sql.execute("DELETE FROM location_achievements WHERE user_id = ? AND location = ? AND achievement_type = '250_kills'",
                           (user_id, location))
                revoked_count += 1
                
                # Уведомляем игрока
                try:
                    await bot.send_message(user_id, f"⚠️ Достижение '250 убийств' в локации {location} было отозвано администратором, так как оно было выдано ошибочно.\n"
                                           f"📊 Ваш реальный прогресс: {kills}/250 убийств")
                except:
                    pass
        
        db.commit()
        
        await msg.answer(f"✅ Отозвано {revoked_count} ошибочно выданных достижений 250_kills")
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.lower().startswith("дипхант"))
async def admin_force_animal(msg: Message):
    """Принудительно задать животное для игрока (игнорирует локацию)
    
    Форматы:
    дипхант животное @username - задать животное
    дипхант офф @username - отключить принудительное животное
    дипхант список - показать всех с принудительным животным
    
    Пример: дипхант Тираннозавр @DeepSleep01
    """
    try:
        # Проверка прав админа
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        parts = msg.text.split(maxsplit=2)
        
        if len(parts) < 2:
            await msg.answer(
                "❌ Используйте:\n"
                "дипхант животное @username - задать животное\n"
                "дипхант офф @username - отключить\n"
                "дипхант список - показать всех\n\n"
                "Пример: дипхант Тираннозавр @DeepSleep01"
            )
            return
        
        command = parts[1].lower()
        
        # ===== СПИСОК ВСЕХ =====
        if command == "список":
            forced = sql.execute("""
                SELECT u.user_id, u.username, af.animal_name 
                FROM admin_forced_animal af
                JOIN users u ON u.user_id = af.user_id
                WHERE af.enabled = 1
            """).fetchall()
            
            if not forced:
                await msg.answer("📋 Список пуст — никто не использует принудительное животное.")
                return
            
            text = "📋 **Игроки с принудительным животным:**\n\n"
            for user_id, username, animal in forced:
                text += f"• @{username} — {animal}\n"
            
            await msg.answer(text, parse_mode="Markdown")
            return
        
        # ===== ОТКЛЮЧЕНИЕ =====
        if command == "офф":
            if len(parts) < 3:
                await msg.answer("❌ Укажите @username\nПример: дипхант офф @DeepSleep01")
                return
            
            username = parts[2].replace("@", "").strip()
            user = sql.execute("SELECT user_id, username FROM users WHERE username = ?", (username,)).fetchone()
            
            if not user:
                await msg.answer(f"❌ Пользователь @{username} не найден")
                return
            
            sql.execute("DELETE FROM admin_forced_animal WHERE user_id = ?", (user[0],))
            db.commit()
            
            await msg.answer(f"✅ Принудительное животное отключено для @{username}")
            try:
                await bot.send_message(user[0], "🔄 Администратор отключил принудительное животное. Теперь охота работает как обычно.")
            except:
                pass
            return
        
        # ===== УСТАНОВКА ЖИВОТНОГО =====
        # Формат: дипхант животное @username
        if len(parts) < 3:
            await msg.answer("❌ Укажите животное и @username\nПример: дипхант Тираннозавр @DeepSleep01")
            return
        
        animal_name = parts[1].strip()
        username_part = parts[2].strip()
        
        if not username_part.startswith("@"):
            await msg.answer("❌ Укажите @username\nПример: дипхант Тираннозавр @DeepSleep01")
            return
        
        username = username_part[1:].strip()
        
        # Ищем пользователя
        user = sql.execute("SELECT user_id, username FROM users WHERE username = ?", (username,)).fetchone()
        if not user:
            await msg.answer(f"❌ Пользователь @{username} не найден")
            return
        
        user_id = user[0]
        user_username = user[1]
        
        # Проверяем, существует ли такое животное в игре
        animal_exists = False
        found_location = None
        found_group = None
        
        for loc_name, loc_data in LOCATIONS.items():
            for group_name, animals_list in loc_data["animals"].items():
                if animal_name in animals_list:
                    animal_exists = True
                    found_location = loc_name
                    found_group = group_name
                    break
            if animal_exists:
                break
        
        if not animal_exists:
            # Показываем похожие животные
            all_animals = []
            for loc_data in LOCATIONS.values():
                for animals_list in loc_data["animals"].values():
                    all_animals.extend(animals_list)
            
            similar = [a for a in all_animals if animal_name.lower() in a.lower()][:10]
            
            if similar:
                await msg.answer(f"❌ Животное '{animal_name}' не найдено!\n\nВозможно, вы имели в виду:\n• " + "\n• ".join(similar))
            else:
                await msg.answer(f"❌ Животное '{animal_name}' не найдено в игре!\n\nДоступно более {len(all_animals)} животных.")
            return
        
        # Сохраняем в БД
        sql.execute("""
            INSERT OR REPLACE INTO admin_forced_animal (user_id, animal_name, enabled)
            VALUES (?, ?, 1)
        """, (user_id, animal_name))
        db.commit()
        
        await msg.answer(
            f"✅ **Принудительное животное установлено!**\n\n"
            f"👤 Игрок: @{user_username}\n"
            f"🐾 Животное: {animal_name}\n"
            f"📍 Локация: {found_location} ({found_group})\n\n"
            f"⚠️ Теперь при каждой охоте этому игроку будет попадаться ТОЛЬКО {animal_name}.\n"
            f"🔄 Чтобы отключить: дипхант офф @{user_username}"
        )
        
        # Уведомляем игрока
        try:
            await bot.send_message(
                user_id,
                f"⚠️ **Внимание!** Администратор изменил вашу охоту.\n\n"
                f"🐾 Теперь при каждой охоте вам будет попадаться **{animal_name}**.\n"
                f"📍 Локация не важна — это животное будет появляться везде.\n\n"
                f"🔄 Чтобы вернуть нормальную охоту, обратитесь к администратору.",
                parse_mode="Markdown"
            )
        except:
            pass
        
        print(f"🔧 Админ {msg.from_user.id} установил принудительное животное {animal_name} для @{user_username}")
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипчек"))
async def admin_check_all_achievements(msg: Message):
    """Проверить и выдать пропущенные награды за достижения локаций ВСЕМ игрокам"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        await msg.answer("🔄 Начинаю проверку достижений у всех игроков...")
        
        users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
        
        total_fixed = 0
        
        for user_id, username in users:
            fixed_for_user = 0
            
            for location_name, location_data in LOCATIONS.items():
                # Получаем РЕАЛЬНОЕ количество убийств из location_stats
                stats = sql.execute("SELECT kills FROM location_stats WHERE user_id = ? AND location = ?", 
                                   (user_id, location_name)).fetchone()
                kills = stats[0] if stats else 0
                
                if kills == 0:
                    continue
                
                # Проверяем 60 убийств
                if kills >= 60:
                    existing = sql.execute("SELECT completed FROM location_achievements WHERE user_id = ? AND location = ? AND achievement_type = '60_kills'",
                                           (user_id, location_name)).fetchone()
                    if not existing or existing[0] == 0:
                        ach_data = LOCATION_ACHIEVEMENTS_DATA.get(location_name, {}).get("60_kills", {})
                        if ach_data.get("title"):
                            current_title = sql.execute("SELECT current_title FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
                            if not current_title:
                                sql.execute("UPDATE users SET current_title = ? WHERE user_id = ?", (ach_data["title"], user_id))
                        if ach_data.get("coins_reward", 0) > 0:
                            sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (ach_data["coins_reward"], user_id))
                        if ach_data.get("exp_reward", 0) > 0:
                            sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (ach_data["exp_reward"], user_id))
                        
                        sql.execute("INSERT OR REPLACE INTO location_achievements (user_id, location, achievement_type, completed, completed_at) VALUES (?, ?, '60_kills', 1, ?)",
                                   (user_id, location_name, int(time.time())))
                        fixed_for_user += 1
                
                # Проверяем 250 убийств
                if kills >= 250:
                    existing = sql.execute("SELECT completed FROM location_achievements WHERE user_id = ? AND location = ? AND achievement_type = '250_kills'",
                                           (user_id, location_name)).fetchone()
                    if not existing or existing[0] == 0:
                        ach_data = LOCATION_ACHIEVEMENTS_DATA.get(location_name, {}).get("250_kills", {})
                        if ach_data.get("quote"):
                            current_quote = sql.execute("SELECT current_quote FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
                            if not current_quote or current_quote == "Я начинающий охотник, и я иду к своей цели":
                                sql.execute("UPDATE users SET current_quote = ? WHERE user_id = ?", (ach_data["quote"], user_id))
                        if ach_data.get("coins_reward", 0) > 0:
                            sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (ach_data["coins_reward"], user_id))
                        if ach_data.get("exp_reward", 0) > 0:
                            sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (ach_data["exp_reward"], user_id))
                        
                        sql.execute("INSERT OR REPLACE INTO location_achievements (user_id, location, achievement_type, completed, completed_at) VALUES (?, ?, '250_kills', 1, ?)",
                                   (user_id, location_name, int(time.time())))
                        fixed_for_user += 1
                
                # Все виды
                                    # Все виды (90% вместо 100%)
                    existing_all = sql.execute("SELECT completed FROM location_achievements WHERE user_id = ? AND location = ? AND achievement_type = 'all_species'",
                                               (user_id, location_name)).fetchone()
                    if not existing_all or existing_all[0] == 0:
                        all_animals = []
                        for animals_list in location_data["animals"].values():
                            all_animals.extend(animals_list)
                        
                        total_animals = len(all_animals)
                        required_count = (total_animals * 9 + 9) // 10  # 90% округление вверх
                        
                        killed_animals = sql.execute("SELECT DISTINCT animal FROM trophies WHERE user_id = ?", (user_id,)).fetchall()
                        killed_animals = [a[0] for a in killed_animals]
                        
                        killed_count = sum(1 for a in all_animals if a in killed_animals)
                        
                        if killed_count >= required_count:  # <--- 90% вместо 100%
                            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(location_name, {}).get("all_species", {})
                            # ... остальное без изменений
                        if ach_data.get("status"):
                            current_status = sql.execute("SELECT current_status FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
                            if not current_status or current_status == "На охоте🏹":
                                sql.execute("UPDATE users SET current_status = ? WHERE user_id = ?", (ach_data["status"], user_id))
                        if ach_data.get("coins_reward", 0) > 0:
                            sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (ach_data["coins_reward"], user_id))
                        if ach_data.get("exp_reward", 0) > 0:
                            sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (ach_data["exp_reward"], user_id))
                        
                        sql.execute("INSERT OR REPLACE INTO location_achievements (user_id, location, achievement_type, completed, completed_at) VALUES (?, ?, 'all_species', 1, ?)",
                                   (user_id, location_name, int(time.time())))
                        fixed_for_user += 1
            
            if fixed_for_user > 0:
                total_fixed += 1
            
            db.commit()
        
        await msg.answer(f"✅ Готово! Выданы награды {total_fixed} игрокам.")
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипресчет"))
async def admin_recalc_stats(msg: Message):
    """Пересчитать статистику локаций для игрока
    Формат: дипресчет @username
    """
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        parts = msg.text.split()
        if len(parts) < 2:
            await msg.answer("❌ Используйте: дипресчет @username")
            return
        
        username = parts[1].replace("@", "").strip()
        user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
        
        if not user:
            await msg.answer(f"❌ Пользователь @{username} не найден")
            return
        
        user_id = user[0]
        
        # Удаляем старую статистику
        sql.execute("DELETE FROM location_stats WHERE user_id = ?", (user_id,))
        
        # Получаем все трофеи
        trophies = sql.execute("SELECT animal, count FROM trophies WHERE user_id = ?", (user_id,)).fetchall()
        
        # Пересчитываем
        location_kills = {}
        for animal, count in trophies:
            for loc_name, loc_data in LOCATIONS.items():
                for animals_list in loc_data["animals"].values():
                    if animal in animals_list:
                        location_kills[loc_name] = location_kills.get(loc_name, 0) + count
                        break
        
        # Сохраняем
        for loc_name, kills in location_kills.items():
            sql.execute("INSERT INTO location_stats (user_id, location, kills) VALUES (?, ?, ?)",
                       (user_id, loc_name, kills))
        
        db.commit()
        
        # Показываем результат
        result_text = f"✅ Пересчитана статистика для @{username}:\n\n"
        for loc_name, kills in sorted(location_kills.items()):
            result_text += f"📍 {loc_name}: {kills} убийств\n"
        
        await msg.answer(result_text)
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипсброс"))
async def admin_reset_achievements(msg: Message):
    """Сбросить достижения локаций у игрока
    Формат: дипсброс @username
    """
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        parts = msg.text.split()
        if len(parts) < 2:
            await msg.answer("❌ Используйте: дипсброс @username")
            return
        
        username = parts[1].replace("@", "").strip()
        user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
        
        if not user:
            await msg.answer(f"❌ Пользователь @{username} не найден")
            return
        
        user_id = user[0]
        
        # Удаляем достижения
        sql.execute("DELETE FROM location_achievements WHERE user_id = ?", (user_id,))
        
        # Сбрасываем титул, статус, цитату (только если они от достижений)
        sql.execute("UPDATE users SET current_title = '' WHERE user_id = ?", (user_id,))
        sql.execute("UPDATE users SET current_status = 'На охоте🏹' WHERE user_id = ?", (user_id,))
        sql.execute("UPDATE users SET current_quote = 'Я начинающий охотник, и я иду к своей цели' WHERE user_id = ?", (user_id,))
        
        db.commit()
        
        await msg.answer(f"✅ Достижения локаций сброшены для @{username}")
        try:
            await bot.send_message(user_id, "🔄 Ваши достижения локаций были сброшены администратором.")
        except:
            pass
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипфикс"))
async def admin_fix_missing_rewards(msg: Message):
    """Выдать пропущенные награды за достижения локаций
    Форматы:
    дипфикс @username - выдать награды игроку
    дипфикс алл - выдать награды ВСЕМ игрокам
    """
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        parts = msg.text.split()
        
        if len(parts) < 2:
            await msg.answer("❌ Используйте: дипфикс @username\nИли: дипфикс алл")
            return
        
        if parts[1].lower() == "алл":
            # Выдать награды всем
            users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
            success_count = 0
            
            await msg.answer(f"🔄 Обработка {len(users)} игроков...")
            
            for user_id, username in users:
                fixed = await fix_user_achievements(user_id)
                if fixed:
                    success_count += 1
                    await asyncio.sleep(0.1)
            
            await msg.answer(f"✅ Готово! Выданы награды {success_count} игрокам.")
            
        elif "@" in parts[1]:
            username = parts[1].replace("@", "").strip()
            user = sql.execute("SELECT user_id, username FROM users WHERE username = ?", (username,)).fetchone()
            
            if not user:
                await msg.answer(f"❌ Пользователь @{username} не найден")
                return
            
            user_id, user_username = user
            fixed = await fix_user_achievements(user_id)
            
            if fixed:
                await msg.answer(f"✅ Пользователю @{user_username} выданы пропущенные награды!")
                try:
                    await bot.send_message(user_id, "🎉 Вам выданы пропущенные награды за достижения локаций! Проверьте свой профиль.")
                except:
                    pass
            else:
                await msg.answer(f"ℹ️ У пользователя @{user_username} нет пропущенных наград.")
        
        else:
            await msg.answer("❌ Используйте: дипфикс @username\nИли: дипфикс алл")
            
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")


async def fix_user_achievements(user_id: int) -> bool:
    """Проверяет и выдает пропущенные награды за достижения локаций"""
    # Получаем все выполненные достижения пользователя
    achievements = sql.execute(
        "SELECT location, achievement_type FROM location_achievements WHERE user_id = ? AND completed = 1",
        (user_id,)
    ).fetchall()
    
    if not achievements:
        return False
    
    fixed = False
    rewards_given = []
    
    for location, ach_type in achievements:
        ach_data = LOCATION_ACHIEVEMENTS_DATA.get(location, {}).get(ach_type, {})
        
        # Проверяем и выдаём статус
        if ach_data.get("status"):
            current = sql.execute("SELECT current_status FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            if not current or current == "На охоте🏹":
                sql.execute("UPDATE users SET current_status = ? WHERE user_id = ?", (ach_data["status"], user_id))
                rewards_given.append(f"🏷️ Статус: {ach_data['status']} ({location})")
                fixed = True
        
        # Проверяем и выдаём титул
        if ach_data.get("title"):
            current = sql.execute("SELECT current_title FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            if not current:
                sql.execute("UPDATE users SET current_title = ? WHERE user_id = ?", (ach_data["title"], user_id))
                rewards_given.append(f"👑 Титул: {ach_data['title']} ({location})")
                fixed = True
        
        # Проверяем и выдаём цитату
        if ach_data.get("quote"):
            current = sql.execute("SELECT current_quote FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            if not current or current == "Я начинающий охотник, и я иду к своей цели":
                sql.execute("UPDATE users SET current_quote = ? WHERE user_id = ?", (ach_data["quote"], user_id))
                rewards_given.append(f"💬 Цитата ({location})")
                fixed = True
    
    if rewards_given:
        db.commit()
        print(f"🔧 Выданы награды игроку {user_id}: {', '.join(rewards_given)}")
    
    return fixed

@dp.message(lambda msg: msg.text and msg.text.startswith("дипсерия"))
async def admin_reset_streak_timer(msg: Message):
    """Сбросить таймер серии (чтобы можно было снова получить награду)
    Форматы:
    дипсерия @username - сбросить таймер игроку
    дипсерия алл - сбросить таймер ВСЕМ игрокам
    """
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        parts = msg.text.split()
        
        if len(parts) < 2:
            await msg.answer("❌ Используйте: дипсерия @username\nИли: дипсерия алл")
            return
        
        if parts[1].lower() == "алл":
            # Сброс таймера для всех
            sql.execute("UPDATE users SET last_daily_claim = 0")
            db.commit()
            await msg.answer("✅ Таймер серии сброшен для ВСЕХ игроков!")
            print(f"🔧 Админ {msg.from_user.id} сбросил таймер серии для ВСЕХ игроков")
            
            # Уведомляем всех
            all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
            for user_id, username in all_users:
                try:
                    await bot.send_message(user_id, "🔄 Таймер вашей ежедневной серии был сброшен администратором! Можете снова получить награду.")
                except:
                    pass
            return
        
        elif "@" in parts[1]:
            username = parts[1].replace("@", "").strip()
            user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
            
            if not user:
                await msg.answer(f"❌ Пользователь @{username} не найден в базе")
                return
            
            user_id = user[0]
            sql.execute("UPDATE users SET last_daily_claim = 0 WHERE user_id = ?", (user_id,))
            db.commit()
            await msg.answer(f"✅ Таймер серии сброшен для @{username}")
            print(f"🔧 Админ {msg.from_user.id} сбросил таймер серии для @{username}")
            
            # Уведомляем игрока
            try:
                await bot.send_message(user_id, "🔄 Таймер вашей ежедневной серии был сброшен администратором! Можете снова получить награду.")
            except:
                pass
            return
        
        else:
            await msg.answer("❌ Используйте: дипсерия @username\nИли: дипсерия алл")
            
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипмонеты"))
async def admin_coins(msg: Message):
    """Выдать монеты игроку"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        if len(parts) >= 2:
            try:
                amount = int(parts[1])
            except ValueError:
                await msg.answer("❌ Ошибка: количество монет должно быть числом")
                return
                
            if len(parts) >= 3 and parts[2].lower() == "алл":
                # Выдать всем игрокам
                sql.execute("UPDATE users SET coins = coins + ?", (amount,))
                db.commit()
                await msg.answer(f"✅ Выдано {amount} монет ВСЕМ игрокам!")
                print(f"🔧 Админ {msg.from_user.id} выдал {amount} монет ВСЕМ игрокам")
                
                # Уведомляем всех игроков
                all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
                for user_id, username in all_users:
                    try:
                        await bot.send_message(user_id, f"💰 Администратор выдал вам {amount} монет!")
                    except:
                        pass
                        
            elif len(parts) >= 3 and "@" in parts[2]:
                username = parts[2].replace("@", "").strip()
                user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
                if user:
                    sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (amount, user[0]))
                    db.commit()
                    await msg.answer(f"✅ Выдано {amount} монет пользователю @{username}")
                    print(f"🔧 Админ {msg.from_user.id} выдал {amount} монет @{username}")
                    
                    # Уведомляем игрока
                    try:
                        await bot.send_message(user[0], f"💰 Администратор выдал вам {amount} монет!")
                    except:
                        pass
                else:
                    await msg.answer(f"❌ Пользователь @{username} не найден в базе")
            else:
                await msg.answer("❌ Используйте: дипмонеты <сумма> @username\nИли: дипмонеты <сумма> алл - для всех игроков")
        else:
            await msg.answer("❌ Используйте: дипмонеты <сумма> @username\nПример: дипмонеты 500 @player123")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипопыт"))
async def admin_exp(msg: Message):
    """Выдать опыт игроку"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        if len(parts) >= 2:
            try:
                amount = int(parts[1])
            except ValueError:
                await msg.answer("❌ Ошибка: количество опыта должно быть числом")
                return
                
            if len(parts) >= 3 and parts[2].lower() == "алл":
                # Выдать всем игрокам
                sql.execute("UPDATE users SET exp = exp + ?", (amount,))
                db.commit()
                await msg.answer(f"✅ Выдано {amount} опыта ВСЕМ игрокам!")
                print(f"🔧 Админ {msg.from_user.id} выдал {amount} опыта ВСЕМ игрокам")
                
                # Уведомляем всех игроков
                all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
                for user_id, username in all_users:
                    try:
                        await bot.send_message(user_id, f"⭐ Администратор выдал вам {amount} опыта!")
                    except:
                        pass
                        
            elif len(parts) >= 3 and "@" in parts[2]:
                username = parts[2].replace("@", "").strip()
                user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
                if user:
                    sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (amount, user[0]))
                    db.commit()
                    await msg.answer(f"✅ Выдано {amount} опыта пользователю @{username}")
                    print(f"🔧 Админ {msg.from_user.id} выдал {amount} опыта @{username}")
                    
                    # Уведомляем игрока
                    try:
                        await bot.send_message(user[0], f"⭐ Администратор выдал вам {amount} опыта!")
                    except:
                        pass
                else:
                    await msg.answer(f"❌ Пользователь @{username} не найден в базе")
            else:
                await msg.answer("❌ Используйте: дипопыт <сумма> @username\nИли: дипопыт <сумма> алл - для всех игроков")
        else:
            await msg.answer("❌ Используйте: дипопыт <сумма> @username\nПример: дипопыт 1000 @player123")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипуровни"))
async def admin_level(msg: Message):
    """Выдать уровни игроку"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        if len(parts) >= 2:
            try:
                levels = int(parts[1])
            except ValueError:
                await msg.answer("❌ Ошибка: количество уровней должно быть числом")
                return
                
            exp_needed = levels * EXP_PER_LEVEL
            
            if len(parts) >= 3 and parts[2].lower() == "алл":
                # Выдать всем игрокам
                sql.execute("UPDATE users SET exp = exp + ?", (exp_needed,))
                db.commit()
                await msg.answer(f"✅ Выдано {levels} уровней ({exp_needed} опыта) ВСЕМ игрокам!")
                print(f"🔧 Админ {msg.from_user.id} выдал {levels} уровней ВСЕМ игрокам")
                
                # Уведомляем всех игроков
                all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
                for user_id, username in all_users:
                    try:
                        await bot.send_message(user_id, f"📈 Администратор выдал вам {levels} уровней!")
                    except:
                        pass
                        
            elif len(parts) >= 3 and "@" in parts[2]:
                username = parts[2].replace("@", "").strip()
                user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
                if user:
                    sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (exp_needed, user[0]))
                    db.commit()
                    await msg.answer(f"✅ Выдано {levels} уровней ({exp_needed} опыта) пользователю @{username}")
                    print(f"🔧 Админ {msg.from_user.id} выдал {levels} уровни @{username}")
                    
                    # Уведомляем игрока
                    try:
                        await bot.send_message(user[0], f"📈 Администратор выдал вам {levels} уровней!")
                    except:
                        pass
                else:
                    await msg.answer(f"❌ Пользователь @{username} не найден в базе")
            else:
                await msg.answer("❌ Используйте: дипуровни <уровни> @username\nИли: дипуровни <уровни> алл - для всех игроков")
        else:
            await msg.answer("❌ Используйте: дипуровни <уровни> @username\nПример: дипуровни 3 @player123")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипзд"))
async def admin_hp(msg: Message):
    """Установить здоровье игроку"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        if len(parts) >= 2:
            try:
                hp_amount = int(parts[1])
            except ValueError:
                await msg.answer("❌ Ошибка: количество HP должно быть числом")
                return
                
            if len(parts) >= 3 and parts[2].lower() == "алл":
                # Установить всем игрокам
                all_users = sql.execute("SELECT user_id, max_health FROM users").fetchall()
                for user_id, max_hp in all_users:
                    if hp_amount > max_hp:
                        sql.execute("UPDATE users SET health = ? WHERE user_id = ?", (max_hp, user_id))
                    else:
                        sql.execute("UPDATE users SET health = ? WHERE user_id = ?", (hp_amount, user_id))
                db.commit()
                await msg.answer(f"✅ Установлено {hp_amount} HP для ВСЕХ игроков!")
                print(f"🔧 Админ {msg.from_user.id} установил {hp_amount} HP для ВСЕХ игроков")
                
                # Уведомляем всех игроков
                all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
                for user_id, username in all_users:
                    try:
                        await bot.send_message(user_id, f"❤️ Администратор установил вам {hp_amount} HP!")
                    except:
                        pass
                        
            elif len(parts) >= 3 and "@" in parts[2]:
                username = parts[2].replace("@", "").strip()
                user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
                if user:
                    max_hp_result = sql.execute("SELECT max_health FROM users WHERE user_id = ?", (user[0],)).fetchone()
                    max_hp = max_hp_result[0] if max_hp_result else 100
                    
                    if hp_amount > max_hp:
                        hp_amount = max_hp
                    
                    sql.execute("UPDATE users SET health = ? WHERE user_id = ?", (hp_amount, user[0]))
                    db.commit()
                    await msg.answer(f"✅ Установлено {hp_amount} HP для @{username}")
                    print(f"🔧 Админ {msg.from_user.id} установил {hp_amount} HP для @{username}")
                    
                    # Уведомляем игрока
                    try:
                        await bot.send_message(user[0], f"❤️ Администратор установил вам {hp_amount} HP!")
                    except:
                        pass
                else:
                    await msg.answer(f"❌ Пользователь @{username} не найден в базе")
            else:
                await msg.answer("❌ Используйте: дипзд <HP> @username\nИли: дипзд <HP> алл - для всех игроков")
        else:
            await msg.answer("❌ Используйте: дипзд <HP> @username\nПример: дипзд 1000 @player123")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипноль"))
async def admin_reset(msg: Message):
    """Полный сброс профиля игрока"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        if len(parts) >= 2:
            if parts[1].lower() == "алл":
                # Сброс для всех игроков (ОПАСНО!)
                confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="✅ Да, сбросить ВСЕХ", callback_data="confirm_reset_all")],
                    [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_reset")]
                ])
                await msg.answer("⚠️ ВЫ УВЕРЕНЫ, ЧТО ХОТИТЕ СБРОСИТЬ ВСЕХ ИГРОКОВ?\nЭто действие НЕОБРАТИМО!", reply_markup=confirm_kb)
                
            elif "@" in parts[1]:
                username = parts[1].replace("@", "").strip()
                user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
                if user:
                    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="✅ Да, сбросить", callback_data=f"confirm_reset:{user[0]}")],
                        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_reset")]
                    ])
                    await msg.answer(f"⚠️ Вы уверены, что хотите сбросить профиль @{username}?\nЭто действие НЕОБРАТИМО!", reply_markup=confirm_kb)
                else:
                    await msg.answer(f"❌ Пользователь @{username} не найден в базе")
            else:
                await msg.answer("❌ Используйте: дипноль @username\nИли: дипноль алл - для всех игроков (ОПАСНО!)")
        else:
            await msg.answer("❌ Используйте: дипноль @username\nПример: дипноль @player123")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.callback_query(lambda c: c.data == "confirm_reset_all")
async def confirm_reset_all(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID and call.from_user.username != ADMIN_USERNAME:
        await call.answer("❌ У вас нет прав", show_alert=True)
        return
    
    try:
        # Получаем всех пользователей для уведомления
        all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
        
        # Сброс всех пользователей
        sql.execute("""
            UPDATE users SET 
            coins = 0, exp = 0, weapon = 'Револьвер', location = 'Тайга',
            last_hunt = 0, daily_kills = 0, total_kills = 0, current_title = '',
            prestige = 0, achievement_streak = 0, achievements_completed = '{}',
            health = 100, max_health = 100, deaths = 0, counterattack_streak = 0,
            titan_escape_streak = 0, trap_days_streak = 0, last_trap_use = 0,
            traps_used = 0, heavy_traps = 0, last_achievement_check = 0,
            golden_bullet = 0, drone_target = '', drone_expires = 0, last_daily_gift = 0,
            survival_hunt_count = 0, survival_damage_count = 0, diamond_bullet = 0,
            immortality_staff = 0, energy_drink = 0, hunt_counter = 0
        """)
        
        sql.execute("DELETE FROM trophies")
        sql.execute("DELETE FROM user_equipment")
        sql.execute("DELETE FROM user_weapons WHERE weapon != 'Револьвер'")
        sql.execute("DELETE FROM stats_daily")
        sql.execute("DELETE FROM survival_items")
        
        db.commit()
        
        await call.message.edit_text("✅ Профили ВСЕХ игроков полностью сброшены!")
        print(f"🔧 Админ {call.from_user.id} сбросил профили ВСЕХ игроков")
        
        # Уведомляем всех игроков
        for user_id, username in all_users:
            try:
                await bot.send_message(user_id, "⚠️ Ваш профиль был сброшен администратором!")
            except:
                pass
                
    except Exception as e:
        await call.message.edit_text(f"❌ Ошибка: {str(e)}")

@dp.callback_query(lambda c: c.data.startswith("confirm_reset:"))
async def confirm_reset_user(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID and call.from_user.username != ADMIN_USERNAME:
        await call.answer("❌ У вас нет прав", show_alert=True)
        return
    
    try:
        user_id = int(call.data.split(":")[1])
        
        user = sql.execute("SELECT username FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not user:
            await call.message.edit_text("❌ Пользователь не найден")
            return
        
        username = user[0]
        
        # Сброс пользователя
        sql.execute("""
            UPDATE users SET 
            coins = 0, exp = 0, weapon = 'Револьвер', location = 'Тайга',
            last_hunt = 0, daily_kills = 0, total_kills = 0, current_title = '',
            prestige = 0, achievement_streak = 0, achievements_completed = '{}',
            health = 100, max_health = 100, deaths = 0, counterattack_streak = 0,
            titan_escape_streak = 0, trap_days_streak = 0, last_trap_use = 0,
            traps_used = 0, heavy_traps = 0, last_achievement_check = 0,
            golden_bullet = 0, drone_target = '', drone_expires = 0, last_daily_gift = 0,
            survival_hunt_count = 0, survival_damage_count = 0, diamond_bullet = 0,
            immortality_staff = 0, energy_drink = 0, hunt_counter = 0
            WHERE user_id = ?
        """, (user_id,))
        
        sql.execute("DELETE FROM trophies WHERE user_id = ?", (user_id,))
        sql.execute("DELETE FROM user_equipment WHERE user_id = ?", (user_id,))
        sql.execute("DELETE FROM user_weapons WHERE user_id = ? AND weapon != 'Револьвер'", (user_id,))
        sql.execute("DELETE FROM stats_daily WHERE user_id = ?", (user_id,))
        sql.execute("DELETE FROM survival_items WHERE user_id = ?", (user_id,))
        
        db.commit()
        
        await call.message.edit_text(f"✅ Профиль @{username} полностью сброшен!")
        print(f"🔧 Админ {call.from_user.id} сбросил профиль @{username}")
        
        # Уведомляем игрока
        try:
            await bot.send_message(user_id, "⚠️ Ваш профиль был сброшен администратором!")
        except:
            pass
            
    except Exception as e:
        await call.message.edit_text(f"❌ Ошибка: {str(e)}")

@dp.callback_query(lambda c: c.data == "cancel_reset")
async def cancel_reset(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID and call.from_user.username != ADMIN_USERNAME:
        await call.answer("❌ У вас нет прав", show_alert=True)
        return
    
    await call.message.edit_text("❌ Сброс отменен")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипл"))
async def admin_reset_traps(msg: Message):
    """Сбросить ловушки для игрока"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        
        if len(parts) >= 2 and parts[1].lower() == "алл":
            # Сброс для всех игроков
            sql.execute("UPDATE users SET last_trap_use = 0")
            db.commit()
            await msg.answer("✅ Ловушки сброшены для ВСЕХ игроков!")
            print(f"🔧 Админ {msg.from_user.id} сбросил ловушки для ВСЕХ игроков")
            
            # Уведомляем всех игроков
            all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
            for user_id, username in all_users:
                try:
                    await bot.send_message(user_id, "🪤 Ваши ловушки были сброшены администратором!")
                except:
                    pass
                    
        elif len(parts) >= 2 and "@" in parts[1]:
            username = parts[1].replace("@", "").strip()
            user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
            if user:
                sql.execute("UPDATE users SET last_trap_use = 0 WHERE user_id = ?", (user[0],))
                db.commit()
                await msg.answer(f"✅ Ловушки сброшены для @{username}")
                print(f"🔧 Админ {msg.from_user.id} сбросил ловушки для @{username}")
                
                # Уведомляем игрока
                try:
                    await bot.send_message(user[0], "🪤 Ваши ловушки были сброшены администратором!")
                except:
                    pass
            else:
                await msg.answer(f"❌ Пользователь @{username} не найден в базе")
        else:
            await msg.answer("❌ Используйте: дипл @username\nИли: дипл алл - для всех игроков")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("диппод"))
async def admin_reset_gift(msg: Message):
    """Сбросить подарок для игрока"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        
        if len(parts) >= 2 and parts[1].lower() == "алл":
            # Сброс для всех игроков
            sql.execute("UPDATE users SET last_daily_gift = 0")
            db.commit()
            await msg.answer("✅ Подарки сброшены для ВСЕХ игроков!")
            print(f"🔧 Админ {msg.from_user.id} сбросил подарки для ВСЕХ игроков")
            
            # Уведомляем всех игроков
            all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
            for user_id, username in all_users:
                try:
                    await bot.send_message(user_id, "🎁 Ваш подарок был сброшен администратором!")
                except:
                    pass
                    
        elif len(parts) >= 2 and "@" in parts[1]:
            username = parts[1].replace("@", "").strip()
            user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
            if user:
                sql.execute("UPDATE users SET last_daily_gift = 0 WHERE user_id = ?", (user[0],))
                db.commit()
                await msg.answer(f"✅ Подарок сброшен для @{username}")
                print(f"🔧 Админ {msg.from_user.id} сбросил подарок для @{username}")
                
                # Уведомляем игрока
                try:
                    await bot.send_message(user[0], "🎁 Ваш подарок был сброшен администратором!")
                except:
                    pass
            else:
                await msg.answer(f"❌ Пользователь @{username} не найден в базе")
        else:
            await msg.answer("❌ Используйте: диппод @username\nИли: диппод алл - для всех игроков")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("дипкил"))
async def admin_add_kills(msg: Message):
    """Добавить убийства игроку"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        if len(parts) >= 2:
            try:
                amount = int(parts[1])
            except ValueError:
                await msg.answer("❌ Ошибка: количество убийств должно быть числом")
                return
                
            if len(parts) >= 3 and parts[2].lower() == "алл":
                # Добавить всем игрокам
                sql.execute("UPDATE users SET total_kills = total_kills + ?", (amount,))
                sql.execute("UPDATE users SET daily_kills = daily_kills + ?", (amount,))
                db.commit()
                await msg.answer(f"✅ Добавлено {amount} убийств ВСЕМ игрокам!")
                print(f"🔧 Админ {msg.from_user.id} добавил {amount} убийств ВСЕМ игрокам")
                
                # Уведомляем всех игроков
                all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
                for user_id, username in all_users:
                    try:
                        await bot.send_message(user_id, f"🎯 Администратор добавил вам {amount} убийств!")
                    except:
                        pass
                        
            elif len(parts) >= 3 and "@" in parts[2]:
                username = parts[2].replace("@", "").strip()
                user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
                if user:
                    sql.execute("UPDATE users SET total_kills = total_kills + ?, daily_kills = daily_kills + ? WHERE user_id = ?", 
                               (amount, amount, user[0]))
                    db.commit()
                    await msg.answer(f"✅ Добавлено {amount} убийств пользователю @{username}")
                    print(f"🔧 Админ {msg.from_user.id} добавил {amount} убийств @{username}")
                    
                    # Уведомляем игрока
                    try:
                        await bot.send_message(user[0], f"🎯 Администратор добавил вам {amount} убийств!")
                    except:
                        pass
                else:
                    await msg.answer(f"❌ Пользователь @{username} не найден в базе")
            else:
                await msg.answer("❌ Используйте: дипкил <кол-во> @username\nИли: дипкил <кол-во> алл - для всех игроков")
        else:
            await msg.answer("❌ Используйте: дипкил <кол-во> @username\nПример: дипкил 10 @player123")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.lower().startswith("диппредмет"))
async def admin_give_collectible(msg: Message):
    """Выдать коллекционный предмет игроку
    Форматы:
    диппредмет название_предмета количество @username
    диппредмет название_предмета количество алл
    Пример: диппредмет Сосновая шишка 5 @DeepSleep01
    """
    try:
        # Проверка прав админа
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        # Убираем "диппредмет" из начала (11 символов)
        text = msg.text[11:].strip()
        
        if not text:
            await msg.answer(
                "❌ Используйте:\n"
                "диппредмет название_предмета количество @username\n"
                "диппредмет название_предмета количество алл\n\n"
                "Пример: диппредмет Сосновая шишка 5 @DeepSleep01"
            )
            return
        
        # Парсим: предмет количество @username (без кавычек)
        parts = text.split()
        if len(parts) < 3:
            await msg.answer("❌ Укажите: название_предмета количество @username\nПример: диппредмет Сосновая шишка 5 @user")
            return
        
        # Последняя часть - @username или алл
        target = parts[-1].strip()
        
        # Предпоследняя часть - количество
        try:
            amount = int(parts[-2])
            if amount <= 0:
                await msg.answer("❌ Количество должно быть больше 0")
                return
            if amount > 1000:
                await msg.answer("❌ Максимальное количество за раз - 1000")
                return
        except ValueError:
            await msg.answer("❌ Количество должно быть числом\nПример: диппредмет Сосновая шишка 5 @user")
            return
        
        # Всё остальное - название предмета (может быть из нескольких слов)
        item_name_input = " ".join(parts[:-2]).strip().lower()
        
        if not item_name_input:
            await msg.answer("❌ Укажите название предмета\nПример: диппредмет Сосновая шишка 5 @user")
            return
        
        # ===== ПОИСК ПРЕДМЕТА (сравниваем без эмодзи и без учёта регистра) =====
        def remove_emoji(text):
            """Удаляет эмодзи из строки, оставляя только текст"""
            import re
            # Удаляем все emoji (диапазоны Unicode)
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # смайлики
                u"\U0001F300-\U0001F5FF"  # символы
                u"\U0001F680-\U0001F6FF"  # транспорт
                u"\U0001F700-\U0001F77F"  # алхимические символы
                u"\U0001F780-\U0001F7FF"  # геометрические
                u"\U0001F800-\U0001F8FF"  # стрелки
                u"\U0001F900-\U0001F9FF"  # дополнительные
                u"\U0001FA00-\U0001FA6F"  # ещё дополнительные
                u"\U0001FA70-\U0001FAFF"  # ещё
                u"\U00002702-\U000027B0"  # символы
                u"\U000024C2-\U0001F251" 
                "]+", flags=re.UNICODE)
            return emoji_pattern.sub('', text).strip()
        
        found_location = None
        found_group = None
        found_item_name = None  # точное название из словаря
        
        for loc_name, loc_data in LOCATION_COLLECTIBLES.items():
            for group_name, items in loc_data.items():
                for item in items:
                    # Сравниваем без эмодзи и без учёта регистра
                    item_clean = remove_emoji(item).lower()
                    if item_name_input == item_clean or item_name_input in item_clean or item_clean in item_name_input:
                        found_location = loc_name
                        found_group = group_name
                        found_item_name = item
                        break
                if found_location:
                    break
            if found_location:
                break
        
        if not found_location:
            # Показываем доступные предметы (без эмодзи для читаемости)
            all_items = []
            for loc_name, loc_data in LOCATION_COLLECTIBLES.items():
                for group_name, items in loc_data.items():
                    for item in items:
                        item_clean = remove_emoji(item)
                        all_items.append(f"• {item_clean} ({loc_name}, {group_name})")
            
            items_preview = "\n".join(all_items[:20])
            if len(all_items) > 20:
                items_preview += f"\n... и ещё {len(all_items) - 20} предметов"
            
            await msg.answer(
                f"❌ Предмет '{item_name_input}' не найден!\n\n"
                f"Доступные предметы (названия без эмодзи):\n{items_preview}"
            )
            return
        
        # ===== ВАРИАНТ: ВСЕМ ИГРОКАМ =====
        if target.lower() == "алл":
            all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
            
            if not all_users:
                await msg.answer("❌ Нет зарегистрированных пользователей!")
                return
            
            success_count = 0
            total_items_given = 0
            
            await msg.answer(f"📤 Выдаю {found_item_name} x{amount} {len(all_users)} игрокам...")
            
            for user_id, username in all_users:
                try:
                    for _ in range(amount):
                        add_collectible(user_id, found_location, found_group, found_item_name)
                    total_items_given += amount
                    success_count += 1
                    
                    try:
                        await bot.send_message(
                            user_id, 
                            f"🎁 Администратор выдал вам предмет:\n"
                            f"📦 {found_item_name} x{amount}\n"
                            f"📍 Локация: {found_location}"
                        )
                    except:
                        pass
                    
                    await asyncio.sleep(0.05)
                    
                except Exception as e:
                    print(f"Ошибка при выдаче игроку {user_id}: {e}")
            
            await msg.answer(
                f"✅ Выдано {found_item_name} x{amount} {success_count} игрокам!\n"
                f"📊 Всего выдано: {total_items_given} предметов"
            )
            
            print(f"🔧 Админ {msg.from_user.id} выдал {found_item_name} x{amount} ВСЕМ игрокам")
            return
        
        # ===== ВАРИАНТ: КОНКРЕТНОМУ ИГРОКУ =====
        if not target.startswith("@"):
            await msg.answer("❌ Укажите @username или 'алл'\nПример: диппредмет Сосновая шишка 5 @user")
            return
        
        username = target[1:].strip()
        
        user = sql.execute("SELECT user_id, username FROM users WHERE username = ?", (username,)).fetchone()
        
        if not user:
            await msg.answer(f"❌ Пользователь @{username} не найден в базе!")
            return
        
        user_id = user[0]
        user_username = user[1]
        
        # Получаем текущее количество предмета у игрока
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        current = cur.execute(
            "SELECT count FROM user_collectibles WHERE user_id = ? AND location = ? AND group_name = ? AND item_name = ?",
            (user_id, found_location, found_group, found_item_name)
        ).fetchone()
        current_count = current[0] if current else 0
        conn.close()
        
        # Добавляем предметы
        for _ in range(amount):
            add_collectible(user_id, found_location, found_group, found_item_name)
        
        # Проверяем, не собрана ли полная коллекция
        collected, total = get_collection_progress(user_id, found_location)
        
        reward_text = ""
        if collected >= total:
            reward_text = f"\n\n🎉 Игрок собрал ВСЕ 10 предметов в {found_location}!\n🏆 +5000💰 +1000⭐ + скин профиля!"
        
        await msg.answer(
            f"✅ Пользователю @{user_username} выдано:\n"
            f"📦 {found_item_name} x{amount}\n"
            f"📍 Локация: {found_location}\n\n"
            f"Было: {current_count}\n"
            f"Стало: {current_count + amount}{reward_text}"
        )
        
        # Уведомляем игрока
        try:
            await bot.send_message(
                user_id,
                f"🎁 Администратор выдал вам предмет:\n"
                f"📦 {found_item_name} x{amount}\n"
                f"📍 Локация: {found_location}"
            )
        except:
            pass
        
        print(f"🔧 Админ {msg.from_user.id} выдал {found_item_name} x{amount} @{user_username}")
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")
        import traceback
        traceback.print_exc()

@dp.message(lambda msg: msg.text and msg.text.lower().startswith("дипквл"))
async def admin_give_location_achievement(msg: Message):
    """Выдать достижение локации принудительно
    Форматы:
    дипквл @username локация 60
    дипквл @username локация 250
    дипквл @username локация 90
    дипквл @username локация пр
    """
    try:
        # Проверка прав админа
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        parts = msg.text.split(maxsplit=3)
        if len(parts) < 4:
            await msg.answer(
                "❌ Используйте:\n"
                "дипквл @username локация 60\n"
                "дипквл @username локация 250\n"
                "дипквл @username локация 90\n"
                "дипквл @username локация пр\n\n"
                "Пример: дипквл @DeepSleep01 Киберпанк 60"
            )
            return
        
        username = parts[1].replace("@", "").strip()
        location = parts[2].strip()
        ach_type = parts[3].strip().lower()
        
        # Проверяем существование локации
        if location not in LOCATIONS:
            # Поиск по частичному совпадению
            found = None
            for loc in LOCATIONS.keys():
                if loc.lower() == location.lower():
                    found = loc
                    break
                if location.lower() in loc.lower():
                    found = loc
                    break
            if found:
                location = found
            else:
                available = "\n".join(list(LOCATIONS.keys())[:15])
                await msg.answer(f"❌ Локация '{location}' не найдена!\n\nДоступные:\n{available}")
                return
        
        # Определяем тип достижения
        if ach_type == "60":
            achievement_type = "60_kills"
        elif ach_type == "250":
            achievement_type = "250_kills"
        elif ach_type == "90":
            achievement_type = "all_species"
        elif ach_type == "пр":
            achievement_type = "full_collection"
        else:
            await msg.answer("❌ Неверный тип. Используйте: 60, 250, 90, пр")
            return
        
        # Ищем пользователя
        user = sql.execute("SELECT user_id, username FROM users WHERE username = ?", (username,)).fetchone()
        if not user:
            await msg.answer(f"❌ Пользователь @{username} не найден")
            return
        
        user_id = user[0]
        user_username = user[1]
        
        # Проверяем, не выдано ли уже достижение
        existing = sql.execute(
            "SELECT completed FROM location_achievements WHERE user_id = ? AND location = ? AND achievement_type = ?",
            (user_id, location, achievement_type)
        ).fetchone()
        
        if existing and existing[0] == 1:
            await msg.answer(f"⚠️ У @{user_username} уже есть достижение '{achievement_type}' в локации {location}")
            return
        
        # Получаем данные достижения
        ach_data = LOCATION_ACHIEVEMENTS_DATA.get(location, {}).get(achievement_type, {})
        
        rewards_text = []
        
        # Выдаём награды
        if ach_data.get("coins_reward", 0) > 0:
            sql.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (ach_data["coins_reward"], user_id))
            rewards_text.append(f"💰 +{ach_data['coins_reward']} монет")
        
        if ach_data.get("exp_reward", 0) > 0:
            sql.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (ach_data["exp_reward"], user_id))
            rewards_text.append(f"⭐ +{ach_data['exp_reward']} опыта")
        
        if ach_data.get("title"):
            current_title = sql.execute("SELECT current_title FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            if not current_title:
                sql.execute("UPDATE users SET current_title = ? WHERE user_id = ?", (ach_data["title"], user_id))
                rewards_text.append(f"👑 Титул: {ach_data['title']}")
            else:
                rewards_text.append(f"👑 Титул: {ach_data['title']} (добавлен в коллекцию)")
        
        if ach_data.get("status"):
            current_status = sql.execute("SELECT current_status FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            if not current_status or current_status == "На охоте🏹":
                sql.execute("UPDATE users SET current_status = ? WHERE user_id = ?", (ach_data["status"], user_id))
                rewards_text.append(f"🏷️ Статус: {ach_data['status']}")
            else:
                rewards_text.append(f"🏷️ Статус: {ach_data['status']} (добавлен в коллекцию)")
        
        if ach_data.get("quote"):
            current_quote = sql.execute("SELECT current_quote FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            if not current_quote or current_quote == "Я начинающий охотник, и я иду к своей цели":
                sql.execute("UPDATE users SET current_quote = ? WHERE user_id = ?", (ach_data["quote"], user_id))
                rewards_text.append(f"💬 Цитата добавлена")
            else:
                rewards_text.append(f"💬 Цитата добавлена в коллекцию")
        
        # Записываем достижение
        sql.execute("""
            INSERT OR REPLACE INTO location_achievements (user_id, location, achievement_type, completed, completed_at)
            VALUES (?, ?, ?, 1, ?)
        """, (user_id, location, achievement_type, int(time.time())))
        
        # Если это "пр" (полная коллекция), разблокируем скин профиля
        if achievement_type == "full_collection":
            sql.execute("""
                INSERT OR REPLACE INTO user_themes (user_id, theme_name, unlocked)
                VALUES (?, ?, 1)
            """, (user_id, location.lower()))
            rewards_text.append(f"🎨 Скин профиля: {location}")
        
        db.commit()
        
        # Формируем ответ
        type_names = {
            "60_kills": "60 убийств",
            "250_kills": "250 убийств",
            "all_species": "90% видов",
            "full_collection": "Полная коллекция предметов"
        }
        
        await msg.answer(
            f"✅ Пользователю @{user_username} выдано достижение в {location}:\n"
            f"📌 {type_names.get(achievement_type, achievement_type)}\n\n"
            f"🎁 Награды:\n" + "\n".join(rewards_text)
        )
        
        # Уведомляем игрока в ЛС
        try:
            await bot.send_message(
                user_id,
                f"🏆 **Вам выдано достижение!** 🏆\n\n"
                f"📍 Локация: {location}\n"
                f"📌 Достижение: {type_names.get(achievement_type, achievement_type)}\n\n"
                f"🎁 Награды:\n" + "\n".join(rewards_text),
                parse_mode="Markdown"
            )
        except:
            pass
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")
        import traceback
        traceback.print_exc()

@dp.message(lambda msg: msg.text and msg.text.startswith("дипжив"))
async def admin_add_animal(msg: Message):
    """Добавить животное игроку"""
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
            
        parts = msg.text.split()
        if len(parts) >= 3:
            animal = parts[1].strip('"\'')
            
            try:
                count = 1
                if len(parts) >= 4:
                    count = int(parts[2])
                    username_part = parts[3]
                else:
                    username_part = parts[2]
                
                # Проверяем существование животного
                animal_exists = False
                for location in LOCATIONS.values():
                    for animal_list in location["animals"].values():
                        if animal in animal_list:
                            animal_exists = True
                            break
                    if animal_exists:
                        break
                
                if not animal_exists:
                    await msg.answer(f"❌ Животное '{animal}' не найдено в игре")
                    return
                
                if username_part.lower() == "алл":
                    # Добавить всем игрокам
                    all_users = sql.execute("SELECT user_id FROM users").fetchall()
                    for user_data in all_users:
                        user_id = user_data[0]
                        trophy = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", 
                                           (user_id, animal)).fetchone()
                        if trophy:
                            sql.execute("UPDATE trophies SET count = count + ? WHERE user_id = ? AND animal = ?", 
                                       (count, user_id, animal))
                        else:
                            sql.execute("INSERT INTO trophies VALUES (?, ?, ?)", (user_id, animal, count))
                    
                    db.commit()
                    await msg.answer(f"✅ Добавлено животное '{animal}' (x{count}) ВСЕМ игрокам!")
                    print(f"🔧 Админ {msg.from_user.id} добавил '{animal}' x{count} ВСЕМ игрокам")
                    
                    # Уведомляем всех игроков
                    all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
                    for user_id, username in all_users:
                        try:
                            await bot.send_message(user_id, f"🐾 Администратор добавил вам животное: {animal} (x{count})!")
                        except:
                            pass
                            
                elif "@" in username_part:
                    username = username_part.replace("@", "").strip()
                    user = sql.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
                    if user:
                        trophy = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", 
                                           (user[0], animal)).fetchone()
                        if trophy:
                            sql.execute("UPDATE trophies SET count = count + ? WHERE user_id = ? AND animal = ?", 
                                       (count, user[0], animal))
                        else:
                            sql.execute("INSERT INTO trophies VALUES (?, ?, ?)", (user[0], animal, count))
                        
                        db.commit()
                        await msg.answer(f"✅ Добавлено животное '{animal}' (x{count}) пользователю @{username}")
                        print(f"🔧 Админ {msg.from_user.id} добавил '{animal}' x{count} @{username}")
                        
                        # Уведомляем игрока
                        try:
                            await bot.send_message(user[0], f"🐾 Администратор добавил вам животное: {animal} (x{count})!")
                        except:
                            pass
                    else:
                        await msg.answer(f"❌ Пользователь @{username} не найден в базе")
                else:
                    await msg.answer("❌ Используйте: дипжив \"животное\" <кол-во> @username\nИли: дипжив \"животное\" <кол-во> алл")
            except ValueError:
                await msg.answer("❌ Ошибка: количество должно быть числом")
        else:
            await msg.answer("❌ Используйте: дипжив \"животное\" <кол-во> @username\nПример: дипжив \"Заяц\" 5 @player123")
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.lower().startswith("дипквест"))
async def admin_give_achievement(msg: Message):
    """Выдать достижение игроку (только для админа)
    Формат: дипквест НазваниеДостижения @username
    Пример: дипквест 👾 Кибермонстр @DeepSleep01
    """
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        # Убираем "дипквест" из начала
        text = msg.text[8:].strip()  # "дипквест" - 8 символов
        
        if not text:
            await msg.answer("❌ Используйте: дипквест НазваниеДостижения @username\nПример: дипквест 👾 Кибермонстр @DeepSleep01")
            return
        
        # Ищем @username в конце
        parts = text.split()
        
        if len(parts) < 2:
            await msg.answer("❌ Укажите @username\nПример: дипквест 👾 Кибермонстр @DeepSleep01")
            return
        
        # Последняя часть - username
        username_part = parts[-1]
        if not username_part.startswith("@"):
            await msg.answer("❌ Укажите корректный @username\nПример: дипквест 👾 Кибермонстр @DeepSleep01")
            return
        
        username = username_part[1:].strip()
        achievement_name = " ".join(parts[:-1]).strip()
        
        if not achievement_name:
            await msg.answer("❌ Укажите название достижения")
            return
        
        # Проверяем существование достижения
        if achievement_name not in ACHIEVEMENTS:
            # Поиск по частичному совпадению
            found = None
            for ach_name in ACHIEVEMENTS.keys():
                if ach_name.lower() == achievement_name.lower():
                    found = ach_name
                    break
                if achievement_name.lower() in ach_name.lower():
                    found = ach_name
                    break
            
            if found:
                achievement_name = found
            else:
                available = "\n".join(list(ACHIEVEMENTS.keys())[:10])
                await msg.answer(f"❌ Достижение '{achievement_name}' не найдено!\n\nДоступные достижения:\n{available}" + ("\n..." if len(ACHIEVEMENTS) > 10 else ""))
                return
        
        # Ищем пользователя
        user = sql.execute("SELECT user_id, username FROM users WHERE username = ?", (username,)).fetchone()
        if not user:
            await msg.answer(f"❌ Пользователь @{username} не найден в базе!")
            return
        
        user_id = user[0]
        user_username = user[1]
        achievement_data = ACHIEVEMENTS[achievement_name]
        
        # Проверяем, не получено ли уже
        completed = get_completed_achievements(user_id)
        if achievement_name in completed:
            await msg.answer(f"⚠️ У пользователя @{user_username} уже есть достижение '{achievement_name}'!")
            return
        
        # Выдаем достижение
        completed[achievement_name] = {
            "completed_at": int(time.time()),
            "reward_coins": achievement_data["reward_coins"],
            "reward_exp": achievement_data["reward_exp"],
            "title": achievement_data.get("title", "")
        }
        
        # Начисляем награды
        sql.execute("UPDATE users SET coins = coins + ?, exp = exp + ? WHERE user_id = ?", 
                   (achievement_data["reward_coins"], achievement_data["reward_exp"], user_id))
        
        if achievement_data.get("title"):
            sql.execute("UPDATE users SET current_title = ? WHERE user_id = ?", 
                       (achievement_data["title"], user_id))
        
        sql.execute("UPDATE users SET achievements_completed = ? WHERE user_id = ?", 
                   (str(completed), user_id))
        db.commit()
        
        await msg.answer(f"✅ Пользователю @{user_username} выдано достижение: {achievement_name}\n"
                        f"💰 +{achievement_data['reward_coins']} монет\n"
                        f"⭐ +{achievement_data['reward_exp']} опыта\n"
                        f"👑 Титул: {achievement_data.get('title', 'нет')}")
        
        # Уведомляем игрока в ЛС
        try:
            reward_text = f"🎉 **Вам выдано достижение!** 🎉\n\n"
            reward_text += f"🏆 **{achievement_name}**\n"
            reward_text += f"📝 {achievement_data['description']}\n\n"
            reward_text += f"💰 Награда: {achievement_data['reward_coins']} монет\n"
            reward_text += f"⭐ Опыт: +{achievement_data['reward_exp']}\n"
            if achievement_data.get("title"):
                reward_text += f"👑 Титул: {achievement_data['title']}\n"
            reward_text += f"\n✨ Поздравляем! Продолжай в том же духе!"
            
            await bot.send_message(user_id, reward_text, parse_mode="Markdown")
        except Exception as e:
            print(f"Не удалось отправить ЛС игроку {user_id}: {e}")
            
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.lower().startswith("дипчат"))
async def admin_chat_message(msg: Message):
    """Отправить сообщение игрокам в ЛС (только для админа)
    Формат: дипчат @username текст
    Или: дипчат алл текст
    Пример: дипчат алл Привет всем!
    Пример: дипчат @DeepSleep01 Привет!
    """
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        # Убираем "дипчат" из начала (7 символов)
        text = msg.text[7:].strip()
        
        if not text:
            await msg.answer("❌ Используйте:\n"
                           "дипчат @username текст\n"
                           "дипчат алл текст\n"
                           "Пример: дипчат алл Привет всем!")
            return
        
        # Определяем получателя
        if text.startswith("алл"):
            # Отправляем всем
            message_text = text[3:].strip()  # убираем "алл "
            
            if not message_text:
                await msg.answer("❌ Введите текст сообщения!\nПример: дипчат алл Привет всем!")
                return
            
            all_users = sql.execute("SELECT user_id, username FROM users WHERE username IS NOT NULL").fetchall()
            
            if not all_users:
                await msg.answer("❌ Нет зарегистрированных пользователей!")
                return
            
            success_count = 0
            fail_count = 0
            
            await msg.answer(f"📤 Отправляю сообщение {len(all_users)} игрокам...\n\n📝 Текст: {message_text}")
            
            for user_id, username in all_users:
                try:
                    await bot.send_message(user_id, f"📢 **Сообщение от администратора:**\n\n{message_text}", parse_mode="Markdown")
                    success_count += 1
                except:
                    fail_count += 1
                await asyncio.sleep(0.05)  # небольшая задержка, чтобы не спамить
            
            await msg.answer(f"✅ Отправлено: {success_count} игрокам\n❌ Не доставлено: {fail_count}")
            print(f"🔧 Админ {msg.from_user.id} отправил сообщение ВСЕМ игрокам: {message_text}")
            
        elif text.startswith("@"):
            # Отправляем одному пользователю
            parts = text.split()
            username_part = parts[0]
            username = username_part[1:].strip()
            message_text = " ".join(parts[1:]).strip()
            
            if not message_text:
                await msg.answer("❌ Введите текст сообщения!\nПример: дипчат @DeepSleep01 Привет!")
                return
            
            user = sql.execute("SELECT user_id, username FROM users WHERE username = ?", (username,)).fetchone()
            
            if not user:
                await msg.answer(f"❌ Пользователь @{username} не найден в базе!")
                return
            
            user_id = user[0]
            user_username = user[1]
            
            try:
                await bot.send_message(user_id, f"📢 **Сообщение от администратора:**\n\n{message_text}", parse_mode="Markdown")
                await msg.answer(f"✅ Сообщение отправлено @{user_username}\n\n📝 Текст: {message_text}")
                print(f"🔧 Админ {msg.from_user.id} отправил сообщение @{user_username}: {message_text}")
            except Exception as e:
                await msg.answer(f"❌ Не удалось отправить сообщение @{user_username}: {str(e)}")
        else:
            await msg.answer("❌ Используйте:\n"
                           "дипчат @username текст - для отправки одному игроку\n"
                           "дипчат алл текст - для отправки всем игрокам\n"
                           "Пример: дипчат алл Привет всем!")
            
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

@dp.message(lambda msg: msg.text and msg.text.startswith("диппогода"))
async def admin_set_weather(msg: Message):
    """Принудительно сменить погоду (только для админа)
    Формат: диппогода солнечно
    Пример: диппогода дождь
    """
    try:
        if msg.from_user.id != ADMIN_ID and msg.from_user.username != ADMIN_USERNAME:
            await msg.answer("❌ У вас нет прав для использования этой команды")
            return
        
        parts = msg.text.split()
        if len(parts) < 2:
            await msg.answer("❌ Используйте: диппогода <погода>\n"
                           "Доступные погоды: солнечно, облачно, дождь, гроза, туманно, ветер")
            return
        
        weather_name = parts[1].lower()
        
        # Сопоставляем название с типом погоды
        weather_map = {
            "солнечно": "☀️ Солнечно",
            "облачно": "☁️ Облачно",
            "дождь": "🌧️ Дождь",
            "гроза": "⛈️ Гроза",
            "туманно": "🌫️ Туманно",
            "туман": "🌫️ Туманно",
            "ветер": "💨 Ветер"
        }
        
        if weather_name not in weather_map:
            await msg.answer(f"❌ Погода '{weather_name}' не найдена!\n"
                           "Доступные: солнечно, облачно, дождь, гроза, туманно, ветер")
            return
        
        global current_weather, last_weather_change
        old_weather = current_weather
        current_weather = weather_map[weather_name]
        last_weather_change = int(time.time())
        
        await msg.answer(f"✅ Погода изменена!\n🌦️ Было: {old_weather}\n🌤️ Стало: {current_weather}")
        print(f"🔧 Админ {msg.from_user.id} сменил погоду: {old_weather} → {current_weather}")
        
        # Уведомляем в чат (если есть ID чата)
        # await bot.send_message(CHAT_ID, f"🌦️ Администратор изменил погоду!\nТеперь: {current_weather}")
        
    except Exception as e:
        await msg.answer(f"❌ Ошибка: {str(e)}")

# ================== ОСНОВНЫЕ КОМАНДЫ ==================

@dp.message(Command("start"))
async def start(msg: Message):
    user_id = msg.from_user.id
    username = msg.from_user.username
    
    user = ensure_user(user_id, username)
    
    # ===== ЕЖЕДНЕВНЫЙ БОНУС ОТ ЗОЛОТОГО ЯЙЦА =====
    if is_event_active():
        last_claim = user[35] if len(user) > 35 else 0
        now = int(time.time())
        
        has_golden_egg = sql.execute("SELECT 1 FROM user_equipment WHERE user_id = ? AND equipment = ?", (user_id, EVENT_ITEM_NAME)).fetchone()
        
        if has_golden_egg and now - last_claim >= 86400:
            sql.execute("UPDATE users SET coins = coins + 500, event_egg_claim = ? WHERE user_id = ?", (now, user_id))
            db.commit()
            await msg.answer(f"🥚 Твоё {EVENT_ITEM_NAME} принесло 500 монет!")
    
    await msg.answer(
        "🏹 Добро пожаловать на охоту!\n\n"
        "📋 Команды:\n"
        "• Хант — начать охоту\n"
        "• Состояние — проверить здоровье\n" 
        "• Инв — посмотреть профиль\n"
        "• Магазин — купить оружие и снаряжение\n"
        "• Локации — выбрать локацию\n"
        "• Топы — таблица лидеров\n"
        "• Справка — информация о боте\n"
        "• Достижения — ваши достижения\n"
        "• Оформление — выбрать титул/цитату/статус\n"
        "• Престиж — получить престиж\n"
        "• Погода — информация о погоде\n"
        "• Выживание — состояние предметов выживания\n"
        "• Ивент — информация об ивенте\n"
        "• Ловушки — использовать ловушки (раз в 12 часов)\n"
        "• Серия — забрать подарок ежедневной серии (раз в 12 часов)\n"
        "• Инфо — посмотреть команды"
    )

@dp.message(lambda msg: msg.text and msg.text.lower() == "справка")
async def help_command(msg: Message):
    await msg.answer("Если есть вопросы/проблемы с ботом/идеи для обновлений то напиши @DeepSleep01")

@dp.message(lambda msg: msg.text and msg.text.lower() == "инфо")
async def help_command(msg: Message):
    await msg.answer(
        "• Хант — начать охоту\n"
        "• Инв — посмотреть профиль\n"
        "• Магазин — открыть магазин\n"
        "• Локации — выбрать локацию/посмотреть список животных\n"
        "• Ивент — информация об ивенте\n"
        "• Достижения — посмотреть список достижений\n"
        "• Оформление — выбрать титул/цитату/статус\n"
        "• Топы — таблица лидеров\n"
        "• Престиж — информация о престиже\n"\
        "• Погода — информация о погоде\n"
        "• Выживание — посмотреть ваши предметы выживания\n"
        "• Состояние — проверить здоровье\n" 
        "• Ловушки — использовать ловушки (раз в 12 часов)\n"
        "• Серия — забрать подарок ежедневной серии (раз в 12 часов)\n"
        "• Справка — информация о боте\n"
        "• Инфо — данный список\n\n"
        "ПЕРЕХОДИ В НАШ ЧАТ - @chatbothunt"
    )

@dp.message(lambda msg: msg.text and msg.text.lower() == "подарок")
async def help_command(msg: Message):
    await msg.answer("Недавно функция подарок была удалена! Но не отчаивайся, напиши 'Серия'")

@dp.message(lambda msg: msg.text and msg.text.lower() == "состояние")
async def health_status(msg: Message):
    """Показать состояние здоровья и информацию о восстановлении"""
    user = ensure_user(msg.from_user.id, msg.from_user.username)
    current_hp, max_hp = get_user_health(msg.from_user.id)
    deaths = user[15] if len(user) > 15 else 0
    
    status_text = f"❤️ Здоровье: {current_hp}/{max_hp}\n"
    
    if current_hp <= 0:
        status_text += f"💀 Слишком мало здоровья! Необходимо восстановить здоровье до 26 HP или больше.\n"
        hp_needed = 26 - current_hp
        status_text += f"📉 Автоматическое восстановление: 1 HP в минуту\n"
        status_text += "💡 Совет: используйте аптечку из магазина для быстрого лечения!"
    elif current_hp < max_hp:
        status_text += f""
        healing_rate = 1
        equipment = get_user_equipment(msg.from_user.id)
        if "Витамины" in equipment:
            healing_rate = 1.5
            status_text += "💊 Бонус восстановления: x1.5 (витамины)\n"
        
        minutes_to_full = (max_hp - current_hp) / healing_rate
        status_text += f"📈 Восстановление: {healing_rate} HP в минуту\n"
        status_text += f"🕐 До полного восстановления: {int(minutes_to_full)} минут\n"
    else:
        status_text += "✅ Вы полностью здоровы!\n"
    
    status_text += f"\n📊 Смертей: {deaths}"
    
    await msg.answer(status_text)

@dp.message(lambda msg: msg.text and msg.text.lower() == "выживание")
async def survival_command(msg: Message):
    """Показать состояние предметов выживания"""
    user_id = msg.from_user.id
    user = ensure_user(user_id)
    location = user[4]
    
    items = get_user_survival_items(user_id)
    
    if not items:
        await msg.answer("🛡️ У вас нет предметов для выживания.\n\n"
                        "🏪 Купите предметы в разделе 'Выживание' магазина!")
        return
    
    text = "🛡️ Ваши предметы для выживания:\n\n"
    
    for item_name in items:
        item_data = SURVIVAL_ITEMS.get(item_name, {})
        location_name = item_data.get("location", "Неизвестно")
        
        text += f"• {item_name}\n"
        text += f"  📍 Локация: {location_name}\n"
        
        if "survival" in item_data and item_data["survival"]:
            text += f"  🛡️ Защитный предмет\n"
        else:
            text += f"  ✨ Бонусный предмет\n"
        
        text += f"  📝 {item_data.get('description', '')}\n\n"
    
    # Проверяем текущую локацию
    if location != "Тайга":
        has_item, item_name = has_survival_item(user_id, location)
        if has_item:
            text += f"📍 Текущая локация: {location}\n"
            text += f"✅ У вас есть предмет для выживания: {item_name}\n"
            text += f"🛡️ Вы защищены от урона среды\n"
        else:
            text += f"📍 Текущая локация: {location}\n"
            text += f"❌ У вас нет предмета для выживания!\n"
            text += f"⚠️ Каждые 5 охот будет отниматься 50HP\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏪 Магазин выживания", callback_data=f"shop_survival:{user_id}")]
    ])
    
    await msg.answer(text, reply_markup=kb)

# ================== НОВАЯ СИСТЕМА ОХОТЫ ==================

@dp.message(lambda msg: msg.text and msg.text.lower() == "хант")
async def hunt(msg: Message):
    
    can_hunt_result, message = can_hunt(msg.from_user.id)
    if not can_hunt_result:
        await msg.answer(message)
        return
    
    user = ensure_user(msg.from_user.id, msg.from_user.username)
    now = int(time.time())
    
    # Проверка зарядов энергетика
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    user_data = cur.execute("SELECT no_cooldown_charges FROM users WHERE user_id = ?", (msg.from_user.id,)).fetchone()
    no_cd_charges = user_data[0] if user_data else 0
    conn.close()
    
    if no_cd_charges > 0:
        sql.execute("UPDATE users SET no_cooldown_charges = no_cooldown_charges - 1 WHERE user_id = ?", (msg.from_user.id,))
        db.commit()
    else:
        if now - user[5] < HUNT_COOLDOWN:
            wait = HUNT_COOLDOWN - (now - user[5])
            minutes = wait // 60
            seconds = wait % 60
            
            coins = user[1]
            if coins < 20000:
                reset_price = 450
            elif coins < 50000:
                reset_price = 1000
            elif coins < 100000:
                reset_price = 2000
            else:
                reset_price = 2500
            
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=f"🔄 Обнулить таймер за {reset_price}💰", callback_data=f"reset_cooldown:{msg.from_user.id}:{reset_price}")
            ]])
            await msg.answer(f"⏳ Подожди {minutes} мин {seconds} сек.", reply_markup=kb)
            return
    
    sql.execute("UPDATE users SET last_hunt = ?, hunt_counter = hunt_counter + 1 WHERE user_id = ?", (now, msg.from_user.id))
    db.commit()
    
    weather_icon = current_weather.split()[0] if current_weather else "🌤️"
    
    # Выбираем животное
    group, animal, mutation_name, animal_id = choose_animal(user[4], msg.from_user.id)
    
    if not animal:
        await msg.answer(f"{weather_icon} Ты блуждаешь по {user[4]}, но поиски безуспешны.")
        return
    
    # Проверка на стаю (только для мелочи)
    is_pack = False
    pack_size = 1
    
    if group == "Мелочь" and random.randint(1, 100) <= PACK_CHANCE:
        is_pack = True
        pack_size = random.randint(PACK_SIZE[0], PACK_SIZE[1])
    
    # Сохраняем животное в БД
    sql.execute("INSERT INTO temp_hunt (user_id, group_name, animal_id, mutation, created_at) VALUES (?, ?, ?, ?, ?)",
               (msg.from_user.id, group, animal_id, mutation_name if mutation_name else "None", int(time.time())))
    hunt_id = sql.lastrowid
    db.commit()
    
    # Создаём кнопки в зависимости от группы
    display_name = f"{mutation_name} {animal}" if mutation_name else animal
    
    # ========== ВАЖНО: ПРАВИЛЬНАЯ СТРУКТУРА if/elif/else ==========
    if group == "Мелочь":
        if is_pack:
            text = f"{weather_icon} Ты нашёл СТАЮ {display_name}! ({pack_size} особей)"
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔫 Выстрел", callback_data=f"battle_shoot|{hunt_id}")],
                [InlineKeyboardButton(text="🪤 Поймать стаю (25%)", callback_data=f"battle_catch_pack|{hunt_id}")]
            ])
        else:
            text = f"{weather_icon} Ты нашёл {display_name}!"
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔫 Выстрел", callback_data=f"battle_shoot|{hunt_id}")]
            ])
    
    elif group == "Средн":
        text = f"{weather_icon} Ты нашёл {display_name}!"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔫 Выстрел", callback_data=f"battle_shoot|{hunt_id}")],
            [InlineKeyboardButton(text="🥷 Подкрасться (+10% попадание)", callback_data=f"battle_sneak|{hunt_id}")]
        ])
    
    else:  # Опасн, Тяжел, Титан
        text = f"{weather_icon} Ты нашёл {display_name}! (HP: {ANIMAL_HP[group]})"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔫 Выстрел", callback_data=f"battle_shoot|{hunt_id}")],
            [InlineKeyboardButton(text="🥷 Подкрасться (+10% попадание)", callback_data=f"battle_sneak|{hunt_id}")]
        ])
        if group == "Титан":
            kb.inline_keyboard.append([InlineKeyboardButton(text="🏃 Убежать", callback_data=f"battle_escape_pre|{hunt_id}")])
    
    await msg.answer(text, reply_markup=kb)


# ================== ОБРАБОТЧИКИ НОВОЙ СИСТЕМЫ ==================

@dp.callback_query(lambda c: c.data.startswith("battle_catch_pack|"))
async def battle_catch_pack(call: CallbackQuery):
    """Поймать стаю (25% успеха)"""
    hunt_id = int(call.data.split("|")[1])
    
    hunt_data = sql.execute("SELECT user_id, group_name, animal_id, mutation FROM temp_hunt WHERE hunt_id = ?", (hunt_id,)).fetchone()
    if not hunt_data or hunt_data[0] != call.from_user.id:
        await call.answer("❌ Ошибка", show_alert=True)
        return
    
    user_id, group, animal_id, mutation_name = hunt_data
    
    sql.execute("DELETE FROM temp_hunt WHERE hunt_id = ?", (hunt_id,))
    db.commit()
    
    animal_dict = get_animal_by_id(animal_id)
    animal_name = animal_dict['animal'] if animal_dict else "животное"
    
    if random.randint(1, 100) <= CATCH_PACK_SUCCESS_CHANCE:
        pack_size = random.randint(3, 4)
        
        rank = get_user_rank(sql.execute("SELECT total_kills FROM users WHERE user_id = ?", (user_id,)).fetchone()[0])
        base_coins, base_exp = REWARDS[group]
        
        coins = base_coins * pack_size
        exp = base_exp * pack_size
        
        coins += int(coins * rank["bonus_coins"] / 100)
        exp += int(exp * rank["bonus_exp"] / 100)
        
        # ===== ДОБАВЛЯЕМ КАЖДОЕ ЖИВОТНОЕ В ТРОФЕИ =====
        for _ in range(pack_size):
            trophy = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", (user_id, animal_name)).fetchone()
            if trophy:
                sql.execute("UPDATE trophies SET count = count + 1 WHERE user_id = ? AND animal = ?", (user_id, animal_name))
            else:
                sql.execute("INSERT INTO trophies VALUES (?, ?, ?)", (user_id, animal_name, 1))
        
        sql.execute("UPDATE users SET coins = coins + ?, exp = exp + ?, total_kills = total_kills + ?, daily_kills = daily_kills + ? WHERE user_id = ?", 
                   (coins, exp, pack_size, pack_size, user_id))
        db.commit()
        
        await call.message.edit_text(
            f"🪤 **УСПЕХ!** Ты поймал стаю {animal_name}!\n"
            f"📦 Поймано: {pack_size} особей\n"
            f"💰 +{coins} монет\n"
            f"⭐ +{exp} опыта"
        )
    else:
        await call.message.edit_text(f"🪤 **ПРОВАЛ!** Стая {animal_name} убежала. Ты ничего не поймал.")

@dp.callback_query(lambda c: c.data.startswith("battle_sneak|"))
async def battle_sneak(call: CallbackQuery):
    """Подкрасться (+10% к попаданию, при провале - контратака)
    Средние: промах = контратака + убегают
    Остальные: промах = контратака + бой продолжается
    """
    hunt_id = int(call.data.split("|")[1])
    
    hunt_data = sql.execute("SELECT user_id, group_name, animal_id, mutation FROM temp_hunt WHERE hunt_id = ?", (hunt_id,)).fetchone()
    if not hunt_data or hunt_data[0] != call.from_user.id:
        await call.answer("❌ Ошибка", show_alert=True)
        return
    
    user_id, group, animal_id, mutation_name = hunt_data
    
    sql.execute("DELETE FROM temp_hunt WHERE hunt_id = ?", (hunt_id,))
    db.commit()
    
    animal_dict = get_animal_by_id(animal_id)
    animal_name = animal_dict['animal'] if animal_dict else "животное"
    
    user = ensure_user(user_id)
    weapon = user[3]
    location = user[4]
    
    # Получаем текущее здоровье
    current_hp, max_hp = get_user_health(user_id)
    
    # Проверяем попадание с бонусом +10%
    groups_order = ["Мелочь", "Средн", "Опасн", "Тяжел", "Титан"]
    group_index = groups_order.index(group)
    weapon_data = get_weapon_data(weapon)
    base_chance = weapon_data["chances"][group_index]
    
    # Бонус подкрадывания +10%
    final_chance = base_chance + 10
    final_chance = max(1, min(99, final_chance))
    
    hit_success = random.randint(1, 100) <= final_chance
    
    if hit_success:
        # ✅ УСПЕХ - начинаем бой с бонусом +10% к попаданию
        start_battle(user_id, animal_id, animal_name, group, False, 1, 10)
        await show_battle_menu(call, user_id, animal_name, group)
    else:
        # ❌ ПРОВАЛ - контратака
        damage = SNEAK_FAIL_DAMAGE.get(group, 25)
        new_hp = update_health(user_id, -damage)
        
        if new_hp <= 0:
            await call.message.edit_text(
                f"🥷 Ты попытался подкрасться к {animal_name}, но провалился!\n"
                f"💥 Животное контратаковало! -{damage} HP\n"
                f"💀 Ты погиб!"
            )
            return
        
        # ===== РАЗНОЕ ПОВЕДЕНИЕ В ЗАВИСИМОСТИ ОТ ГРУППЫ =====
        if group == "Средн":
            # Средние - убегают после контратаки
            await call.message.edit_text(
                f"🥷 Ты попытался подкрасться к {animal_name}, но провалился!\n"
                f"💥 Животное контратаковало! -{damage} HP\n"
                f"❤️ Осталось здоровья: {new_hp}/{max_hp}\n\n"
                f"🏃 Животное убежало."
            )
        else:
            # Опасн, Тяжел, Титан - не убегают, начинается бой
            await call.message.edit_text(
                f"🥷 Ты попытался подкрасться к {animal_name}, но провалился!\n"
                f"💥 Животное контратаковало! -{damage} HP\n"
                f"❤️ Осталось здоровья: {new_hp}/{max_hp}\n\n"
                f"⚔️ Животное готовится к бою!"
            )
            # Начинаем бой
            start_battle(user_id, animal_id, animal_name, group, False, 1, 0)
            await show_battle_menu(call, user_id, animal_name, group)


@dp.callback_query(lambda c: c.data.startswith("battle_escape_pre|"))
async def battle_escape_pre(call: CallbackQuery):
    """Попытка убежать до боя (только для титанов)"""
    hunt_id = int(call.data.split("|")[1])
    
    hunt_data = sql.execute("SELECT user_id, group_name, animal_id, mutation FROM temp_hunt WHERE hunt_id = ?", (hunt_id,)).fetchone()
    if not hunt_data or hunt_data[0] != call.from_user.id:
        await call.answer("❌ Ошибка", show_alert=True)
        return
    
    user_id, group, animal_id, mutation_name = hunt_data
    
    sql.execute("DELETE FROM temp_hunt WHERE hunt_id = ?", (hunt_id,))
    db.commit()
    
    animal_dict = get_animal_by_id(animal_id)
    animal_name = animal_dict['animal'] if animal_dict else "животное"
    
    chance = ESCAPE_CHANCES.get(group, 100)
    
    if random.randint(1, 100) <= chance:
        await call.message.edit_text(f"🏃 Ты успешно убежал от {animal_name}!")
    else:
        await call.message.edit_text(
            f"🏃 Ты попытался убежать, но {animal_name} догнал тебя!\n"
            f"⚔️ Начинается бой!"
        )
        start_battle(user_id, animal_id, animal_name, group)
        await show_battle_menu(call, user_id, animal_name, group)


@dp.callback_query(lambda c: c.data.startswith("battle_shoot|"))
async def battle_shoot(call: CallbackQuery):
    """Начать бой с обычным выстрелом"""
    hunt_id = int(call.data.split("|")[1])
    
    hunt_data = sql.execute("SELECT user_id, group_name, animal_id, mutation FROM temp_hunt WHERE hunt_id = ?", (hunt_id,)).fetchone()
    if not hunt_data or hunt_data[0] != call.from_user.id:
        await call.answer("❌ Ошибка", show_alert=True)
        return
    
    user_id, group, animal_id, mutation_name = hunt_data
    
    sql.execute("DELETE FROM temp_hunt WHERE hunt_id = ?", (hunt_id,))
    db.commit()
    
    animal_dict = get_animal_by_id(animal_id)
    animal_name = animal_dict['animal'] if animal_dict else "животное"
    
    start_battle(user_id, animal_id, animal_name, group)
    await show_battle_menu(call, user_id, animal_name, group)


# ================== НОВАЯ СИСТЕМА БОЯ (БЕЗ СБРОСОВ HP) ==================

# ================== НОВАЯ БОЕВАЯ СИСТЕМА (ПОЛНОСТЬЮ ИСПРАВЛЕНА) ==================

async def simple_shot(call: CallbackQuery, user_id: int, battle: tuple):
    """Простой выстрел для мелочи и средних (БЕЗ контратаки)"""
    animal_name = battle[2]
    group = battle[3]
    
    user = ensure_user(user_id)
    weapon = user[3]
    location = user[4]
    
    groups_order = ["Мелочь", "Средн", "Опасн", "Тяжел", "Титан"]
    group_index = groups_order.index(group)
    weapon_data = get_weapon_data(weapon)
    base_chance = weapon_data["chances"][group_index]
    
    # Погода
    weather_effects = WEATHER_EFFECTS.get(current_weather, {})
    hit_bonus = weather_effects.get("hit", 0)
    
    # Локация
    location_bonus = get_weapon_location_bonus(weapon, location)
    hit_bonus += location_bonus["hit"]
    
    final_chance = base_chance + hit_bonus
    final_chance = max(1, min(99, final_chance))
    
    hit_success = random.randint(1, 100) <= final_chance
    
    # Завершаем бой
    end_battle(user_id)
    
    if hit_success:
        rank = get_user_rank(user[7])
        base_coins, base_exp = REWARDS[group]
        coins = base_coins + int(base_coins * rank["bonus_coins"] / 100)
        exp = base_exp + int(base_exp * rank["bonus_exp"] / 100)
        
        if location_bonus["coins"] != 0:
            coins = int(coins * (1 + location_bonus["coins"] / 100))
        if location_bonus["exp"] != 0:
            exp = int(exp * (1 + location_bonus["exp"] / 100))
        
        # Трофеи
        trophy = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", (user_id, animal_name)).fetchone()
        if trophy:
            sql.execute("UPDATE trophies SET count = count + 1 WHERE user_id = ? AND animal = ?", (user_id, animal_name))
        else:
            sql.execute("INSERT INTO trophies VALUES (?, ?, ?)", (user_id, animal_name, 1))
        
        sql.execute("UPDATE users SET coins = coins + ?, exp = exp + ?, total_kills = total_kills + 1, daily_kills = daily_kills + 1 WHERE user_id = ?", 
                   (coins, exp, user_id))
        db.commit()
        
        await call.message.edit_text(f"🎯 **ПОПАДАНИЕ!**\n\n🐾 {animal_name} убит!\n💰 +{coins} монет\n⭐ +{exp} опыта")
    else:
        miss_phrase = random.choice(MISS_PHRASES)
        await call.message.edit_text(miss_phrase)


async def show_battle_menu(call: CallbackQuery, user_id: int, animal_name: str = None, group: str = None):
    """Показывает меню боя - использует ТЕКУЩЕЕ состояние из battle_state"""
    
    # ✅ ПОЛУЧАЕМ АКТУАЛЬНОЕ СОСТОЯНИЕ БОЯ
    battle = get_battle_state(user_id)
    if not battle:
        await call.answer("❌ Бой не найден", show_alert=True)
        return
    
    group = battle[3]
    animal_name = battle[2]  # получаем имя животного из battle_state
    
    # ✅ ПОЛУЧАЕМ ЛОКАЦИЮ ИЗ ДАННЫХ ПОЛЬЗОВАТЕЛЯ
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    result = cur.execute("SELECT location FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    location = result[0] if result else "Тайга"
    
    # ✅ БЕРЁМ АКТУАЛЬНОЕ HP ИЗ БД
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    battle_data = cur.execute("SELECT animal_hp, animal_max_hp FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    if battle_data:
        animal_current_hp = battle_data[0]
        animal_max_hp = battle_data[1]
    else:
        animal_current_hp = ANIMAL_HP.get(group, 100)
        animal_max_hp = ANIMAL_HP.get(group, 100)
    
    current_hp, max_hp = get_user_health(user_id)
    
    text = f"⚔️ **БОЙ!** ⚔️\n\n"
    text += f"🐾 {animal_name} ({group})\n"
    text += f"❤️ HP животного: {animal_current_hp}/{animal_max_hp}\n\n"
    text += f"❤️ Твоё HP: {current_hp}/{max_hp}\n"
    text += f"\n📍 Локация: {location}\n"
    
    # Для тяжелых и титанов - выбор части тела
    if group in ["Тяжел", "Титан"] and location in BODY_PARTS:
        body_buttons = []
        for part_name in BODY_PARTS[location].keys():
            body_buttons.append([InlineKeyboardButton(
                text=part_name,
                callback_data=f"battle_body|{user_id}|{part_name}"
            )])
        body_kb = InlineKeyboardMarkup(inline_keyboard=body_buttons)
        
        await call.message.edit_text(text + "\n🎯 **Выбери часть тела для выстрела:**", reply_markup=body_kb)
        return
    
    # Кнопки для опасных
    user = ensure_user(user_id)
    buttons = [
        [InlineKeyboardButton(text="🔫 Выстрел", callback_data=f"battle_attack|{user_id}")],
    ]
    
    # Кнопка способности оружия
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    ability_used = cur.execute("SELECT ability_used FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    if ability_used and ability_used[0] == 0:
        weapon = user[3]
        ability, ability_desc, ability_chance = get_weapon_ability(weapon)
        if ability:
            buttons[0].append(InlineKeyboardButton(
                text=f"✨ {ability_desc} (50%)", 
                callback_data=f"battle_ability|{user_id}"
            ))
    
    # Кнопка побега
    if group == "Титан":
        buttons.append([InlineKeyboardButton(text="🏃 Бежать (10%)", callback_data=f"battle_escape|{user_id}")])
    elif group == "Тяжел":
        buttons.append([InlineKeyboardButton(text="🏃 Бежать (75%)", callback_data=f"battle_escape|{user_id}")])
    else:
        buttons.append([InlineKeyboardButton(text="🏃 Бежать", callback_data=f"battle_escape|{user_id}")])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    try:
        await call.message.edit_text(text, reply_markup=kb)
    except Exception as e:
        if "message is not modified" not in str(e):
            await call.message.answer(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("battle_body|"))
async def battle_body_part(call: CallbackQuery):
    """Выбор части тела для выстрела"""
    parts = call.data.split("|")
    if len(parts) < 3:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    user_id = int(parts[1])
    body_part = parts[2]
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не твой бой!", show_alert=True)
        return
    
    user = ensure_user(user_id)
    location = user[4]
    
    # Проверяем, существует ли такая часть тела для этой локации
    if location not in BODY_PARTS or body_part not in BODY_PARTS[location]:
        await call.answer("❌ Неверная часть тела", show_alert=True)
        return
    
    # Сохраняем выбранную часть тела
    part_code = list(BODY_PARTS[location].keys()).index(body_part) + 1
    
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO battle_mods (user_id, hit_bonus, damage_bonus) VALUES (?, 0, 0)", (user_id,))
    cur.execute("UPDATE battle_mods SET hit_bonus = ? WHERE user_id = ?", (part_code, user_id))
    conn.commit()
    conn.close()
    
    await call.answer(f"✅ Выбрана цель: {body_part}", show_alert=True)
    
    # ✅ ПОЛУЧАЕМ АКТУАЛЬНОЕ СОСТОЯНИЕ БОЯ
    battle = get_battle_state(user_id)
    if not battle:
        await call.answer("❌ Бой не найден", show_alert=True)
        return
    
    group = battle[3]
    # ✅ БЕРЁМ АКТУАЛЬНОЕ HP ИЗ БД, А НЕ ИЗ СТАРОЙ ПЕРЕМЕННОЙ
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    result = cur.execute("SELECT animal_hp, animal_max_hp FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    if result:
        animal_current_hp = result[0]
        animal_max_hp = result[1]
    else:
        animal_current_hp = ANIMAL_HP.get(group, 100)
        animal_max_hp = ANIMAL_HP.get(group, 100)
    
    current_hp, max_hp = get_user_health(user_id)
  
    text = f"⚔️ **БОЙ!** ⚔️\n\n"
    text += f"🐾 {battle[2]} ({group})\n"
    text += f"❤️ HP животного: {animal_current_hp}/{animal_max_hp}\n\n"
    text += f"❤️ Твоё HP: {current_hp}/{max_hp}\n"
    text += f"🎯 Цель: {body_part}\n"
    text += f"\n📍 Локация: {location}\n\n"
    text += f"⚔️ **ТВОЙ ХОД!**"
    
    # Получаем способность оружия
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    ability_used = cur.execute("SELECT ability_used FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    buttons = [[InlineKeyboardButton(text="🔫 Выстрел", callback_data=f"battle_attack|{user_id}")]]
    
    if ability_used and ability_used[0] == 0:
        weapon = user[3]
        ability, ability_desc, ability_chance = get_weapon_ability(weapon)
        if ability:
            buttons[0].append(InlineKeyboardButton(
                text=f"✨ {ability_desc} (50%)", 
                callback_data=f"battle_ability|{user_id}"
            ))
    
    if group == "Титан":
        buttons.append([InlineKeyboardButton(text="🏃 Бежать (10%)", callback_data=f"battle_escape|{user_id}")])
    else:
        buttons.append([InlineKeyboardButton(text="🏃 Бежать (75%)", callback_data=f"battle_escape|{user_id}")])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("battle_attack|"))
async def battle_attack(call: CallbackQuery):
    user_id = int(call.data.split("|")[1])
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не твой бой!", show_alert=True)
        return

    # ПОЛУЧАЕМ ТЕКУЩЕЕ СОСТОЯНИЕ БОЯ ИЗ БД
    battle = get_battle_state(user_id)
    if not battle:
        await call.message.edit_text("❌ Бой не найден")
        return

    animal_name = battle[2]
    group = battle[3]
    sneak_bonus = battle[10] if len(battle) > 10 else 0
    
    # Для мелочи и средних - простой выстрел
    if group in ["Мелочь", "Средн"]:
        await simple_shot(call, user_id, battle)
        return
    
    user = ensure_user(user_id)
    weapon = user[3]
    location = user[4]
    current_hp, max_hp = get_user_health(user_id)
    
    # Расчёт попадания
    groups_order = ["Мелочь", "Средн", "Опасн", "Тяжел", "Титан"]
    group_index = groups_order.index(group)
    weapon_data = get_weapon_data(weapon)
    base_chance = weapon_data["chances"][group_index]
    
    weather_effects = WEATHER_EFFECTS.get(current_weather, {})
    hit_bonus = weather_effects.get("hit", 0)
    
    location_bonus = get_weapon_location_bonus(weapon, location)
    hit_bonus += location_bonus["hit"]
    hit_bonus += sneak_bonus
    
    final_chance = base_chance + hit_bonus
    final_chance = max(1, min(99, final_chance))
    
    # Получаем выбранную часть тела
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    mod = cur.execute("SELECT hit_bonus FROM battle_mods WHERE user_id = ?", (user_id,)).fetchone()
    cur.execute("DELETE FROM battle_mods WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    body_part = None
    if mod and mod[0] > 0 and location in BODY_PARTS:
        parts = list(BODY_PARTS[location].keys())
        if parts:
            body_part = parts[mod[0] % len(parts)]
    
    # ========== ПОЛУЧАЕМ ТЕКУЩЕЕ HP ЖИВОТНОГО ДО ВСЕХ ДЕЙСТВИЙ ==========
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    current_animal_hp = cur.execute("SELECT animal_hp FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()[0]
    animal_max_hp = cur.execute("SELECT animal_max_hp FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()[0]
    conn.close()
    
    hit_success = random.randint(1, 100) <= final_chance
    
    # ========== ПРОМАХ ==========
    if not hit_success:
        miss_phrase = random.choice(MISS_PHRASES)
        
        # ========== ВАЖНО: ДЛЯ СРЕДНИХ ЖИВОТНЫХ ПРИ ПОДКРАДЫВАНИИ ВСЕГДА АТАКА ==========
        # Определяем, было ли это подкрадывание (sneak_bonus > 0)
        was_sneak = sneak_bonus > 0
        
        if group == "Средн" and was_sneak:
            # При подкрадывании к среднему и промахе - ВСЕГДА контратака (без шанса убежать)
            damage = SNEAK_FAIL_DAMAGE.get(group, 25)
            new_hp = update_health(user_id, -damage)
            animal_msg = f"💥 {animal_name} заметил тебя и контратаковал! -{damage} HP"
            animal_ran = False
            animal_damage = damage
            
            # Сохраняем текущее HP животного (оно не изменилось)
            animal_current_hp = current_animal_hp
            
        else:
            # Обычное действие животного
            animal_damage, animal_msg, animal_ran, hit_mod = animal_action(user_id, group, location)
            
            # Сохраняем штраф от защиты
            if hit_mod != 0:
                conn = sqlite3.connect("hunt.db")
                cur = conn.cursor()
                cur.execute("INSERT OR REPLACE INTO battle_mods (user_id, hit_bonus, damage_bonus) VALUES (?, ?, 0)", 
                           (user_id, hit_mod))
                conn.commit()
                conn.close()
            
            # HP животного не изменилось при промахе
            animal_current_hp = current_animal_hp
            
            if animal_damage > 0:
                update_health(user_id, -animal_damage)
                current_hp, max_hp = get_user_health(user_id)
        
        # В разделе "ПРОМАХ" после animal_action, замените:
        if animal_ran:
            end_battle(user_id)
            await call.message.edit_text(f"{miss_phrase}\n\n{animal_msg}\n\n⚔️ Бой закончен.")
            return

        if animal_damage > 0:
            current_hp, max_hp = get_user_health(user_id)
            if current_hp <= 0:
                end_battle(user_id)
                await call.message.edit_text(f"{miss_phrase}\n\n{animal_msg}\n\n💀 Ты погиб!")
                return

        # ✅ ПОЛУЧАЕМ АКТУАЛЬНОЕ HP ЖИВОТНОГО ПОСЛЕ ВСЕХ ЭФФЕКТОВ
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        battle = cur.execute("SELECT animal_hp, animal_max_hp FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        if battle:
            animal_current_hp = battle[0]
            animal_max_hp = battle[1]
        else:
            animal_current_hp = current_animal_hp
            animal_max_hp = animal_max_hp

        # Увеличиваем ход
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        cur.execute("UPDATE battle_state SET turn = turn + 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

        # ✅ ИСПРАВЛЕНО: используем актуальное animal_current_hp
        text = (
            f"{miss_phrase}\n\n"
            f"{animal_msg}\n\n"
            f"❤️ HP животного: {animal_current_hp}/{animal_max_hp}\n"
            f"❤️ Твоё HP: {current_hp}/{max_hp}\n\n"
            f"⚔️ **ТВОЙ ХОД!**"
        )
        
        # Создаём кнопки
        buttons = [[InlineKeyboardButton(text="🔫 Выстрел", callback_data=f"battle_attack|{user_id}")]]
        
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        ability_used = cur.execute("SELECT ability_used FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
        
        if ability_used and ability_used[0] == 0:
            ability, ability_desc, ability_chance = get_weapon_ability(weapon)
            if ability:
                buttons[0].append(InlineKeyboardButton(
                    text=f"✨ {ability_desc} (50%)", 
                    callback_data=f"battle_ability|{user_id}"
                ))
        
        # Кнопки побега
        if group == "Титан":
            buttons.append([InlineKeyboardButton(text="🏃 Бежать (10%)", callback_data=f"battle_escape|{user_id}")])
        elif group == "Тяжел":
            buttons.append([InlineKeyboardButton(text="🏃 Бежать (75%)", callback_data=f"battle_escape|{user_id}")])
        else:
            buttons.append([InlineKeyboardButton(text="🏃 Бежать", callback_data=f"battle_escape|{user_id}")])
        
        # Для тяжелых и титанов - показываем выбор части тела
        if group in ["Тяжел", "Титан"] and location in BODY_PARTS:
            text += f"\n\n🎯 **Выбери часть тела для следующего выстрела:**"
            body_buttons = []
            for part_name in BODY_PARTS[location].keys():
                body_buttons.append([InlineKeyboardButton(
                    text=part_name,
                    callback_data=f"battle_body|{user_id}|{part_name}"
                )])
            kb = InlineKeyboardMarkup(inline_keyboard=body_buttons)
            await call.message.edit_text(text, reply_markup=kb)
            return
        
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.edit_text(text, reply_markup=kb)
        return
    
    # ========== ПОПАДАНИЕ (остальной код без изменений) ==========
    
    # Проверка способности титана
    if group == "Титан" and location in TITAN_ABILITIES:
        blocked, ability_msg, extra_damage = apply_titan_ability(location, user_id)
        if blocked:
            animal_damage, animal_msg, animal_ran, _ = animal_action(user_id, group, location)
            if animal_damage > 0:
                update_health(user_id, -animal_damage)
                
            conn = sqlite3.connect("hunt.db")
            cur = conn.cursor()
            battle = cur.execute("SELECT animal_hp, animal_max_hp FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
            conn.close()
            if battle:
                animal_current_hp = battle[0]
                animal_max_hp = battle[1]
            else:
                animal_current_hp = current_animal_hp
                animal_max_hp = animal_max_hp
            
            text = f"{ability_msg}\n\n{animal_msg}\n❤️ Твоё HP: {current_hp}/{max_hp}\n❤️ HP животного: {animal_current_hp}/{animal_max_hp}\n\n⚔️ **ТВОЙ ХОД!**"
            buttons = [[InlineKeyboardButton(text="🔫 Выстрел", callback_data=f"battle_attack|{user_id}")]]
            if group == "Титан":
                buttons.append([InlineKeyboardButton(text="🏃 Бежать (10%)", callback_data=f"battle_escape|{user_id}")])
            else:
                buttons.append([InlineKeyboardButton(text="🏃 Бежать", callback_data=f"battle_escape|{user_id}")])
            
            await call.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            return
    
    # Расчёт урона
    damage, _, extra_effect = calculate_damage_with_ability(weapon, group, location, user_id, body_part)
    
    new_animal_hp = current_animal_hp - damage
    
    # Обновляем HP в БД
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("UPDATE battle_state SET animal_hp = ? WHERE user_id = ?", (new_animal_hp, user_id))
    conn.commit()
    conn.close()
    
    # Обработка особых эффектов
    if extra_effect == "instant_kill":
        new_animal_hp = 0
    
    # ========== СМЕРТЬ ЖИВОТНОГО ==========
    if new_animal_hp <= 0:
        end_battle(user_id)
        
        rank = get_user_rank(user[7])
        base_coins, base_exp = REWARDS[group]
        coins = base_coins + int(base_coins * rank["bonus_coins"] / 100)
        exp = base_exp + int(base_exp * rank["bonus_exp"] / 100)
        
        if location_bonus["coins"] != 0:
            coins = int(coins * (1 + location_bonus["coins"] / 100))
        if location_bonus["exp"] != 0:
            exp = int(exp * (1 + location_bonus["exp"] / 100))
        
        mutation_name = battle[4] if len(battle) > 4 else None
        if mutation_name and mutation_name != "None":
            mutation_data = MUTATIONS.get(mutation_name)
            if mutation_data:
                coins = int(coins * mutation_data["coins_mult"])
                exp = int(exp * mutation_data["exp_mult"])
        
        sql.execute("UPDATE users SET coins = coins + ?, exp = exp + ? WHERE user_id = ?", (coins, exp, user_id))
        sql.execute("UPDATE users SET total_kills = total_kills + 1, daily_kills = daily_kills + 1 WHERE user_id = ?", (user_id,))
        
        trophy = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", (user_id, animal_name)).fetchone()
        if trophy:
            sql.execute("UPDATE trophies SET count = count + 1 WHERE user_id = ? AND animal = ?", (user_id, animal_name))
        else:
            sql.execute("INSERT INTO trophies VALUES (?, ?, ?)", (user_id, animal_name, 1))
        
        db.commit()
        
        await call.message.edit_text(f"🎯 **ПОБЕДА!**\n\n🐾 {animal_name} повержен!\n💰 +{coins} монет\n⭐ +{exp} опыта")
        return
    
    # ========== ЖИВОТНОЕ ВЫЖИЛО - ХОД ЖИВОТНОГО ==========
    animal_damage, animal_msg, animal_ran, _ = animal_action(user_id, group, location)
    
    # Увеличиваем ход
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("UPDATE battle_state SET turn = turn + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    if animal_ran:
        end_battle(user_id)
        await call.message.edit_text(f"🎯 **ПОПАДАНИЕ!** Урон: {damage}\n❤️ HP животного: {new_animal_hp}/{animal_max_hp}\n\n{animal_msg}\n\n⚔️ Бой закончен. Животное убежало.")
        return
    
    if animal_damage > 0:
        update_health(user_id, -animal_damage)
        current_hp, max_hp = get_user_health(user_id)
        
        if current_hp <= 0:
            end_battle(user_id)
            await call.message.edit_text(f"🎯 **ПОПАДАНИЕ!** Урон: {damage}\n❤️ HP животного: {new_animal_hp}/{animal_max_hp}\n\n{animal_msg}\n💀 Ты погиб!")
            return
    
    # ========== ПОКАЗЫВАЕМ РЕЗУЛЬТАТ ==========
    text = f"🎯 **ПОПАДАНИЕ!** Урон: {damage}\n"
    text += f"❤️ HP животного: {new_animal_hp}/{animal_max_hp}\n\n"
    text += f"{animal_msg}\n"
    text += f"❤️ Твоё HP: {current_hp}/{max_hp}\n"
    
    # Для тяжелых и титанов - снова выбор части тела
    if group in ["Тяжел", "Титан"] and location in BODY_PARTS:
        text += f"\n🎯 **Выбери часть тела для следующего выстрела:**"
        body_buttons = []
        for part_name in BODY_PARTS[location].keys():
            body_buttons.append([InlineKeyboardButton(
                text=part_name,
                callback_data=f"battle_body|{user_id}|{part_name}"
            )])
        body_kb = InlineKeyboardMarkup(inline_keyboard=body_buttons)
        await call.message.edit_text(text, reply_markup=body_kb)
        return
    
    # Для опасных - обычные кнопки
    text += f"\n\n⚔️ **ТВОЙ ХОД!**"
    buttons = [[InlineKeyboardButton(text="🔫 Выстрел", callback_data=f"battle_attack|{user_id}")]]
    
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    ability_used = cur.execute("SELECT ability_used FROM battle_state WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    if ability_used and ability_used[0] == 0:
        ability, ability_desc, ability_chance = get_weapon_ability(weapon)
        if ability:
            buttons[0].append(InlineKeyboardButton(
                text=f"✨ {ability_desc} (50%)", 
                callback_data=f"battle_ability|{user_id}"
            ))
    
    if group == "Титан":
        buttons.append([InlineKeyboardButton(text="🏃 Бежать (10%)", callback_data=f"battle_escape|{user_id}")])
    else:
        buttons.append([InlineKeyboardButton(text="🏃 Бежать", callback_data=f"battle_escape|{user_id}")])
    
    await call.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


@dp.callback_query(lambda c: c.data.startswith("battle_ability|"))
async def battle_ability(call: CallbackQuery):
    """Использование способности оружия (1 раз за бой, 50% шанс)"""
    user_id = int(call.data.split("|")[1])
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не твой бой!", show_alert=True)
        return
    
    battle = get_battle_state(user_id)
    if not battle:
        await call.message.edit_text("❌ Бой не найден")
        return
    
    user = ensure_user(user_id)
    weapon = user[3]
    ability, ability_desc, ability_chance = get_weapon_ability(weapon)
    
    if not ability:
        await call.answer("❌ У этого оружия нет способности!", show_alert=True)
        return
    
    # 50% ШАНС НА УСПЕХ
    if random.randint(1, 100) > 50:
        await call.answer(f"❌ Способность '{ability_desc}' не сработала! (50% шанс)", show_alert=True)
        # НЕ ОТМЕЧАЕМ КАК ИСПОЛЬЗОВАННУЮ - кнопка остаётся
        await show_battle_menu(call, user_id, battle[2], battle[3])
        return
    
    # ТОЛЬКО ЗДЕСЬ отмечаем, что способность использована
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("UPDATE battle_state SET ability_used = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    # Получаем текущее HP животного
    animal_hp = battle[5]
    location = user[4]
    
    # Применяем эффект способности
    final_damage, ability_msg, extra_effect = apply_weapon_ability(ability, user_id, 0, animal_hp, location)
    
    # Если способность наносит урон
    if final_damage > 0:
        new_animal_hp = animal_hp - final_damage
        if new_animal_hp < 0:
            new_animal_hp = 0
        
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        cur.execute("UPDATE battle_state SET animal_hp = ? WHERE user_id = ?", (new_animal_hp, user_id))
        conn.commit()
        conn.close()
        
        # Проверяем смерть животного
        if new_animal_hp <= 0:
            end_battle(user_id)
            
            rank = get_user_rank(user[7])
            base_coins, base_exp = REWARDS[battle[3]]
            coins = base_coins + int(base_coins * rank["bonus_coins"] / 100)
            exp = base_exp + int(base_exp * rank["bonus_exp"] / 100)
            
            location_bonus = get_weapon_location_bonus(weapon, location)
            if location_bonus["coins"] != 0:
                coins = int(coins * (1 + location_bonus["coins"] / 100))
            if location_bonus["exp"] != 0:
                exp = int(exp * (1 + location_bonus["exp"] / 100))
            
            sql.execute("UPDATE users SET coins = coins + ?, exp = exp + ? WHERE user_id = ?", (coins, exp, user_id))
            sql.execute("UPDATE users SET total_kills = total_kills + 1, daily_kills = daily_kills + 1 WHERE user_id = ?", (user_id,))
            
            trophy = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", (user_id, battle[2])).fetchone()
            if trophy:
                sql.execute("UPDATE trophies SET count = count + 1 WHERE user_id = ? AND animal = ?", (user_id, battle[2]))
            else:
                sql.execute("INSERT INTO trophies VALUES (?, ?, ?)", (user_id, battle[2], 1))
            
            db.commit()
            
            await call.message.edit_text(
                f"✨ **СПОСОБНОСТЬ АКТИВИРОВАНА!** ✨\n\n"
                f"{ability_msg}\n\n"
                f"🎯 **ПОБЕДА!**\n"
                f"🐾 {battle[2]} повержен!\n"
                f"💰 +{coins} монет\n"
                f"⭐ +{exp} опыта"
            )
            return
    
    await call.answer(f"✅ Способность '{ability_desc}' сработала!", show_alert=True)
    
    await call.message.edit_text(
        f"✨ **СПОСОБНОСТЬ АКТИВИРОВАНА!** ✨\n\n"
        f"{ability_msg}\n\n"
        f"⚔️ Продолжаем бой!"
    )
    
    # Увеличиваем ход
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    cur.execute("UPDATE battle_state SET turn = turn + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    await show_battle_menu(call, user_id, battle[2], battle[3])


@dp.callback_query(lambda c: c.data.startswith("battle_escape|"))
async def battle_escape(call: CallbackQuery):
    """Попытка убежать во время боя"""
    user_id = int(call.data.split("|")[1])
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не твой бой!", show_alert=True)
        return
    
    battle = get_battle_state(user_id)
    if not battle:
        await call.message.edit_text("❌ Бой не найден")
        return
    
    group = battle[3]
    chance = ESCAPE_CHANCES.get(group, 100)
    
    if random.randint(1, 100) <= chance:
        end_battle(user_id)
        await call.message.edit_text("🏃 Ты успешно убежал!")
    else:
        damage = CONTRATTACK_DAMAGE.get(group, 50)
        update_health(user_id, -damage)
        current_hp, max_hp = get_user_health(user_id)
        
        if current_hp <= 0:
            end_battle(user_id)
            await call.message.edit_text(f"🏃 Ты попытался убежать, но животное догнало тебя!\n💥 -{damage} HP\n💀 Ты погиб!")
        else:
            # Увеличиваем ход
            conn = sqlite3.connect("hunt.db")
            cur = conn.cursor()
            cur.execute("UPDATE battle_state SET turn = turn + 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            
            await call.message.edit_text(f"🏃 Ты попытался убежать, но животное догнало тебя!\n💥 -{damage} HP\n❤️ Осталось: {current_hp}/{max_hp}\n\n⚔️ Бой продолжается!")
            await show_battle_menu(call, user_id, battle[2], group)

@dp.callback_query(lambda c: c.data.startswith("reset_cooldown"))
async def reset_cooldown(call: CallbackQuery):
    """Сброс таймера охоты за монеты"""
    try:
        data_parts = call.data.split(":")
        if len(data_parts) < 2:
            await call.answer("❌ Ошибка данных", show_alert=True)
            return
        
        user_id = int(data_parts[1])
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш таймер!", show_alert=True)
            return
        
        # Определяем цену сброса
        user = ensure_user(call.from_user.id)
        coins = user[1]
        
        if coins < 20000:
            reset_price = 450
        elif coins < 50000:
            reset_price = 1000
        elif coins < 100000:
            reset_price = 2000
        else:
            reset_price = 2500
        
        # Если цена передана в callback, используем её
        if len(data_parts) >= 3:
            reset_price = int(data_parts[2])
        
        if coins < reset_price:
            await call.answer(f"❌ Недостаточно монет! Нужно {reset_price}💰", show_alert=True)
            return
        
        # Списываем монеты и сбрасываем таймер
        sql.execute("UPDATE users SET coins = coins - ?, last_hunt = 0 WHERE user_id = ?", 
                   (reset_price, call.from_user.id))
        db.commit()
        
        await call.message.edit_text("✅ Таймер охоты обнулен! Можете снова охотиться.")
        
    except Exception as e:
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)

# ================== ИНВЕНТАРЬ ==================
@dp.message(lambda msg: msg.text and msg.text.lower() in ["инв", "инвен", "инвентарь"])
async def inventory(msg: Message):
    user = ensure_user(msg.from_user.id, msg.from_user.username)
    
    # Получаем скин профиля отдельным запросом
    theme_result = sql.execute("SELECT profile_theme FROM users WHERE user_id = ?", (msg.from_user.id,)).fetchone()
    current_theme = theme_result[0] if theme_result and theme_result[0] else "standard"
    if isinstance(current_theme, int):
        current_theme = "standard"
    current_theme = str(current_theme).lower()
    
    rank = get_user_rank(user[7])
    prestige_level = user[10] if len(user) > 10 else 0
    current_title = user[9] if len(user) > 9 and user[9] else ""
    
    # ВАЖНО: Получаем current_status и current_quote из user
    current_status = user[36] if len(user) > 36 and user[36] else ""
    current_quote = user[37] if len(user) > 37 and user[37] else ""
    
    username = msg.from_user.username or msg.from_user.first_name
    
    current_hp, max_hp = get_user_health(msg.from_user.id)
    equipment = get_user_equipment(msg.from_user.id)
    equipment_bonuses = get_equipment_bonuses(msg.from_user.id)
    
    # ===== СЛОВАРИ ДЛЯ СКИНОВ =====
    default_emojis = {
        "prestige": "⭐",
        "streak": "📆",
        "health": "❤️",
        "weapon": "🔫",
        "location": "📍",
        "coins": "💰",
        "level": "📊",
        "kills_today": "🎯",
        "kills_total": "🎯",
        "deaths": "💀",
        "artifacts": "🔱"
    }
    
    # Скины по локациям
    theme_emojis = {
        "тайга": {
            "prestige": "🌳", "streak": "🪵", "health": "💚", "weapon": "🏹",
            "location": "🌲", "coins": "🫐", "level": "🐻", "kills_today": "🍃",
            "kills_total": "🍃", "deaths": "🍂", "artifacts": "🍄"
        },
        "саванна": {
            "prestige": "☀️", "streak": "⌛", "health": "🧡", "weapon": "🪃",
            "location": "🏜️", "coins": "💵", "level": "🔶", "kills_today": "🐫",
            "kills_total": "🐪", "deaths": "🌵", "artifacts": "✨"
        },
        "арктика": {
            "prestige": "❄️", "streak": "🧤", "health": "🩵", "weapon": "🧊",
            "location": "🌨️", "coins": "🐧", "level": "🐻‍❄️", "kills_today": "🏒",
            "kills_total": "🏒", "deaths": "⛄", "artifacts": "💎"
        },
        "джунгли": {
            "prestige": "☀️", "streak": "🌿", "health": "💚", "weapon": "🦎",
            "location": "🌴", "coins": "🍃", "level": "🍀", "kills_today": "🐒",
            "kills_total": "🐒", "deaths": "🐍", "artifacts": "🗿"
        },
        "горы": {
            "prestige": "🦅", "streak": "📈", "health": "🤍", "weapon": "⛏️",
            "location": "⛰️", "coins": "🏺", "level": "🏔️", "kills_today": "⚒️",
            "kills_total": "⚒️", "deaths": "🥀", "artifacts": "🎒"
        },
        "древний мир": {
            "prestige": "🦕", "streak": "⏳", "health": "💚", "weapon": "🦴",
            "location": "🦖", "coins": "🪨", "level": "🧬", "kills_today": "🌿",
            "kills_total": "🌿", "deaths": "🦟", "artifacts": "📜"
        },
        "подводный мир": {
            "prestige": "🪸", "streak": "🦈", "health": "💙", "weapon": "🔱",
            "location": "🌊", "coins": "🪙", "level": "💧", "kills_today": "🎣",
            "kills_total": "🎣", "deaths": "🏴‍☠️", "artifacts": "⚓"
        },
        "болото проклятых": {
            "prestige": "🌿", "streak": "🪵", "health": "🤎", "weapon": "🪓",
            "location": "🕸️", "coins": "🍄", "level": "🌴", "kills_today": "🥀",
            "kills_total": "🥀", "deaths": "🧟", "artifacts": "🧪"
        },
        "призрачный лес": {
            "prestige": "👻", "streak": "🕯️", "health": "🩶", "weapon": "🏹",
            "location": "🐦‍⬛", "coins": "✨", "level": "🦇", "kills_today": "⚰️",
            "kills_total": "⚰️", "deaths": "☠️", "artifacts": "🔮"
        },
        "рад-зона": {
            "prestige": "☣️", "streak": "🔬", "health": "💛", "weapon": "📡",
            "location": "☢️", "coins": "⚡", "level": "📟", "kills_today": "🦴",
            "kills_total": "🦴", "deaths": "💀", "artifacts": "🧪"
        },
        "грозовая бездна": {
            "prestige": "🌀", "streak": "🌧️", "health": "💙", "weapon": "💥",
            "location": "⛈️", "coins": "💠", "level": "⚡", "kills_today": "🌪️",
            "kills_total": "🌪️", "deaths": "🔱", "artifacts": "🔮"
        },
        "киберпанк": {
            "prestige": "🌧️", "streak": "💾", "health": "💜", "weapon": "🛰️",
            "location": "🌃", "coins": "⚙️", "level": "🤖", "kills_today": "👾",
            "kills_total": "👾", "deaths": "☔", "artifacts": "🦾"
        },
        "инферно": {
            "prestige": "🔥", "streak": "💥", "health": "🧡", "weapon": "☄️",
            "location": "🌋", "coins": "🧨", "level": "🔥", "kills_today": "💨",
            "kills_total": "💨", "deaths": "☠️", "artifacts": "♨️"
        },
        "космическая пустошь": {
            "prestige": "💫", "streak": "⭐", "health": "🖤", "weapon": "🚀",
            "location": "🌌", "coins": "🌑", "level": "🪐", "kills_today": "🛸",
            "kills_total": "🛸", "deaths": "👽", "artifacts": "🔭"
        }
    }
    
    # Выбираем эмодзи в зависимости от скина
    emojis = theme_emojis.get(current_theme.lower(), default_emojis)
    
    # Формируем сообщение
    message_lines = []
    
    # Строка с ником и статусом
    status_display = f" {current_status}" if current_status else ""
    message_lines.append(f"{username}{status_display}")
    
    # Титул
    if current_title:
        message_lines.append(current_title)
    
    # Звание и престиж
    message_lines.append(f"{rank['name']}")
    message_lines.append(f"{emojis['prestige']} Престиж: {prestige_level}")

    # Серия
    daily_streak = user[38] if len(user) > 38 else 0
    streak_emoji = get_streak_emoji(daily_streak)
    message_lines.append(f"{emojis['streak']} Серия — {daily_streak} {streak_emoji}")

    message_lines.append("")
    
    # Цитата
    if current_quote:
        message_lines.append(current_quote)
        message_lines.append("")
    
    # Здоровье, оружие, локация
    message_lines.append(f"{emojis['health']} Здоровье: {current_hp}/{max_hp}")
    message_lines.append(f"{emojis['weapon']} Оружие: {user[3]}")
    message_lines.append(f"{emojis['location']} Локация: {user[4]}")
    message_lines.append(f"{emojis['coins']} Монеты: {user[1]}")
    message_lines.append(f"{emojis['level']} Уровень: {get_level(user[2])}")
    message_lines.append(f"{emojis['kills_today']} Убийств сегодня: {user[6]}")
    message_lines.append(f"{emojis['kills_total']} Всего убийств: {user[7]}")
    message_lines.append(f"{emojis['deaths']} Смертей: {user[15] if len(user) > 15 else 0}")
    message_lines.append("")
    
    # Артефакты (снаряжение)
    if equipment:
        message_lines.append(f"{emojis['artifacts']} Артефакты: {', '.join(equipment)}")
    else:
        message_lines.append(f"{emojis['artifacts']} Артефакты: нет")
    message_lines.append("")
    
    # Бонусы
    bonuses = []
    groups = ["Мелочь", "Средн", "Опасн", "Тяжел", "Титан"]
    for group in groups:
        bonus = equipment_bonuses.get(group, 0)
        if bonus > 0:
            bonuses.append(f"+{bonus}% к поиску {group.lower()}")
    
    if rank["bonus_exp"] > 0:
        bonuses.append(f"+{rank['bonus_exp']}% к опыту")
    if rank["bonus_coins"] > 0:
        bonuses.append(f"+{rank['bonus_coins']}% к монетам")
    
    if bonuses:
        message_lines.append(f"📊 Бонусы: {', '.join(bonuses)}")
    
    text = "\n".join(message_lines)
    await msg.answer(text)

# ================== ДОСТИЖЕНИЯ ==================
@dp.message(lambda msg: msg.text and msg.text.lower() == "достижения")
async def achievements_command(msg: Message):
    user = ensure_user(msg.from_user.id, msg.from_user.username)
    completed = get_completed_achievements(msg.from_user.id)
    
    check_achievements(msg.from_user.id)
    completed = get_completed_achievements(msg.from_user.id)
    
    text = "🏆 Ваши достижения:\n\n"
    
    for achievement_name, achievement_data in ACHIEVEMENTS.items():
        status = "✅" if achievement_name in completed else "❌"
        
        progress = ""
        if achievement_name not in completed:
            if achievement_data["condition_type"] == "animal_kills":
                animal_name, required_count = achievement_data["condition_value"]
                result = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", 
                                   (msg.from_user.id, animal_name)).fetchone()
                current = result[0] if result else 0
                progress = f" [{current}/{required_count}]"
                
            elif achievement_data["condition_type"] == "titan_kills":
                titan_animals = []
                for loc in LOCATIONS.values():
                    titan_animals.extend(loc["animals"].get("Титан", []))
                titan_kills = 0
                for animal in titan_animals:
                    result = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", 
                                       (msg.from_user.id, animal)).fetchone()
                    if result:
                        titan_kills += result[0]
                progress = f" [{titan_kills}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "coins":
                progress = f" [{user[1]}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "location_kills":
                location_name, required_count = achievement_data["condition_value"]
                location_kills = 0
                for animal_data, count in sql.execute("SELECT animal, count FROM trophies WHERE user_id = ?", (msg.from_user.id,)).fetchall():
                    animal = animal_data
                    for loc_name, loc_data in LOCATIONS.items():
                        if loc_name == location_name:
                            for group_animals in loc_data["animals"].values():
                                if animal in group_animals:
                                    location_kills += count
                                    break
                progress = f" [{location_kills}/{required_count}]"
                
            elif achievement_data["condition_type"] == "unique_animals":
                unique_result = sql.execute("SELECT COUNT(DISTINCT animal) FROM trophies WHERE user_id = ?", 
                                          (msg.from_user.id,)).fetchone()
                unique_count = unique_result[0] if unique_result else 0
                progress = f" [{unique_count}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "streak":
                progress = f" [{user[11] if len(user) > 11 else 0}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "max_health":
                current_hp, max_hp = get_user_health(msg.from_user.id)
                progress = f" [{max_hp}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "counterattack_streak":
                progress = f" [{user[16] if len(user) > 16 else 0}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "titan_escape_streak":
                progress = f" [{user[17] if len(user) > 17 else 0}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "deaths":
                progress = f" [{user[15] if len(user) > 15 else 0}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "trap_heavy":
                progress = f" [{user[21] if len(user) > 21 else 0}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "trap_days_streak":
                progress = f" [{user[18] if len(user) > 18 else 0}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "hunt_count":
                progress = f" [{user[32] if len(user) > 32 else 0}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "level":
                level = get_level(user[2])
                progress = f" [{level}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "all_weapons":
                weapons_result = sql.execute("SELECT COUNT(DISTINCT weapon) FROM user_weapons WHERE user_id = ?", 
                                          (msg.from_user.id,)).fetchone()
                weapons_count = weapons_result[0] if weapons_result else 0
                progress = f" [{weapons_count}/{achievement_data['condition_value']}]"
                
            elif achievement_data["condition_type"] == "all_locations":
                locations_visited = set()
                for animal_data in sql.execute("SELECT animal FROM trophies WHERE user_id = ?", (msg.from_user.id,)).fetchall():
                    animal = animal_data[0]
                    for loc_name, loc_data in LOCATIONS.items():
                        for group_animals in loc_data["animals"].values():
                            if animal in group_animals:
                                locations_visited.add(loc_name)
                                break
                progress = f" [{len(locations_visited)}/{achievement_data['condition_value']}]"
        
        text += f"{status} {achievement_name}{progress}\n"
        text += f"   Условие: {achievement_data['description']}\n"
        text += f"   Награда: {achievement_data['reward_coins']}💰"
        if achievement_data['reward_exp'] > 0:
            text += f", {achievement_data['reward_exp']}⭐"
        if achievement_data['title']:
            text += f"\n   Титул: {achievement_data['title']}"
        text += "\n\n"
    
    text += f"📊 Выполнено: {len(completed)}/{len(ACHIEVEMENTS)}"
    
    await msg.answer(text)


# ================== ДОСТИЖЕНИЯ ЛОКАЦИЙ ==================
LOCATION_ACHIEVEMENTS_DATA = {
    "Тайга": {
        "all_species": {"status": "Охраняет лес 🌳 ", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "🌳 Хранитель тайги", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Каждый куст знает моё имя, каждая тропа помнит мой шаг, а лес шепчет свои секреты.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Саванна": {
        "all_species": {"status": "Догоняет льва 🦁 ", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "🦁 Король саванны", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Здесь каждый день — битва. Зной, ветер, хищники. Но это моя земля.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Арктика": {
        "all_species": {"status": "Купается в снегу ❄️ ", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "❄️ Отмороженный", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Холодно? Ха. Это просто воздух такой освежающий.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Джунгли": {
        "all_species": {"status": "Лазает по лианам 🌿 ", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "🐍 Джунглевый змей", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Листва, пот, тишина. И никого вокруг. Красота.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Горы": {
        "all_species": {"status": "Покоряет горы ⏳ ", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "🦅 Горный орёл", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Воздух разреженный, но лёгкие радуются. А вид — сказка.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Древний мир": {
        "all_species": {"status": "Переносится во времени ⏳ ", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "🦖 Ти-рекс", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Здесь время течёт иначе. Или не течёт вообще. Кто ж разберёт.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Подводный мир": {
        "all_species": {"status": "Ищет акул 🦈 ", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "🌊 Повелитель глубин", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Тишина. Только пузыри и далёкий шум воды. Умиротворение.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Болото проклятых": {
        "all_species": {"status": "Пьёт болотный чай 🍵", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "🕸️ Пастырь болотных пауков", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Я не увяз в болоте — болото увязло во мне.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Призрачный лес": {
        "all_species": {"status": "Шепчется с тенями 👻 ", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "🔮 Призрачный жнец", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Тени здесь живые. Они наблюдают, шепчут, но не трогают. Пока что.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Рад-зона": {
        "all_species": {"status": "Мутирует ☣️", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "🧪 Сталкер", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Гейгер трещит, воздух дрожит, мутанты за углом - всегда.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Грозовая бездна": {
        "all_species": {"status": "Пускает молнии ⚡", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "💥 Властелин энергии", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "В бездне между тучами прячется не свет, а обещание удара.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Киберпанк": {
        "all_species": {"status": "Стоит под неоновым дождём ☔", "coins_reward": 1000, "exp_reward": 500},
        "60_kills": {"title": "👾 Неоновый хищник", "coins_reward": 2000, "exp_reward": 1000},
        "250_kills": {"quote": "Неон, дождь, железо. Город никогда не спит. И я тоже, больше никогда не сплю.", "coins_reward": 5000, "exp_reward": 2500}
    },
    "Инферно": {
        "all_species": {"status": "Пьёт лаву 🌋", "coins_reward": 5000, "exp_reward": 1000},
        "60_kills": {"title": "🌋 Владыка демонов", "coins_reward": 5000, "exp_reward": 1000},
        "250_kills": {"quote": "Пепел — моя броня, пламя — мой меч.", "coins_reward": 10000, "exp_reward": 2500}
    },
    "Космическая пустошь": {
        "all_species": {"status": "Дрейфует между галактиками 🌀", "coins_reward": 10000, "exp_reward": 5000},
        "60_kills": {"title": "🚀 Межгалактический странник", "coins_reward": 20000, "exp_reward": 10000},
        "250_kills": {"quote": "В космосе никто не услышит твой крик, здесь только ты и бесконечность", "coins_reward": 25000, "exp_reward": 25000}
    }
}

# ================== КОЛЛЕКЦИОННЫЕ ПРЕДМЕТЫ ==================
LOCATION_COLLECTIBLES = {
    "Тайга": {
        "Мелочь": ["🌲 Сосновая шишка", "🍂 Сухой лист"],
        "Средн": ["🪵 Берёзовая кора", "🌿 Сосновая живица"],
        "Опасн": ["🪨 Охотничий камень", "🌲 Еловая ветвь"],
        "Тяжел": ["🪵 Корень-великан", "💧 Ключевая вода"],
        "Титан": ["💚 Сердце леса", "🌫️ Дыхание лешего"]
    },
    "Саванна": {
        "Мелочь": ["🌾 Засохший колос", "🌵 Кактусовая игла"],
        "Средн": ["🧂 Солёный камень", "🌿 Сухая трава"],
        "Опасн": ["🔥 Обожжённая земля", "🪨 Знойный камень"],
        "Тяжел": ["🪨 Красный песок", "🌪️ Пыльная спираль"],
        "Титан": ["☀️ Осколок солнца", "🔥 Пылающий песок"]
    },
    "Арктика": {
        "Мелочь": ["❄️ Маленький снежок", "🐚 Осколок ракушки"],
        "Средн": ["🧊 Ледяная крошка", "🌫️ Холодный пар"],
        "Опасн": ["❄️ Вечная льдинка", "🌬️ Ледяной шип"],
        "Тяжел": ["🧊 Айсберг (осколок)", "❄️ Снежная крупа"],
        "Титан": ["✨ Северное сияние", "🧊 Сердце вечной мерзлоты"]
    },
    "Джунгли": {
        "Мелочь": ["🍃 Опавший лист", "🌱 Росток"],
        "Средн": ["🌿 Лиана", "🍂 Гнилой лист"],
        "Опасн": ["💧 Ядовитая роса", "🧪 Гнилой сок"],
        "Тяжел": ["🌴 Пальмовое волокно", "🪵 Гниющая древесина"],
        "Титан": ["🌺 Цветок-людоед", "🧪 Слеза джунглей"]
    },
    "Горы": {
        "Мелочь": ["🪨 Гладкий камешек", "🌬️ Горный воздух"],
        "Средн": ["💧 Родниковая вода", "🪨 Острый обломок"],
        "Опасн": ["🧊 Ледниковая крошка", "🌫️ Облачный туман"],
        "Тяжел": ["🪨 Осколок скалы", "💎 Горный хрусталь"],
        "Титан": ["🌬️ Дуновение ветра", "🪨 Каменный глаз"]
    },
    "Древний мир": {
        "Мелочь": ["🦴 Мелкая косточка", "🧪 Доисторическая смола"],
        "Средн": ["🥚 Окаменевшее яйцо", "🪨 Янтарь с пузырьком"],
        "Опасн": ["🌿 Древний папоротник", "💎 Окаменевшая слеза"],
        "Тяжел": ["🦴 Позвонок гиганта", "🪨 След гиганта"],
        "Титан": ["🧬 Древний ген", "🥚 Яйцо времени"]
    },
    "Подводный мир": {
        "Мелочь": ["🐚 Красивая ракушка", "🪸 Коралл"],
        "Средн": ["🧂 Морская соль", "💧 Солёная капля"],
        "Опасн": ["🧪 Глубинная слизь", "💎 Жемчуг"],
        "Тяжел": ["🌊 Волна в бутылке", "🪨 Рифовый камень"],
        "Титан": ["🌊 Глаз бездны", "🐙 Чернила глубин"]
    },
    "Болото проклятых": {
        "Мелочь": ["🧪 Болотная жижа", "🍄 Гнилой гриб"],
        "Средн": ["🧵 Болотная тина", "🪵 Коряга"],
        "Опасн": ["🧪 Ядовитая слизь", "💨 Болотный газ"],
        "Тяжел": ["🪨 Камень-трясина", "🧪 Чёрная жижа"],
        "Титан": ["👁️ Око болота", "🧪 Живая грязь"]
    },
    "Призрачный лес": {
        "Мелочь": ["🕯️ Огарок свечи", "🪦 Могильная земля"],
        "Средн": ["🧵 Призрачная нить", "🌫️ Туман в банке"],
        "Опасн": ["👁️ Стеклянный глаз", "🕯️ Свеча без пламени"],
        "Тяжел": ["🗡️ Ржавый меч", "🛡️ Разбитый щит"],
        "Титан": ["💀 Крик банши", "🕯️ Свеча с того света"]
    },
    "Рад-зона": {
        "Мелочь": ["🟢 Светящийся мох", "🧪 Радиоактивная капля"],
        "Средн": ["📟 Сломанный дозиметр", "🧪 Облучённый песок"],
        "Опасн": ["🧪 Радиационная слизь", "🟢 Светящийся камень"],
        "Тяжел": ["🧪 Тяжёлая вода", "🪨 Обломок реактора"],
        "Титан": ["💚 Сердце зоны", "☣️ Чистое облучение"]
    },
    "Грозовая бездна": {
        "Мелочь": ["⚡ Статическая искра", "🧲 Магнитный камень"],
        "Средн": ["🔋 Энергетическая сфера", "🌩️ Сгусток молнии"],
        "Опасн": ["⚡ Разрядная катушка", "🧪 Плазменная жидкость"],
        "Тяжел": ["🌪️ Сердце бури", "🔌 Грозовой кристалл"],
        "Титан": ["⚡ Застывший разряд", "🌩️ Гром в банке"]
    },
    "Киберпанк": {
        "Мелочь": ["🔩 Маленький винтик", "💾 Сломанный чип"],
        "Средн": ["🔋 Изношенный аккумулятор", "🔌 Сгоревший провод"],
        "Опасн": ["💿 Плата с чипами", "⚙️ Шестерёнка"],
        "Тяжел": ["🧠 Процессор", "🧪 Жидкий металл"],
        "Титан": ["🖥️ Искусственный интеллект", "⚙️ Идеальный винтик"]
    },
    "Инферно": {
        "Мелочь": ["🔥 Уголёк", "🧂 Адская соль"],
        "Средн": ["🔥 Огненная искра", "🧪 Серный пепел"],
        "Опасн": ["🔥 Пламенный кристалл", "🧪 Расплавленная лава"],
        "Тяжел": ["🪨 Осколок лавового камня", "🔥 Ядро костра"],
        "Титан": ["🔥 Пепел демона", "🧂 Серный камень"]
    },
    "Космическая пустошь": {
        "Мелочь": ["⭐ Падающая звезда", "🌑 Чёрная пыль"],
        "Средн": ["🧪 Тёмная материя", "💫 Осколок кометы"],
        "Опасн": ["🌌 Нейтронная крошка", "🧪 Звёздная пыль"],
        "Тяжел": ["⚫ Гравитационная аномалия", "🔭 Звёздный глаз"],
        "Титан": ["⭐ Черная дыра", "💥 Сверхновая"]
    }
}

# ================== ОФОРМЛЕНИЕ ==================
# Словари для хранения соответствия ID -> значение
TITLES_DICT = {}
STATUSES_DICT = {}
QUOTES_DICT = {}

def load_custom_items():
    """Загружает все доступные титулы, статусы и цитаты в словари"""
    global TITLES_DICT, STATUSES_DICT, QUOTES_DICT
    
    TITLES_DICT = {}
    STATUSES_DICT = {}
    QUOTES_DICT = {}
    
    # Титулы из ACHIEVEMENTS
    tid = 1
    for ach_name, ach_data in ACHIEVEMENTS.items():
        if ach_data.get('title'):
            TITLES_DICT[tid] = ach_data['title']
            tid += 1
    
    # Титулы из локаций
    for loc, data in LOCATION_ACHIEVEMENTS_DATA.items():
        for ach_type, ach_data in data.items():
            if ach_data.get('title'):
                TITLES_DICT[tid] = ach_data['title']
                tid += 1
    
    # Статусы из локаций
    sid = 1
    for loc, data in LOCATION_ACHIEVEMENTS_DATA.items():
        for ach_type, ach_data in data.items():
            if ach_data.get('status'):
                STATUSES_DICT[sid] = ach_data['status']
                sid += 1
    # Базовые статусы
    STATUSES_DICT[sid] = "На охоте🏹"
    sid += 1
    STATUSES_DICT[sid] = "Дома🏠"
    sid += 1
    
    # Цитаты из локаций
    qid = 1
    for loc, data in LOCATION_ACHIEVEMENTS_DATA.items():
        for ach_type, ach_data in data.items():
            if ach_data.get('quote'):
                QUOTES_DICT[qid] = ach_data['quote']
                qid += 1
    # Базовая цитата
    QUOTES_DICT[qid] = "Я начинающий охотник, и я иду к своей цели"


@dp.message(lambda msg: msg.text and msg.text.lower() == "оформление")
async def customization(msg: Message):
    """Меню оформления: титулы, статусы, цитаты, скины"""
    user_id = msg.from_user.id
    load_custom_items()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👑 Титулы", callback_data=f"cust_titles:{user_id}")],
        [InlineKeyboardButton(text="🏷️ Статусы", callback_data=f"cust_statuses:{user_id}")],
        [InlineKeyboardButton(text="💬 Цитаты", callback_data=f"cust_quotes:{user_id}")],
        [InlineKeyboardButton(text="🎨 Скины профиля", callback_data=f"cust_themes:{user_id}")]  # НОВАЯ КНОПКА
    ])
    await msg.answer("🎨 **Оформление профиля**\n\nВыберите категорию:", reply_markup=kb, parse_mode="Markdown")


@dp.callback_query(lambda c: c.data.startswith("cust_titles"))
async def cust_titles(call: CallbackQuery):
    user_id = int(call.data.split(":")[1])
    if user_id != call.from_user.id:
        await call.answer("❌ Это не ваше меню!", show_alert=True)
        return
    
    user = ensure_user(call.from_user.id)
    current_title = user[9] if len(user) > 9 and user[9] else ""
    
    # Получаем ID титулов, которые есть у игрока
    completed = get_completed_achievements(call.from_user.id)
    available_ids = []
    
    # Титулы из достижений
    for ach_name, ach_data in ACHIEVEMENTS.items():
        if ach_name in completed and ach_data.get('title'):
            for tid, title in TITLES_DICT.items():
                if title == ach_data['title']:
                    available_ids.append(tid)
                    break
    
    # Титулы из локаций
    loc_ach = sql.execute("SELECT location, achievement_type FROM location_achievements WHERE user_id = ? AND completed = 1",
                          (call.from_user.id,)).fetchall()
    for loc, ach_type in loc_ach:
        ach_data = LOCATION_ACHIEVEMENTS_DATA.get(loc, {}).get(ach_type, {})
        if ach_data.get('title'):
            for tid, title in TITLES_DICT.items():
                if title == ach_data['title']:
                    available_ids.append(tid)
                    break
    
    available_ids = list(set(available_ids))
    
    if not available_ids:
        await call.message.edit_text("👑 У вас пока нет титулов. Выполняйте достижения!")
        return
    
    await show_custom_page(call, available_ids, TITLES_DICT, current_title, "title", 0)


@dp.callback_query(lambda c: c.data.startswith("cust_statuses"))
async def cust_statuses(call: CallbackQuery):
    user_id = int(call.data.split(":")[1])
    if user_id != call.from_user.id:
        await call.answer("❌ Это не ваше меню!", show_alert=True)
        return
    
    user = ensure_user(call.from_user.id)
    current_status = user[36] if len(user) > 36 and user[36] else ""
    
    # Получаем ID статусов, которые есть у игрока
    available_ids = []
    
    loc_ach = sql.execute("SELECT location, achievement_type FROM location_achievements WHERE user_id = ? AND completed = 1",
                          (call.from_user.id,)).fetchall()
    for loc, ach_type in loc_ach:
        ach_data = LOCATION_ACHIEVEMENTS_DATA.get(loc, {}).get(ach_type, {})
        if ach_data.get('status'):
            for sid, status in STATUSES_DICT.items():
                if status == ach_data['status']:
                    available_ids.append(sid)
                    break
    
    # Базовые статусы всегда доступны
    for sid, status in STATUSES_DICT.items():
        if status in ["На охоте🏹", "Дома🏠"]:
            available_ids.append(sid)
    
    available_ids = list(set(available_ids))
    
    await show_custom_page(call, available_ids, STATUSES_DICT, current_status, "status", 0)


@dp.callback_query(lambda c: c.data.startswith("cust_quotes"))
async def cust_quotes(call: CallbackQuery):
    user_id = int(call.data.split(":")[1])
    if user_id != call.from_user.id:
        await call.answer("❌ Это не ваше меню!", show_alert=True)
        return
    
    user = ensure_user(call.from_user.id)
    current_quote = user[37] if len(user) > 37 and user[37] else ""
    
    # Получаем ID цитат, которые есть у игрока
    available_ids = []
    
    loc_ach = sql.execute("SELECT location, achievement_type FROM location_achievements WHERE user_id = ? AND completed = 1",
                          (call.from_user.id,)).fetchall()
    for loc, ach_type in loc_ach:
        ach_data = LOCATION_ACHIEVEMENTS_DATA.get(loc, {}).get(ach_type, {})
        if ach_data.get('quote'):
            for qid, quote in QUOTES_DICT.items():
                if quote == ach_data['quote']:
                    available_ids.append(qid)
                    break
    
    # Базовая цитата всегда доступна
    for qid, quote in QUOTES_DICT.items():
        if quote == "Я начинающий охотник, и я иду к своей цели":
            available_ids.append(qid)
            break
    
    available_ids = list(set(available_ids))
    
    await show_custom_page(call, available_ids, QUOTES_DICT, current_quote, "quote", 0)


async def show_custom_page(call: CallbackQuery, available_ids: list, items_dict: dict, current: str, item_type: str, page: int):
    per_page = 3
    total_pages = (len(available_ids) + per_page - 1) // per_page if available_ids else 1
    start = page * per_page
    end = start + per_page
    page_ids = available_ids[start:end]
    
    type_names = {"title": "👑 Титулы", "status": "🏷️ Статусы", "quote": "💬 Цитаты"}
    title = type_names.get(item_type, "Оформление")
    
    text = f"{title}\n\n"
    text += f"Текущий: {current if current else '❌ Не выбран'}\n\n"
    
    buttons = []
    for item_id in page_ids:
        item_text = items_dict[item_id]
        display_text = item_text[:35] + "..." if len(item_text) > 35 else item_text
        
        if item_text == current:
            buttons.append([InlineKeyboardButton(text=f"✅ {display_text}", callback_data="no_action")])
        else:
            buttons.append([InlineKeyboardButton(
                text=f"👑 {display_text}",
                callback_data=f"cust_set:{call.from_user.id}:{item_type}:{item_id}:{page}"
            )])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"cust_page:{call.from_user.id}:{item_type}:{page-1}"))
    if current:
        nav_buttons.append(InlineKeyboardButton(text="❌ Снять", callback_data=f"cust_remove:{call.from_user.id}:{item_type}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперед ▶️", callback_data=f"cust_page:{call.from_user.id}:{item_type}:{page+1}"))
    
    if nav_buttons:
        buttons.append(nav_buttons)
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"cust_back:{call.from_user.id}")])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    try:
        await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        if "message is not modified" not in str(e):
            raise
@dp.callback_query(lambda c: c.data.startswith("cust_themes"))
async def cust_themes(call: CallbackQuery):
    """Меню выбора скина профиля"""
    user_id = int(call.data.split(":")[1])
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не ваше меню!", show_alert=True)
        return
    
    # Получаем разблокированные скины
    conn = sqlite3.connect("hunt.db")
    cur = conn.cursor()
    unlocked = cur.execute(
        "SELECT theme_name FROM user_themes WHERE user_id = ? AND unlocked = 1",
        (user_id,)
    ).fetchall()
    conn.close()
    
    unlocked_themes = [row[0] for row in unlocked]
    
    # Всегда есть стандартный скин
    available_themes = ["standard"] + unlocked_themes
    
    # Получаем текущий выбранный скин
    theme_result = sql.execute("SELECT profile_theme FROM users WHERE user_id = ?", (user_id,)).fetchone()
    current_theme = theme_result[0] if theme_result and theme_result[0] else "standard"
    if isinstance(current_theme, int):
        current_theme = "standard"
    current_theme = str(current_theme).lower()
    
    # Словарь для отображения названий
    theme_names = {
        "standard": "🏠 Стандартный",
        "тайга": "🌲 Тайга",
        "саванна": "☀️ Саванна",
        "арктика": "❄️ Арктика",
        "джунгли": "🌿 Джунгли",
        "горы": "⛰️ Горы",
        "древний мир": "🦖 Древний мир",
        "подводный мир": "🌊 Подводный мир",
        "болото проклятых": "🧪 Болото проклятых",
        "призрачный лес": "👻 Призрачный лес",
        "рад-зона": "☢️ Рад-зона",
        "грозовая бездна": "⚡ Грозовая бездна",
        "киберпанк": "🤖 Киберпанк",
        "инферно": "🔥 Инферно",
        "космическая пустошь": "🪐 Космическая пустошь"
    }
    
    buttons = []
    for theme in available_themes:
        display_name = theme_names.get(theme.lower(), theme)
        if theme == current_theme:
            buttons.append([InlineKeyboardButton(text=f"✅ {display_name}", callback_data="no_action")])
        else:
            buttons.append([InlineKeyboardButton(
                text=f"{display_name}",
                callback_data=f"theme_select:{user_id}:{theme}"
            )])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"cust_back:{user_id}")])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await call.message.edit_text("🎨 **Выберите скин профиля:**\n\nСкины разблокируются за сбор всех 10 предметов в локации.", reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        if "message is not modified" not in str(e):
            raise

@dp.callback_query(lambda c: c.data.startswith("theme_select"))
async def theme_select(call: CallbackQuery):
    """Выбор скина профиля"""
    parts = call.data.split(":")
    if len(parts) < 3:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    user_id = int(parts[1])
    theme = parts[2]
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не ваш выбор!", show_alert=True)
        return
    
    # Проверяем, разблокирован ли скин
    if theme != "standard":
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        unlocked = cur.execute(
            "SELECT 1 FROM user_themes WHERE user_id = ? AND theme_name = ? AND unlocked = 1",
            (user_id, theme)
        ).fetchone()
        conn.close()
        
        if not unlocked:
            await call.answer("❌ Этот скин ещё не разблокирован!", show_alert=True)
            return
    
    # Сохраняем выбранный скин
    sql.execute("UPDATE users SET profile_theme = ? WHERE user_id = ?", (theme.lower(), user_id))
    db.commit()
    
    await call.answer(f"✅ Скин профиля изменён на {theme}!", show_alert=True)
    
    # Обновляем меню скинов (чтобы галочка переместилась)
    await cust_themes(call)


@dp.callback_query(lambda c: c.data.startswith("cust_page"))
async def cust_page(call: CallbackQuery):
    parts = call.data.split(":")
    if len(parts) < 4:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    user_id = int(parts[1])
    item_type = parts[2]
    page = int(parts[3])
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не ваше меню!", show_alert=True)
        return
    
    # Восстанавливаем список ID
    completed = get_completed_achievements(call.from_user.id)
    available_ids = []
    
    if item_type == "title":
        # Титулы из достижений
        for ach_name, ach_data in ACHIEVEMENTS.items():
            if ach_name in completed and ach_data.get('title'):
                for tid, title in TITLES_DICT.items():
                    if title == ach_data['title']:
                        available_ids.append(tid)
                        break
        # Титулы из локаций
        loc_ach = sql.execute("SELECT location, achievement_type FROM location_achievements WHERE user_id = ? AND completed = 1",
                              (call.from_user.id,)).fetchall()
        for loc, ach_type in loc_ach:
            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(loc, {}).get(ach_type, {})
            if ach_data.get('title'):
                for tid, title in TITLES_DICT.items():
                    if title == ach_data['title']:
                        available_ids.append(tid)
                        break
        available_ids = list(set(available_ids))
        current = sql.execute("SELECT current_title FROM users WHERE user_id = ?", (call.from_user.id,)).fetchone()[0] or ""
        items_dict = TITLES_DICT
        
    elif item_type == "status":
        loc_ach = sql.execute("SELECT location, achievement_type FROM location_achievements WHERE user_id = ? AND completed = 1",
                              (call.from_user.id,)).fetchall()
        for loc, ach_type in loc_ach:
            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(loc, {}).get(ach_type, {})
            if ach_data.get('status'):
                for sid, status in STATUSES_DICT.items():
                    if status == ach_data['status']:
                        available_ids.append(sid)
                        break
        for sid, status in STATUSES_DICT.items():
            if status in ["На охоте🏹", "Дома🏠"]:
                available_ids.append(sid)
        available_ids = list(set(available_ids))
        current = sql.execute("SELECT current_status FROM users WHERE user_id = ?", (call.from_user.id,)).fetchone()[0] or ""
        items_dict = STATUSES_DICT
        
    else:  # quote
        loc_ach = sql.execute("SELECT location, achievement_type FROM location_achievements WHERE user_id = ? AND completed = 1",
                              (call.from_user.id,)).fetchall()
        for loc, ach_type in loc_ach:
            ach_data = LOCATION_ACHIEVEMENTS_DATA.get(loc, {}).get(ach_type, {})
            if ach_data.get('quote'):
                for qid, quote in QUOTES_DICT.items():
                    if quote == ach_data['quote']:
                        available_ids.append(qid)
                        break
        for qid, quote in QUOTES_DICT.items():
            if quote == "Я начинающий охотник, и я иду к своей цели":
                available_ids.append(qid)
                break
        available_ids = list(set(available_ids))
        current = sql.execute("SELECT current_quote FROM users WHERE user_id = ?", (call.from_user.id,)).fetchone()[0] or ""
        items_dict = QUOTES_DICT
    
    await show_custom_page(call, available_ids, items_dict, current, item_type, page)


@dp.callback_query(lambda c: c.data.startswith("cust_set"))
async def cust_set(call: CallbackQuery):
    parts = call.data.split(":")
    if len(parts) < 5:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    user_id = int(parts[1])
    item_type = parts[2]
    item_id = int(parts[3])
    page = int(parts[4])
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не ваш выбор!", show_alert=True)
        return
    
    if item_type == "title":
        value = TITLES_DICT.get(item_id, "")
        if value:
            sql.execute("UPDATE users SET current_title = ? WHERE user_id = ?", (value, call.from_user.id))
            await call.answer(f"✅ Титул изменён!", show_alert=True)
    elif item_type == "status":
        value = STATUSES_DICT.get(item_id, "")
        if value:
            sql.execute("UPDATE users SET current_status = ? WHERE user_id = ?", (value, call.from_user.id))
            await call.answer(f"✅ Статус изменён!", show_alert=True)
    elif item_type == "quote":
        value = QUOTES_DICT.get(item_id, "")
        if value:
            sql.execute("UPDATE users SET current_quote = ? WHERE user_id = ?", (value, call.from_user.id))
            await call.answer(f"✅ Цитата установлена!", show_alert=True)
    
    db.commit()
    await cust_page(call)


@dp.callback_query(lambda c: c.data.startswith("cust_remove"))
async def cust_remove(call: CallbackQuery):
    parts = call.data.split(":")
    if len(parts) < 3:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    user_id = int(parts[1])
    item_type = parts[2]
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не ваш выбор!", show_alert=True)
        return
    
    if item_type == "title":
        sql.execute("UPDATE users SET current_title = '' WHERE user_id = ?", (call.from_user.id,))
        await call.answer("✅ Титул снят", show_alert=True)
    elif item_type == "status":
        sql.execute("UPDATE users SET current_status = '' WHERE user_id = ?", (call.from_user.id,))
        await call.answer("✅ Статус снят", show_alert=True)
    elif item_type == "quote":
        sql.execute("UPDATE users SET current_quote = '' WHERE user_id = ?", (call.from_user.id,))
        await call.answer("✅ Цитата снята", show_alert=True)
    
    db.commit()
    await cust_page(call)


@dp.callback_query(lambda c: c.data.startswith("cust_back"))
async def cust_back(call: CallbackQuery):
    user_id = int(call.data.split(":")[1])
    
    if user_id != call.from_user.id:
        await call.answer("❌ Это не ваше меню!", show_alert=True)
        return
    
    # Возвращаемся в главное меню оформления
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👑 Титулы", callback_data=f"cust_titles:{user_id}")],
        [InlineKeyboardButton(text="🏷️ Статусы", callback_data=f"cust_statuses:{user_id}")],
        [InlineKeyboardButton(text="💬 Цитаты", callback_data=f"cust_quotes:{user_id}")],
        [InlineKeyboardButton(text="🎨 Скины профиля", callback_data=f"cust_themes:{user_id}")]
    ])
    await call.message.edit_text("🎨 **Оформление профиля**\n\nВыберите категорию:", reply_markup=kb, parse_mode="Markdown")

# ================== ПРЕСТИЖ ==================
@dp.message(lambda msg: msg.text and msg.text.lower() == "престиж")
async def prestige_command(msg: Message):
    user = ensure_user(msg.from_user.id, msg.from_user.username)
    prestige_level = user[10] if len(user) > 10 else 0
    
    if prestige_level >= 10:
        await msg.answer("🎖️ Вы достигли максимального престижа (10)!")
        return
    
    next_prestige = prestige_level + 1
    prestige_data = PRESTIGES.get(next_prestige, {})
    
    if not prestige_data:
        await msg.answer("❌ Ошибка: следующий престиж не найден")
        return
    
    requirements = prestige_data.get("requirements", {})
    
    text = f"🎖️ Престиж {next_prestige}: {prestige_data['name']}\n\n"
    text += "📋 Требования:\n"
    text += f"• Уровень: {requirements.get('level', 0)}+\n"
    text += f"• Убийств: {requirements.get('kills', 0)}+\n"
    text += f"• Монет: {requirements.get('coins', 0)}+\n"
    
    if "unique_animals" in requirements:
        text += f"• Уникальных животных: {requirements['unique_animals']}+\n"
    if "titans" in requirements:
        text += f"• Титанов: {requirements['titans']}+\n"
    if "dangerous" in requirements:
        text += f"• Опасных животных: {requirements['dangerous']}+\n"
    if "arctic" in requirements:
        text += f"• Арктических животных: {requirements['arctic']}+\n"
    if "all_locations" in requirements:
        text += f"• Животные из всех локаций: Да\n"
    if "all_weapons" in requirements:
        text += f"• Все виды оружия: Да\n"
    if "all_titans" in requirements:
        text += f"• По 5 каждого титана: Да\n"
    
    text += f"\n🏆 Ваш текущий престиж: {prestige_level}"
    
    can_prestige, message = check_prestige_requirements(msg.from_user.id, next_prestige)
    
    if can_prestige:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎖️ Получить престиж", callback_data=f"get_prestige:{msg.from_user.id}:{next_prestige}")],
            [InlineKeyboardButton(text="🏆 Топ по престижу", callback_data=f"top_prestige:{msg.from_user.id}")]
        ])
        text += f"\n\n✅ {message}"
        await msg.answer(text, reply_markup=kb)
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏆 Топ по престижу", callback_data=f"top_prestige:{msg.from_user.id}")]
        ])
        text += f"\n\n❌ {message}"
        await msg.answer(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("get_prestige"))
async def get_prestige_callback(call: CallbackQuery):
    data_parts = call.data.split(":")
    if len(data_parts) < 3:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    user_id, prestige_level = data_parts[1:]
    prestige_level = int(prestige_level)
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваш престиж!", show_alert=True)
        return
    
    can_prestige, message = check_prestige_requirements(call.from_user.id, prestige_level)
    
    if not can_prestige:
        await call.answer(f"❌ {message}", show_alert=True)
        return
    
    # Выдаем награды за престиж
    if prestige_level in PRESTIGE_REWARDS:
        reward_data = PRESTIGE_REWARDS[prestige_level]
        
        # Выдаем монеты и опыт
        coins = reward_data["reward_coins"]
        exp = reward_data["reward_exp"]
        
        sql.execute("UPDATE users SET coins = coins + ?, exp = exp + ?, prestige = ? WHERE user_id = ?", 
                   (coins, exp, prestige_level, call.from_user.id))
        
        # Добавляем титул, если его еще нет
        current_title = sql.execute("SELECT current_title FROM users WHERE user_id = ?", (call.from_user.id,)).fetchone()[0]
        if not current_title and "title" in reward_data:
            sql.execute("UPDATE users SET current_title = ? WHERE user_id = ?", (reward_data["title"], call.from_user.id))
        
        db.commit()
        
        reward_text = f"🎉 Поздравляем! Вы получили престиж {prestige_level}: {reward_data['name']}\n\n"
        reward_text += f"🎁 Награды:\n"
        reward_text += f"• Монеты: +{coins}💰\n"
        reward_text += f"• Опыт: +{exp}⭐\n"
        
        if "title" in reward_data:
            reward_text += f"• Титул: {reward_data['title']}\n"
        
        if "bonus" in reward_data:
            bonus_text = ""
            for bonus_type, bonus_value in reward_data["bonus"].items():
                if bonus_type == "exp_bonus":
                    bonus_text += f"• +{bonus_value}% к опыту\n"
                elif bonus_type == "coins_bonus":
                    bonus_text += f"• +{bonus_value}% к монетам\n"
                elif bonus_type == "collectible_chance":
                    bonus_text += f"• +{bonus_value}% к шансу коллекционных предметов\n"
                elif bonus_type == "titan_hit":
                    bonus_text += f"• +{bonus_value}% к шансу попадания по титанам\n"
                elif bonus_type == "discount":
                    bonus_text += f"• Скидка {bonus_value}% на покупки\n"
                elif bonus_type == "healing_bonus":
                    bonus_text += f"• +{bonus_value}% к скорости восстановления HP\n"
                elif bonus_type == "all_bonus":
                    bonus_text += f"• Все бонусы усилены на {bonus_value}%\n"
            
            if bonus_text:
                reward_text += f"\n📈 Перманентные бонусы:\n{bonus_text}"
        
        if "special" in reward_data:
            special = reward_data["special"]
            if special == "golden_bullet:5":
                sql.execute("UPDATE users SET golden_bullet = golden_bullet + 5 WHERE user_id = ?", (call.from_user.id,))
                reward_text += f"\n💫 Специальная награда: 5 золотых пуль!\n"
        
        await call.message.edit_text(reward_text)
    else:
        sql.execute("UPDATE users SET prestige = ? WHERE user_id = ?", (prestige_level, call.from_user.id))
        db.commit()
        await call.message.edit_text(f"🎉 Поздравляем! Вы получили престиж {prestige_level}: {PRESTIGES[prestige_level].get('name', '')}")

@dp.callback_query(lambda c: c.data.startswith("top_prestige"))
async def top_prestige_callback(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваш топ!", show_alert=True)
        return
    
    top_users = sql.execute(
        "SELECT username, prestige FROM users WHERE username IS NOT NULL AND prestige > 0 ORDER BY prestige DESC, exp DESC LIMIT 10"
    ).fetchall()
    
    if not top_users:
        await call.message.edit_text("🏆 Пока никто не получил престиж.")
        return
    
    text = "🏆 Топ по престижу:\n\n"
    for i, (username, prestige) in enumerate(top_users, 1):
        prestige_name = PRESTIGES.get(prestige, {}).get("name", f"Престиж {prestige}")
        text += f"{i}. @{username} — {prestige_name}\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"prestige_back:{call.from_user.id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("prestige_back"))
async def prestige_back(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваше меню!", show_alert=True)
        return
    
    user = ensure_user(call.from_user.id)
    prestige_level = user[10] if len(user) > 10 else 0
    
    if prestige_level >= 10:
        await call.message.edit_text("🎖️ Вы достигли максимального престижа (10)!")
        return
    
    next_prestige = prestige_level + 1
    prestige_data = PRESTIGES.get(next_prestige, {})
    
    if not prestige_data:
        await call.message.edit_text("❌ Ошибка: следующий престиж не найден")
        return
    
    requirements = prestige_data.get("requirements", {})
    
    text = f"🎖️ Престиж {next_prestige}: {prestige_data['name']}\n\n"
    text += "📋 Требования:\n"
    text += f"• Уровень: {requirements.get('level', 0)}+\n"
    text += f"• Убийств: {requirements.get('kills', 0)}+\n"
    text += f"• Монет: {requirements.get('coins', 0)}+\n"
    
    if "unique_animals" in requirements:
        text += f"• Уникальных животных: {requirements['unique_animals']}+\n"
    if "titans" in requirements:
        text += f"• Титанов: {requirements['titans']}+\n"
    if "dangerous" in requirements:
        text += f"• Опасных животных: {requirements['dangerous']}+\n"
    if "arctic" in requirements:
        text += f"• Арктических животных: {requirements['arctic']}+\n"
    if "all_locations" in requirements:
        text += f"• Животные из всех локаций: Да\n"
    if "all_weapons" in requirements:
        text += f"• Все виды оружия: Да\n"
    if "all_titans" in requirements:
        text += f"• По 5 каждого титана: Да\n"
    
    text += f"\n🏆 Ваш текущий престиж: {prestige_level}"
    
    can_prestige, message = check_prestige_requirements(call.from_user.id, next_prestige)
    
    if can_prestige:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎖️ Получить престиж", callback_data=f"get_prestige:{call.from_user.id}:{next_prestige}")],
            [InlineKeyboardButton(text="🏆 Топ по престижу", callback_data=f"top_prestige:{call.from_user.id}")]
        ])
        text += f"\n\n✅ {message}"
        await call.message.edit_text(text, reply_markup=kb)
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏆 Топ по престижу", callback_data=f"top_prestige:{call.from_user.id}")]
        ])
        text += f"\n\n❌ {message}"
        await call.message.edit_text(text, reply_markup=kb)



# ================== ИВЕНТАРЬ БАФФОВ ==================
@dp.message(lambda msg: msg.text and msg.text.lower() == "баффы")
async def show_buffs(msg: Message):
    """Показать инвентарь баффов"""
    user_id = msg.from_user.id
    user_buffs = get_user_buffs(user_id)
    
    # Фильтруем только баффы с количеством > 0
    user_buffs = {name: count for name, count in user_buffs.items() if count > 0}
    
    if not user_buffs:
        await msg.answer("📦 У вас нет купленных баффов.\n\nКупить их можно в магазине → ⚡ Баффы")
        return
    
    buttons = []
    for buff_name, count in user_buffs.items():
        if count > 0:
            buttons.append([InlineKeyboardButton(
                text=f"{buff_name} x{count}",
                callback_data=f"activate_buff:{user_id}:{buff_name}"
            )])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await msg.answer("📦 **Ваши баффы:**\n\nНажмите на бафф, чтобы активировать.", reply_markup=kb, parse_mode="Markdown")


@dp.callback_query(lambda c: c.data.startswith("activate_buff"))
async def activate_buff(call: CallbackQuery):
    """Активация баффа из инвентаря"""
    try:
        _, user_id, buff_name = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш бафф!", show_alert=True)
            return
        
        # Проверяем, есть ли бафф у игрока
        user_buffs = get_user_buffs(user_id)
        if buff_name not in user_buffs or user_buffs[buff_name] <= 0:
            await call.answer("❌ У вас нет этого баффа!", show_alert=True)
            return
        
        buff_data = BUFFS.get(buff_name)
        if not buff_data:
            await call.answer("❌ Бафф не найден!", show_alert=True)
            return
        
        # Удаляем бафф из инвентаря (1 штуку)
        remove_user_buff(user_id, buff_name, 1)
        
        if buff_data['effect'] == "medkit":
            # Восстанавливаем 50 HP, но не больше максимума
            user = ensure_user(user_id)
            current_hp = user[13]
            max_hp = user[14]
            new_hp = min(current_hp + 60, max_hp)
            sql.execute("UPDATE users SET health = ? WHERE user_id = ?", (new_hp, user_id))
            db.commit()
            await call.message.edit_text(
                f"✅ **Бафф активирован!**\n\n"
                f"💊 {buff_name}\n"
                f"❤️ Восстановлено 60 HP! Теперь: {new_hp}/{max_hp}",
                parse_mode="Markdown"
            )
        
        elif buff_data['effect'] == "golden_bullet":
            sql.execute("UPDATE users SET golden_bullet = golden_bullet + 1 WHERE user_id = ?", (user_id,))
            db.commit()
            await call.message.edit_text(
                f"✅ **Бафф активирован!**\n\n"
                f"💫 {buff_name}\n"
                f"💫 Золотая пуля добавлена! Следующий выстрел с x2 шансом.",
                parse_mode="Markdown"
            )
        
        elif buff_data['effect'] == "diamond_bullet":
            sql.execute("UPDATE users SET diamond_bullet = diamond_bullet + 1 WHERE user_id = ?", (user_id,))
            db.commit()
            await call.message.edit_text(
                f"✅ **Бафф активирован!**\n\n"
                f"💎 {buff_name}\n"
                f"💎 Алмазная пуля добавлена! +20% к шансу попадания.",
                parse_mode="Markdown"
            )
        
        elif buff_data['effect'] == "immortality_staff":
            sql.execute("UPDATE users SET immortality_staff = immortality_staff + 1 WHERE user_id = ?", (user_id,))
            db.commit()
            await call.message.edit_text(
                f"✅ **Бафф активирован!**\n\n"
                f"🪄 {buff_name}\n"
                f"🪄 Посох бессмертия добавлен! Защита от следующей контратаки.",
                parse_mode="Markdown"
            )
        
        elif buff_data['effect'] == "no_cooldown_charges":
            sql.execute("UPDATE users SET no_cooldown_charges = no_cooldown_charges + ? WHERE user_id = ?", 
                       (buff_data.get('charges', 3), user_id))
            db.commit()
            await call.message.edit_text(
                f"✅ **Бафф активирован!**\n\n"
                f"🔋 {buff_name}\n"
                f"🔋 Следующие {buff_data.get('charges', 3)} ханта без задержки!",
                parse_mode="Markdown"
            )
        
        elif buff_data['effect'] == "drone":
            user_data = ensure_user(user_id)
            location = user_data[4]
            
            found_animals = []
            for _ in range(3):
                rand = random.randint(1, 1000)
                if rand <= 600:
                    group = "Средн"
                elif rand <= 950:
                    group = "Опасн"
                elif rand <= 999:
                    group = "Тяжел"
                else:
                    group = "Титан"
                
                if group in LOCATIONS[location]["animals"] and LOCATIONS[location]["animals"][group]:
                    animal = random.choice(LOCATIONS[location]["animals"][group])
                    found_animals.append(animal)
            
            buttons = []
            for animal in found_animals:
                buttons.append([InlineKeyboardButton(
                    text=f"{animal}",
                    callback_data=f"drone_select:{user_id}:{animal}"
                )])
            
            kb = InlineKeyboardMarkup(inline_keyboard=buttons)
            await call.message.edit_text(
                "🛸 **Дрон запущен!** Найдены животные:\n\n"
                "Выберите одно животное для отслеживания (+10% шанс найти его в течение 30 минут):",
                reply_markup=kb,
                parse_mode="Markdown"
            )
            return
        
        elif buff_data['effect'] == "ultra_drone":
            user_data = ensure_user(user_id)
            location = user_data[4]
            
            found_animals = []  # теперь храним tuple (group, animal)
            for _ in range(4):
                rand = random.randint(1, 100)
                if rand <= 70:
                    group = "Опасн"
                elif rand <= 95:
                    group = "Тяжел"
                else:
                    group = "Титан"
                
                if group in LOCATIONS[location]["animals"] and LOCATIONS[location]["animals"][group]:
                    animal = random.choice(LOCATIONS[location]["animals"][group])
                    found_animals.append((group, animal))  # сохраняем и группу, и животное
            
            buttons = []
            for group, animal in found_animals:
                buttons.append([InlineKeyboardButton(
                    text=f"{animal} ({group})",  # теперь с типом в скобках
                    callback_data=f"ultra_select:{user_id}:{animal}"
                )])

            kb = InlineKeyboardMarkup(inline_keyboard=buttons)
            await call.message.edit_text(
                "🛸 **Ультра-звуковой дрон запущен!** Найдены животные:\n\n"
                "Выберите одно животное для отслеживания (+10% шанс найти его в течение 30 минут):",
                reply_markup=kb,
                parse_mode="Markdown"
            )
            return
        
        await asyncio.sleep(2)
        
        # Обновляем меню баффов
        user_buffs = get_user_buffs(user_id)
        if user_buffs:
            buttons = []
            for bn, cnt in user_buffs.items():
                if cnt > 0:
                    buttons.append([InlineKeyboardButton(
                        text=f"{bn} x{cnt}",
                        callback_data=f"activate_buff:{user_id}:{bn}"
                    )])
            kb = InlineKeyboardMarkup(inline_keyboard=buttons)
            await call.message.edit_text(
                "📦 **Ваши баффы:**\n\nНажмите на бафф, чтобы активировать.",
                reply_markup=kb,
                parse_mode="Markdown"
            )
        else:
            await call.message.edit_text("📦 У вас нет купленных баффов.\n\nКупить их можно в магазине → ⚡ Баффы")
        
    except Exception as e:
        print(f"Ошибка activate_buff: {e}")
        await call.answer("❌ Ошибка при активации", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("drone_select:"))
async def drone_select_handler(call: CallbackQuery):
    """Выбор цели для обычного дрона"""
    try:
        _, user_id, animal = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш выбор!", show_alert=True)
            return
        
        expires_at = int(time.time()) + 1800
        sql.execute("UPDATE users SET drone_target = ?, drone_expires = ? WHERE user_id = ?",
                   (animal, expires_at, call.from_user.id))
        db.commit()
        
        await call.message.edit_text(
            f"✅ **Дрон настроен!**\n\n"
            f"Цель: {animal}\n"
            f"📈 +10% шанс найти это животное в течение 30 минут.",
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(2)
        
        # Показываем инвентарь баффов
        user_buffs = get_user_buffs(user_id)
        if user_buffs:
            buttons = []
            for bn, cnt in user_buffs.items():
                if cnt > 0:
                    buttons.append([InlineKeyboardButton(
                        text=f"{bn} x{cnt}",
                        callback_data=f"activate_buff:{user_id}:{bn}"
                    )])
            kb = InlineKeyboardMarkup(inline_keyboard=buttons)
            await call.message.edit_text(
                "📦 **Ваши баффы:**\n\nНажмите на бафф, чтобы активировать.",
                reply_markup=kb,
                parse_mode="Markdown"
            )
        
    except Exception as e:
        print(f"Ошибка drone_select_handler: {e}")
        await call.answer("❌ Ошибка", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("ultra_select:"))
async def ultra_select_handler(call: CallbackQuery):
    """Выбор цели для ультра-дрона"""
    try:
        _, user_id, animal = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш выбор!", show_alert=True)
            return
        
        expires_at = int(time.time()) + 1800
        sql.execute("UPDATE users SET drone_target = ?, drone_expires = ? WHERE user_id = ?",
                   (animal, expires_at, call.from_user.id))
        db.commit()
        
        await call.message.edit_text(
            f"✅ **Ультра-звуковой дрон настроен!**\n\n"
            f"Цель: {animal}\n"
            f"📈 +10% шанс найти это животное в течение 30 минут.",
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(2)
        
        # Показываем инвентарь баффов
        user_buffs = get_user_buffs(user_id)
        if user_buffs:
            buttons = []
            for bn, cnt in user_buffs.items():
                if cnt > 0:
                    buttons.append([InlineKeyboardButton(
                        text=f"{bn} x{cnt}",
                        callback_data=f"activate_buff:{user_id}:{bn}"
                    )])
            kb = InlineKeyboardMarkup(inline_keyboard=buttons)
            await call.message.edit_text(
                "📦 **Ваши баффы:**\n\nНажмите на бафф, чтобы активировать.",
                reply_markup=kb,
                parse_mode="Markdown"
            )
        
    except Exception as e:
        print(f"Ошибка ultra_select_handler: {e}")
        await call.answer("❌ Ошибка", show_alert=True)
        
# ================== ИВЕНТЫ ==================

@dp.message(lambda msg: msg.text and msg.text.lower() == "ивент")
async def event_command(msg: Message):
    """Главное меню ивента"""
    if not EVENT_ACTIVE:
        await msg.answer("🎄 Сейчас нет активного ивента. Следите за новостями!")
        return
    
    user = ensure_user(msg.from_user.id)
    eggs = user[33] if len(user) > 33 else 0
    current_quest = user[34] if len(user) > 34 else 0
    
    # Формируем список заданий
    quests_lines = []
    for i, quest in enumerate(EVENT_QUESTS):
        need = quest["need"]
        if i < current_quest:
            status = "✅"
        elif i == current_quest:
            status = f"📌 ({eggs}/{need})"
        else:
            status = "🔒"
        
        reward_text = ""
        if quest["reward_coins"] > 0:
            reward_text += f" +{quest['reward_coins']}💰"
        if quest["reward_exp"] > 0:
            reward_text += f" +{quest['reward_exp']}⭐"
        if quest["reward_item"] == "golden_bullet":
            reward_text += " +💫 Золотая пуля"
        if quest["reward_item"] == "diamond_bullet":
            reward_text += " +💎 Алмазная пуля"
        if quest["reward_item"] == "drone":
            reward_text += " +🛸 Дрон"
        if quest["reward_item"] == "title" and quest["title_name"]:
            reward_text += f" +👑 {quest['title_name']}"
        
        quests_lines.append(f"{status} {i+1}. {need} 🥚 →{reward_text}")
    
    # Топ игроков
    top = sql.execute("""
        SELECT u.username, et.eggs 
        FROM event_top et
        JOIN users u ON u.user_id = et.user_id
        WHERE u.username IS NOT NULL AND et.eggs > 0
        ORDER BY et.eggs DESC 
        LIMIT 5
    """).fetchall()
    
    top_lines = []
    for i, (username, eggs_count) in enumerate(top, 1):
        top_lines.append(f"{i}. @{username} — {eggs_count} 🥚")
    
    text = f"""🎉 **{EVENT_NAME}** 🎉

🥚 Твои {EVENT_CURRENCY}: {eggs}

**📋 ЗАДАНИЯ:**
{chr(10).join(quests_lines)}

**ТОП ПО {EVENT_CURRENCY}:**
{chr(10).join(top_lines) if top_lines else "— пока никого —"}"""
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❓ Что это?", callback_data="event_help")],
        [InlineKeyboardButton(text="🛒 Магазин ивента", callback_data="event_shop_menu")]
    ])
    
    await msg.answer(text, reply_markup=kb)


@dp.callback_query(lambda c: c.data == "event_help")
async def event_help(call: CallbackQuery):
    """Помощь по ивенту"""
    text = f"""📖 **ЧТО ТАКОЕ ИВЕНТ?**

🎯 Ивент "{EVENT_NAME}" — временное событие!

📍 **ВРЕМЕННАЯ ЛОКАЦИЯ:**
"{EVENT_LOCATION}" (доступна с {EVENT_LOCATION_LEVEL} уровня)

🥚 **КАК ПОЛУЧИТЬ {EVENT_CURRENCY}:**
• Убить Опасн/Тяжел/Титан в любой локации → +1 🥚
• Убить любое животное на ивентовой локации → +1 🥚
• Убить титана на ивентовой локации → +5 🥚
• Купить в магазине ивента (1 🥚 = 500 монет)

📋 **ЗАДАНИЯ:**
1. 1 яйцо → 500 монет
2. 5 яиц → 1000 монет
3. 15 яиц → 2000 монет + 1000 опыта
4. 30 яиц → 5000 монет + Золотая пуля
5. 55 яиц → 7500 монет + Алмазная пуля
6. 100 яиц → 15000 монет + Дрон
7. 200 яиц → Титул "🐇 Пасхальный кролик"

🛒 **МАГАЗИН ИВЕНТА** (покупка за яйца):
• 5000 монет — 10 🥚
• Золотая пуля — 3 🥚
• Алмазная пуля — 7 🥚
• Аптечка — 1 🥚
• Титул "🐣 Цыпленок" — 50 🥚
• {EVENT_ITEM_NAME} — 100 🥚

🥚 **{EVENT_ITEM_NAME}:**
Снаряжение (как рюкзак). Пока надето — каждые 24 часа даёт 500 монет!

⏰ Ивент активен до отключения администратором."""
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="event_back_main")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == "event_shop_menu")
async def event_shop_menu(call: CallbackQuery):
    """Магазин ивента"""
    if not EVENT_ACTIVE:
        await call.answer("❌ Ивент не активен!", show_alert=True)
        return
    
    user = ensure_user(call.from_user.id)
    eggs = user[33] if len(user) > 33 else 0
    
    has_golden_egg = sql.execute("SELECT 1 FROM user_equipment WHERE user_id = ? AND equipment = ?", 
                                 (call.from_user.id, EVENT_ITEM_NAME)).fetchone()
    golden_egg_status = "✅ Уже есть" if has_golden_egg else f"❌ {EVENT_ITEM_NAME}"
    
    text = f"""🎪 **МАГАЗИН ИВЕНТА**

🥚 Твои {EVENT_CURRENCY}: {eggs}"""   # <--- ЗАКРЫВАЮЩИЕ КАВЫЧКИ ЗДЕСЬ!

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 5000 монет (10🥚)", callback_data="event_buy:coins:10")],
        [InlineKeyboardButton(text="💫 Золотая пуля (3🥚)", callback_data="event_buy:golden_bullet:3")],
        [InlineKeyboardButton(text="💎 Алмазная пуля (7🥚)", callback_data="event_buy:diamond_bullet:7")],
        [InlineKeyboardButton(text="💊 Аптечка (1🥚)", callback_data="event_buy:medkit:1")],
        [InlineKeyboardButton(text="👑 Титул '🐣 Цыпленок' (50🥚)", callback_data="event_buy:title_chick:50")],
        [InlineKeyboardButton(text=f"{golden_egg_status} (100🥚)", callback_data="event_buy:golden_egg:100")],
        [InlineKeyboardButton(text="🔄 Купить яйца за монеты (500💰 = 1🥚)", callback_data="event_buy_coins")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_shop:{call.from_user.id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")


@dp.callback_query(lambda c: c.data == "event_back_main")
async def event_back_main(call: CallbackQuery):
    """Возврат в главное меню ивента"""
    await event_command(call.message)


@dp.callback_query(lambda c: c.data.startswith("event_buy:"))
async def event_buy_item(call: CallbackQuery):
    """Покупка предмета за яйца"""
    try:
        _, item, price_str = call.data.split(":")
        price = int(price_str)

        user = ensure_user(call.from_user.id)
        eggs = user[33] if len(user) > 33 else 0

        if eggs < price:
            await call.answer(f"❌ Не хватает! Нужно {price} 🥚, у тебя {eggs}", show_alert=True)
            return

        # Списываем яйца
        sql.execute("UPDATE users SET event_eggs = event_eggs - ? WHERE user_id = ?", (price, call.from_user.id))

        # Выдаем награду
        if item == "coins":
            sql.execute("UPDATE users SET coins = coins + 5000 WHERE user_id = ?", (call.from_user.id,))
            await call.answer("✅ Получено 5000 монет!", show_alert=True)

        elif item == "golden_bullet":
            sql.execute("UPDATE users SET golden_bullet = golden_bullet + 1 WHERE user_id = ?", (call.from_user.id,))
            await call.answer("✅ Получена Золотая пуля!", show_alert=True)

        elif item == "diamond_bullet":
            sql.execute("UPDATE users SET diamond_bullet = diamond_bullet + 1 WHERE user_id = ?", (call.from_user.id,))
            await call.answer("✅ Получена Алмазная пуля!", show_alert=True)

        elif item == "medkit":
            # Восстанавливаем 60 HP, но не больше максимума
            user = ensure_user(call.from_user.id)
            current_hp = user[13]
            max_hp = user[14]
            new_hp = min(current_hp + 60, max_hp)
            sql.execute("UPDATE users SET health = ? WHERE user_id = ?", (new_hp, call.from_user.id))
            await call.answer(f"✅ Восстановлено 60 HP! Теперь: {new_hp}/{max_hp}", show_alert=True)

        elif item == "title_chick":
            sql.execute("UPDATE users SET current_title = '🐣 Цыпленок' WHERE user_id = ?", (call.from_user.id,))
            await call.answer("✅ Получен титул '🐣 Цыпленок'!", show_alert=True)

        elif item == "golden_egg":
            owned = sql.execute("SELECT 1 FROM user_equipment WHERE user_id = ? AND equipment = ?", 
                               (call.from_user.id, EVENT_ITEM_NAME)).fetchone()
            if owned:
                await call.answer(f"❌ У тебя уже есть {EVENT_ITEM_NAME}!", show_alert=True)
                sql.execute("UPDATE users SET event_eggs = event_eggs + ? WHERE user_id = ?", (price, call.from_user.id))
                db.commit()
                return
            sql.execute("INSERT INTO user_equipment VALUES (?, ?)", (call.from_user.id, EVENT_ITEM_NAME))
            await call.answer(f"✅ Получен {EVENT_ITEM_NAME}!", show_alert=True)

        db.commit()
        await event_shop_menu(call)

    except Exception as e:
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)
        
# ================== ТОП ==================
@dp.message(lambda msg: msg.text and msg.text.lower() == "топы")
async def top(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Топ по убийствам (все время)", callback_data=f"top_total:{msg.from_user.id}")],
        [InlineKeyboardButton(text="📊 Топ по убийствам (за день)", callback_data=f"top_daily:{msg.from_user.id}")],
        [InlineKeyboardButton(text="⭐ Топ по опыту", callback_data=f"top_exp:{msg.from_user.id}")],
        [InlineKeyboardButton(text="💰 Топ по монетам", callback_data=f"top_coins:{msg.from_user.id}")],
        [InlineKeyboardButton(text="🎯 Топ по титанам", callback_data=f"top_titans:{msg.from_user.id}")],
        [InlineKeyboardButton(text="🎖️ Топ по престижу", callback_data=f"top_prestige_list:{msg.from_user.id}")]
    ])
    await msg.answer("Выберите категорию топа:", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("top_total"))
async def top_total(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваш топ!", show_alert=True)
        return
    
    top_users = sql.execute(
        "SELECT username, total_kills FROM users WHERE username IS NOT NULL AND total_kills > 0 ORDER BY total_kills DESC LIMIT 10"
    ).fetchall()
    
    if not top_users:
        await call.message.edit_text("📭 Пока нет данных в этой категории.")
        return
    
    text = "🏆 Топ по убийствам (все время):\n\n"
    for i, (username, kills) in enumerate(top_users, 1):
        text += f"{i}. @{username} — {kills} убийств\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"top_back:{call.from_user.id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("top_daily"))
async def top_daily(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваш топ!", show_alert=True)
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    top_users = sql.execute(
        "SELECT u.username, s.kills FROM users u "
        "JOIN stats_daily s ON u.user_id = s.user_id "
        "WHERE s.date = ? AND u.username IS NOT NULL AND s.kills > 0 "
        "ORDER BY s.kills DESC LIMIT 10",
        (today,)
    ).fetchall()
    
    if not top_users:
        await call.message.edit_text("📭 Пока нет данных в этой категории.")
        return
    
    text = f"📊 Топ по убийствам (за день, {today}):\n\n"
    for i, (username, kills) in enumerate(top_users, 1):
        text += f"{i}. @{username} — {kills} убийств\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"top_back:{call.from_user.id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("top_exp"))
async def top_exp(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваш топ!", show_alert=True)
        return
    
    top_users = sql.execute(
        "SELECT username, exp, exp/500 as level FROM users "
        "WHERE username IS NOT NULL AND exp > 0 ORDER BY exp DESC LIMIT 10"
    ).fetchall()
    
    if not top_users:
        await call.message.edit_text("📭 Пока нет данных в этой категории.")
        return
    
    text = "⭐ Топ по опыту (и уровню):\n\n"
    for i, (username, exp, level) in enumerate(top_users, 1):
        text += f"{i}. @{username} — Опыт: {exp} (Уровень: {int(level)})\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"top_back:{call.from_user.id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("top_coins"))
async def top_coins(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваш топ!", show_alert=True)
        return
    
    top_users = sql.execute(
        "SELECT username, coins FROM users "
        "WHERE username IS NOT NULL AND coins > 0 ORDER BY coins DESC LIMIT 10"
    ).fetchall()
    
    if not top_users:
        await call.message.edit_text("📭 Пока нет данных в этой категории.")
        return
    
    text = "💰 Топ по монетам:\n\n"
    for i, (username, coins) in enumerate(top_users, 1):
        text += f"{i}. @{username} — {coins} монет\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"top_back:{call.from_user.id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("top_titans"))
async def top_titans(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваш топ!", show_alert=True)
        return
    
    titan_animals = []
    for location_name, location_data in LOCATIONS.items():
        if "Титан" in location_data["animals"]:
            titan_animals.extend(location_data["animals"]["Титан"])
    
    if not titan_animals:
        await call.message.edit_text("🎯 В игре пока нет титанов.")
        return
    
    titan_counts = {}
    
    for username, user_id_db in sql.execute("SELECT username, user_id FROM users WHERE username IS NOT NULL").fetchall():
        total_titans = 0
        for animal in titan_animals:
            result = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?",
                               (user_id_db, animal)).fetchone()
            if result:
                total_titans += result[0]
        
        if total_titans > 0:
            titan_counts[username] = total_titans
    
    if not titan_counts:
        await call.message.edit_text("🎯 Пока никто не убил ни одного титана.")
        return
    
    sorted_titans = sorted(titan_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    text = "🎯 Топ по убийству титанов:\n\n"
    for i, (username, count) in enumerate(sorted_titans, 1):
        text += f"{i}. @{username} — {count} титанов\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"top_back:{call.from_user.id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("top_prestige_list"))
async def top_prestige_list(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваш топ!", show_alert=True)
        return
    
    top_users = sql.execute(
        "SELECT username, prestige FROM users WHERE username IS NOT NULL AND prestige > 0 ORDER BY prestige DESC, exp DESC LIMIT 10"
    ).fetchall()
    
    if not top_users:
        await call.message.edit_text("🎖️ Пока никто не получил престиж.")
        return
    
    text = "🎖️ Топ по престижу:\n\n"
    for i, (username, prestige) in enumerate(top_users, 1):
        prestige_name = PRESTIGES.get(prestige, {}).get("name", f"Престиж {prestige}")
        text += f"{i}. @{username} — {prestige_name}\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"top_back:{call.from_user.id}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("top_back"))
async def top_back(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваш топ!", show_alert=True)
        return
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Топ по убийствам (все время)", callback_data=f"top_total:{call.from_user.id}")],
        [InlineKeyboardButton(text="📊 Топ по убийствам (за день)", callback_data=f"top_daily:{call.from_user.id}")],
        [InlineKeyboardButton(text="⭐ Топ по опыту", callback_data=f"top_exp:{call.from_user.id}")],
        [InlineKeyboardButton(text="💰 Топ по монетам", callback_data=f"top_coins:{call.from_user.id}")],
        [InlineKeyboardButton(text="🎯 Топ по титанам", callback_data=f"top_titans:{call.from_user.id}")],
        [InlineKeyboardButton(text="🎖️ Топ по престижу", callback_data=f"top_prestige_list:{call.from_user.id}")]
    ])
    await call.message.edit_text("Выберите категорию топа:", reply_markup=kb)

# ================== МАГАЗИН (ПОЛНОСТЬЮ ПЕРЕПИСАН) ==================

@dp.message(lambda msg: msg.text and msg.text.lower() == "магазин")
async def shop(msg: Message):
    """Главное меню магазина"""
    user_id = msg.from_user.id
    buttons = [
        [InlineKeyboardButton(text="🔫 Оружие", callback_data=f"weapons_menu:{user_id}")],
        [InlineKeyboardButton(text="🎩 Снаряжение", callback_data=f"equipment_menu:{user_id}")],
        [InlineKeyboardButton(text="⚡ Баффы", callback_data=f"buffs_menu:{user_id}")],  # ← этот формат
        [InlineKeyboardButton(text="🛡️ Выживание", callback_data=f"survival_shop:{user_id}")]  # ← ИЗМЕНЕНО
    ]
    
    if is_event_active():
        buttons.append([InlineKeyboardButton(text="🎪 Ивент", callback_data="event_shop_menu")])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await msg.answer("🏪 **Добро пожаловать в магазин!**\n\nВыберите категорию:", reply_markup=kb, parse_mode="Markdown")
    
# ================== ОРУЖИЕ ==================
@dp.callback_query(lambda c: c.data.startswith("weapons_menu"))
async def weapons_menu(call: CallbackQuery):
    try:
        user_id = int(call.data.split(":")[1])
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш магазин!", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        level = get_level(user[2])
        
        buttons = []
        group_emojis = {
            "обычные": "⚪", "огненные": "🔥", "ледяные": "❄️",
            "ядовитые": "🧪", "электрические": "⚡", "тёмные": "🌑", "священные": "✨"
        }
        
        for group_name, group_data in WEAPON_GROUPS.items():
            emoji = group_emojis.get(group_name, "🔫")
            required_level = group_data["level_req"]
            
            if level >= required_level:
                # Доступно
                buttons.append([InlineKeyboardButton(
                    text=f"{emoji} {group_name.upper()} (ур. {required_level}+)",
                    callback_data=f"weapons_group:{user_id}:{group_name}"
                )])
            else:
                # Заблокировано
                buttons.append([InlineKeyboardButton(
                    text=f"🔒 {emoji} {group_name.upper()} (нужен {required_level} уровень)",
                    callback_data="no_action"
                )])
        
        buttons.append([InlineKeyboardButton(text="🔙 Назад в магазин", callback_data=f"back_to_shop:{user_id}")])
        
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.edit_text(
            f"💰 Баланс: {user[1]} монет | 🏆 Уровень: {level}\n\n"
            f"🔫 **Выберите группу оружия:**",
            reply_markup=kb, parse_mode="Markdown"
        )
    except Exception as e:
        await call.answer(f"❌ Ошибка", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("weapons_group:"))
async def weapons_group_menu(call: CallbackQuery):
    try:
        _, user_id, group_name = call.data.split(":")
        user_id = int(user_id)
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш магазин!", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        level = get_level(user[2])
        
        group_data = WEAPON_GROUPS.get(group_name)
        if not group_data or level < group_data["level_req"]:
            await call.answer("❌ Группа недоступна!", show_alert=True)
            return
        
        owned_weapons = [w[0] for w in sql.execute("SELECT weapon FROM user_weapons WHERE user_id = ?", (call.from_user.id,)).fetchall()]
        
        buttons = []
        for weapon_name, weapon_data in group_data["weapons"].items():
            status = "✅ " if weapon_name in owned_weapons else ""
            
            # Определяем тип получения и значок
            obtain = weapon_data.get("obtain", {})
            obtain_type = obtain.get("type", "shop")
            
            if obtain_type == "shop":
                price = obtain.get("price", 0)
                suffix = f" — {price}💰"
            elif obtain_type == "achievement":
                suffix = " — 🏆 ДОСТИЖЕНИЕ"
            elif obtain_type == "craft":
                suffix = " — 🔨 КРАФТ"
            elif obtain_type == "case":
                suffix = " — 📦 КЕЙС"
            elif obtain_type == "start":
                suffix = " — 🎁 СТАРТОВОЕ"
            else:
                suffix = ""
            
            weapon_id = WEAPON_IDS[weapon_name]
            buttons.append([InlineKeyboardButton(
                text=f"{status}{weapon_name}{suffix}",
                callback_data=f"wi:{user_id}:{weapon_id}"
            )])
        
        buttons.append([InlineKeyboardButton(text="🔙 Назад к группам", callback_data=f"weapons_menu:{user_id}")])
        
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.edit_text(
            f"💰 Баланс: {user[1]} монет | 🏆 Уровень: {level}\n\n"
            f"🔫 **{group_name.upper()}** — оружие:",
            reply_markup=kb, parse_mode="Markdown"
        )
    except Exception as e:
        await call.answer("❌ Ошибка", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("wi:"))
async def weapon_info(call: CallbackQuery):
    try:
        _, user_id, weapon_id = call.data.split(":")
        user_id = int(user_id)
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш магазин!", show_alert=True)
            return
        
        weapon = WEAPON_NAMES.get(weapon_id)
        if not weapon or weapon not in WEAPONS_DATA:
            await call.answer("❌ Оружие не найдено", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        weapon_data = get_weapon_data(weapon)
        price = get_weapon_price(weapon)
        level_req = weapon_data["level_req"]
        group = weapon_data["group"]
        
        owned = sql.execute("SELECT 1 FROM user_weapons WHERE user_id = ? AND weapon = ?", (call.from_user.id, weapon)).fetchone()
        chances = weapon_data["chances"]
        damage = weapon_data["damage"]
        
        group_emoji = {"обычные": "⚪", "огненные": "🔥", "ледяные": "❄️", "ядовитые": "🧪", "электрические": "⚡", "тёмные": "🌑", "священные": "✨"}.get(group, "🔫")
        user_level = get_level(user[2])
        level_ok = user_level >= level_req
        
        if owned:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Уже куплено", callback_data="no_action")],
                [InlineKeyboardButton(text="🔄 Выбрать", callback_data=f"sw:{user_id}:{weapon_id}")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data=f"weapons_group:{user_id}:{group}")]
            ])
            status_text = "✅ Уже есть!"
            
        elif not level_ok:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"🔒 Требуется {level_req} уровень", callback_data="no_action")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data=f"weapons_group:{user_id}:{group}")]
            ])
            status_text = f"❌ Нужен {level_req} уровень (у вас {user_level})"
            
        else:
            obtain = weapon_data.get("obtain", {})
            obtain_type = obtain.get("type", "shop")
            
            if obtain_type == "shop":
                price = obtain.get("price", 0)
                if user[1] >= price:
                    kb = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f"💰 Купить за {price} монет", callback_data=f"bw:{user_id}:{weapon_id}")],
                        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"weapons_group:{user_id}:{group}")]
                    ])
                    status_text = "✅ Достаточно средств"
                else:
                    kb = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f"❌ Не хватает {price - user[1]} монет", callback_data="no_action")],
                        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"weapons_group:{user_id}:{group}")]
                    ])
                    status_text = f"❌ Не хватает {price - user[1]} монет"
                    
            elif obtain_type == "achievement":
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🏆 ДОСТИЖЕНИЕ", callback_data="no_action")],
                    [InlineKeyboardButton(text="🔙 Назад", callback_data=f"weapons_group:{user_id}:{group}")]
                ])
                req = obtain.get("requirement", "выполните достижение")
                status_text = f"📋 Получение: {req}"
                
            elif obtain_type == "craft":
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔨 КРАФТ", callback_data="no_action")],
                    [InlineKeyboardButton(text="🔙 Назад", callback_data=f"weapons_group:{user_id}:{group}")]
                ])
                req = obtain.get("requirement", "")
                status_text = f"📋 Получение: КРАФТ" + (f" ({req})" if req else "")
                
            elif obtain_type == "case":
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="📦 КЕЙС", callback_data="no_action")],
                    [InlineKeyboardButton(text="🔙 Назад", callback_data=f"weapons_group:{user_id}:{group}")]
                ])
                req = obtain.get("requirement", "")
                status_text = f"📋 Получение: КЕЙС" + (f" ({req})" if req else "")
                
            elif obtain_type == "start":
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔙 Назад", callback_data=f"weapons_group:{user_id}:{group}")]
                ])
                status_text = "🎁 Стартовое оружие"
                
            else:
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔙 Назад", callback_data=f"weapons_group:{user_id}:{group}")]
                ])
                status_text = "📋 Получение: неизвестно"

        text = f"{group_emoji} **{weapon}** ({group})\n\n📝 {weapon_data['description']}\n\n💥 Урон: {damage}\n🎯 Шансы:\n• Мелочь: {chances[0]}%\n• Средн: {chances[1]}%\n• Опасн: {chances[2]}%\n• Тяжел: {chances[3]}%\n• Титан: {chances[4]}%\n"
        if weapon_data["ability"]:
            text += f"\n✨ Способность: {weapon_data['ability_desc']} ({weapon_data['ability_chance']}%)\n"
        text += f"\n⭐ Требуемый уровень: {level_req}\n" + (f"💰 Цена: {price} монет\n" if price > 0 else "") + f"💳 Баланс: {user[1]} монет\n{status_text}"
        
        await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        await call.answer(f"❌ Ошибка", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("bw:"))
async def buy_weapon(call: CallbackQuery):
    try:
        _, user_id, weapon_id = call.data.split(":")
        user_id = int(user_id)
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        weapon = WEAPON_NAMES.get(weapon_id)
        if not weapon:
            await call.answer("❌ Оружие не найдено", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        price = get_weapon_price(weapon)
        level_req = get_weapon_level_req(weapon)
        user_level = get_level(user[2])
        
        owned = sql.execute("SELECT 1 FROM user_weapons WHERE user_id = ? AND weapon = ?", (call.from_user.id, weapon)).fetchone()
        if owned:
            await call.answer("✅ Уже есть!", show_alert=True)
            return
        if user_level < level_req:
            await call.answer(f"❌ Нужен {level_req} уровень!", show_alert=True)
            return
        if user[1] < price:
            await call.answer(f"❌ Не хватает {price - user[1]} монет!", show_alert=True)
            return
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да, купить", callback_data=f"cbw:{user_id}:{weapon_id}")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data=f"wi:{user_id}:{weapon_id}")]
        ])
        await call.message.edit_text(f"❓ **Купить {weapon} за {price} монет?**\n\n💰 Баланс: {user[1]} → {user[1] - price}", reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        await call.answer("❌ Ошибка", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("cbw:"))
async def confirm_buy_weapon(call: CallbackQuery):
    try:
        _, user_id, weapon_id = call.data.split(":")
        user_id = int(user_id)
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        weapon = WEAPON_NAMES.get(weapon_id)
        if not weapon:
            await call.answer("❌ Оружие не найдено", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        price = get_weapon_price(weapon)
        
        owned = sql.execute("SELECT 1 FROM user_weapons WHERE user_id = ? AND weapon = ?", (call.from_user.id, weapon)).fetchone()
        if owned:
            await call.answer("✅ Уже есть!", show_alert=True)
            return
        if user[1] < price:
            await call.answer("❌ Не хватает монет!", show_alert=True)
            return
        
        sql.execute("UPDATE users SET coins = coins - ? WHERE user_id = ?", (price, call.from_user.id))
        sql.execute("INSERT OR IGNORE INTO user_weapons VALUES (?, ?)", (call.from_user.id, weapon))
        sql.execute("UPDATE users SET weapon = ? WHERE user_id = ?", (weapon, call.from_user.id))
        db.commit()
        
        await call.message.edit_text(f"✅ **Куплено!** {weapon} за {price} монет.\nОружие экипировано.", parse_mode="Markdown")
        await asyncio.sleep(2)
        await weapons_menu(call)
    except Exception as e:
        await call.answer("❌ Ошибка", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("sw:"))
async def select_weapon(call: CallbackQuery):
    try:
        _, user_id, weapon_id = call.data.split(":")
        user_id = int(user_id)
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваше оружие!", show_alert=True)
            return
        
        weapon = WEAPON_NAMES.get(weapon_id)
        if not weapon:
            await call.answer("❌ Оружие не найдено", show_alert=True)
            return
        
        owned = sql.execute("SELECT 1 FROM user_weapons WHERE user_id = ? AND weapon = ?", (call.from_user.id, weapon)).fetchone()
        if not owned:
            await call.answer("❌ У вас нет этого оружия!", show_alert=True)
            return
        
        sql.execute("UPDATE users SET weapon = ? WHERE user_id = ?", (weapon, call.from_user.id))
        db.commit()
        await call.answer(f"✅ Экипировано {weapon}!", show_alert=True)
        await weapons_menu(call)
    except Exception as e:
        await call.answer("❌ Ошибка", show_alert=True)

# ================== СНАРЯЖЕНИЕ ==================

@dp.callback_query(lambda c: c.data.startswith("equipment_menu"))
async def equipment_menu(call: CallbackQuery):
    """Меню снаряжения"""
    try:
        user_id = int(call.data.split(":")[1])
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш магазин!", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        owned_equipment = get_user_equipment(call.from_user.id)
        
        buttons = []
        for eq_name, eq_data in EQUIPMENT.items():
            if eq_name in owned_equipment:
                status = "✅ "
            else:
                status = ""
            buttons.append([InlineKeyboardButton(
                text=f"{status}{eq_name} — {eq_data['price']}💰",
                callback_data=f"equipment_info:{user_id}:{eq_name}"
            )])
        
        buttons.append([InlineKeyboardButton(text="🔙 Назад в магазин", callback_data=f"back_to_shop:{user_id}")])
        
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.edit_text(f"💰 Ваш баланс: {user[1]} монет\n\n🎩 **Выберите снаряжение:**", reply_markup=kb, parse_mode="Markdown")
    
    except Exception as e:
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("equipment_info"))
async def equipment_info(call: CallbackQuery):
    """Информация о снаряжении"""
    try:
        _, user_id, eq_name = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш магазин!", show_alert=True)
            return
        
        if eq_name not in EQUIPMENT:
            await call.answer("❌ Предмет не найден", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        eq_data = EQUIPMENT[eq_name]
        
        owned = eq_name in get_user_equipment(call.from_user.id)
        
        # КОРОТКИЙ callback
        short = eq_name.replace("Улучшенные ловушки", "ut").replace("Продвинутый искатель", "ps")
        
        if owned:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Уже куплено", callback_data="no_action")],
                [InlineKeyboardButton(text="🔙 Назад к снаряжению", callback_data=f"equipment_menu:{user_id}")]
            ])
            status_text = "✅ Этот предмет уже у вас есть!"
        else:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"💰 Купить за {eq_data['price']}💰", callback_data=f"buy_equip:{user_id}:{short}")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data=f"equipment_menu:{user_id}")]
            ])
            if user[1] >= eq_data['price']:
                status_text = "✅ Достаточно средств"
            else:
                status_text = f"❌ Не хватает {eq_data['price'] - user[1]} монет"
        
        text = f"🎩 **{eq_name}**\n\n"
        text += f"📝 {eq_data['description']}\n\n"
        text += f"💰 Цена: {eq_data['price']} монет\n"
        text += f"💳 Ваш баланс: {user[1]} монет\n"
        text += f"{status_text}"
        
        await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    
    except Exception as e:
        print(f"Ошибка equipment_info: {e}")
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("buy_equip:"))
async def buy_equip_handler(call: CallbackQuery):
    """Обработчик покупки снаряжения"""
    print(f"buy_equip вызван с data: {call.data}")
    
    try:
        _, user_id, short = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        # Восстанавливаем название
        if short == "ut":
            eq_name = "Улучшенные ловушки"
        elif short == "ps":
            eq_name = "Продвинутый искатель"
        else:
            eq_name = short
        
        print(f"Покупка: {eq_name}")
        
        if eq_name not in EQUIPMENT:
            await call.answer("❌ Предмет не найден", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        eq_data = EQUIPMENT[eq_name]
        
        # Проверяем баланс
        if user[1] < eq_data['price']:
            await call.answer(f"❌ Не хватает {eq_data['price'] - user[1]} монет!", show_alert=True)
            return
        
        # Проверяем, не куплено ли уже
        owned = eq_name in get_user_equipment(call.from_user.id)
        if owned:
            await call.answer("✅ У вас уже есть этот предмет!", show_alert=True)
            return
        
        # Создаем кнопки подтверждения
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да, купить", callback_data=f"confirm_eq:{user_id}:{short}")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data=f"equipment_info:{user_id}:{eq_name}")]
        ])
        
        await call.message.edit_text(
            f"❓ **Подтверждение покупки**\n\n"
            f"Вы хотите купить {eq_name} за {eq_data['price']} монет?\n\n"
            f"📝 {eq_data['description']}\n\n"
            f"💰 Ваш баланс: {user[1]} монет\n"
            f"💰 После покупки: {user[1] - eq_data['price']} монет",
            reply_markup=kb,
            parse_mode="Markdown"
        )
        
        await call.answer()
        
    except Exception as e:
        print(f"Ошибка buy_equip_handler: {e}")
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("confirm_eq:"))
async def confirm_eq_handler(call: CallbackQuery):
    """Подтверждение покупки снаряжения"""
    print(f"confirm_eq вызван с data: {call.data}")
    
    try:
        _, user_id, short = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        # Восстанавливаем название
        if short == "ut":
            eq_name = "Улучшенные ловушки"
        elif short == "ps":
            eq_name = "Продвинутый искатель"
        else:
            eq_name = short
        
        eq_data = EQUIPMENT[eq_name]
        
        # Получаем данные через отдельное соединение
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        
        # Проверяем баланс
        user_data = cur.execute("SELECT coins FROM users WHERE user_id = ?", (call.from_user.id,)).fetchone()
        
        if not user_data or user_data[0] < eq_data['price']:
            conn.close()
            await call.answer("❌ Не хватает монет!", show_alert=True)
            return
        
        # Проверяем, не куплено ли уже
        owned = cur.execute("SELECT 1 FROM user_equipment WHERE user_id = ? AND equipment = ?", 
                           (call.from_user.id, eq_name)).fetchone()
        
        if owned:
            conn.close()
            await call.answer("✅ У вас уже есть этот предмет!", show_alert=True)
            return
        
        # Покупка
        cur.execute("UPDATE users SET coins = coins - ? WHERE user_id = ?", (eq_data['price'], call.from_user.id))
        cur.execute("INSERT INTO user_equipment VALUES (?, ?)", (call.from_user.id, eq_name))
        conn.commit()
        conn.close()
        
        # Обновляем глобальную БД
        db.commit()
        
        effect_text = ""
        if eq_name == "Улучшенные ловушки":
            effect_text = "\n\n🪤 **Теперь ловушки находят 5 животных вместо 3!**"
        
        await call.message.edit_text(
            f"✅ **Покупка успешна!**\n\n"
            f"Вы купили {eq_name}!\n"
            f"{eq_data['description']}{effect_text}",
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(2)
        await equipment_menu(call)
        
    except Exception as e:
        print(f"Ошибка confirm_eq_handler: {e}")
        import traceback
        traceback.print_exc()
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("buy_equipment"))
async def buy_equipment(call: CallbackQuery):
    """Покупка снаряжения (с подтверждением)"""
    try:
        _, user_id, eq_name = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        eq_data = EQUIPMENT[eq_name]
        
        owned = eq_name in get_user_equipment(call.from_user.id)
        
        if owned:
            await call.answer("✅ У вас уже есть этот предмет!", show_alert=True)
            return
        
        if user[1] < eq_data['price']:
            await call.answer(f"❌ Не хватает {eq_data['price'] - user[1]} монет!", show_alert=True)
            return
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да, купить", callback_data=f"confirm_buy_equipment:{user_id}:{eq_name}")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data=f"equipment_info:{user_id}:{eq_name}")]
        ])
        
        await call.message.edit_text(
            f"❓ **Подтверждение покупки**\n\n"
            f"Вы хотите купить {eq_name} за {eq_data['price']} монет?\n\n"
            f"📝 {eq_data['description']}\n\n"
            f"💰 Ваш баланс: {user[1]} монет\n"
            f"💰 После покупки: {user[1] - eq_data['price']} монет",
            reply_markup=kb,
            parse_mode="Markdown"
        )
    
    except Exception as e:
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("confirm_buy_equipment"))
async def confirm_buy_equipment(call: CallbackQuery):
    """Подтверждение покупки снаряжения"""
    try:
        _, user_id, eq_name = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        # Получаем данные пользователя через отдельное соединение
        conn = sqlite3.connect("hunt.db")
        cur = conn.cursor()
        
        # Проверяем баланс
        user_data = cur.execute("SELECT coins FROM users WHERE user_id = ?", (call.from_user.id,)).fetchone()
        if not user_data:
            conn.close()
            await call.answer("❌ Пользователь не найден!", show_alert=True)
            return
        
        eq_data = EQUIPMENT[eq_name]
        
        if user_data[0] < eq_data['price']:
            conn.close()
            await call.answer(f"❌ Не хватает монет!", show_alert=True)
            return
        
        # Проверяем, не куплено ли уже
        owned = cur.execute("SELECT 1 FROM user_equipment WHERE user_id = ? AND equipment = ?", 
                           (call.from_user.id, eq_name)).fetchone()
        
        if owned:
            conn.close()
            await call.answer("✅ У вас уже есть этот предмет!", show_alert=True)
            return
        
        # Покупка
        cur.execute("UPDATE users SET coins = coins - ? WHERE user_id = ?", (eq_data['price'], call.from_user.id))
        cur.execute("INSERT INTO user_equipment VALUES (?, ?)", (call.from_user.id, eq_name))
        conn.commit()
        
        # Обновляем максимальное здоровье если это рюкзак
        if "Рюкзак" in eq_name:
            # Обновляем через основной курсор или отдельно
            sql.execute("UPDATE users SET max_health = ? WHERE user_id = ?", 
                       (get_max_health_from_equipment(call.from_user.id), call.from_user.id))
            db.commit()
        
        conn.close()
        
        # Специальное сообщение для улучшенных ловушек
        if eq_name == "Улучшенные ловушки":
            effect_text = "\n\n🪤 Теперь ловушки будут находить 5 животных вместо 3!"
        else:
            effect_text = ""
        
        await call.message.edit_text(
            f"✅ **Покупка успешна!**\n\n"
            f"Вы купили {eq_name}!\n"
            f"{eq_data['description']}{effect_text}",
            parse_mode="Markdown"
        )
        
        # Возврат в меню снаряжения через 2 секунды
        await asyncio.sleep(2)
        await equipment_menu(call)
    
    except Exception as e:
        print(f"Ошибка confirm_buy_equipment: {e}")

@dp.callback_query(lambda c: c.data == "buffs_menu" or c.data.startswith("buffs_menu:"))
async def buffs_menu(call: CallbackQuery):
    """Меню баффов с динамическими ценами"""
    try:
        # Извлекаем user_id из callback
        if ":" in call.data:
            user_id = int(call.data.split(":")[1])
        else:
            user_id = call.from_user.id
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш магазин!", show_alert=True)
            return
        
        user = ensure_user(call.from_user.id)
        coins = user[1]
        
        # Определяем множитель цены
        if coins <= 20000:
            multiplier = 1.0
            multiplier_text = "🟢 Базовая цена (≤20к монет)"
        elif coins <= 50000:
            multiplier = 2.0
            multiplier_text = "🟡 Цена x2 (20к-50к монет)"
        elif coins <= 100000:
            multiplier = 3.0
            multiplier_text = "🟠 Цена x3 (50к-100к монет)"
        else:
            multiplier = 3.5
            multiplier_text = "🔴 Цена x3.5 (≥100к монет)"
        
        # Создаём кнопки для каждого баффа с КОРОТКИМИ callback'ами
        buttons = []
        for buff_name, buff_data in BUFFS.items():
            original_price = buff_data['price']
            final_price = int(original_price * multiplier)
            
            # Создаём короткий ID для баффа (цифровой)
            buff_id = list(BUFFS.keys()).index(buff_name)
            
            # Цена в callback (только число)
            callback_data = f"b_{user_id}_{buff_id}_{final_price}"
            
            buttons.append([InlineKeyboardButton(
                text=f"{buff_name} — {final_price}💰",
                callback_data=callback_data
            )])
        
        buttons.append([InlineKeyboardButton(text="🔙 Назад в магазин", callback_data=f"back_to_shop:{user_id}")])
        
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await call.message.edit_text(
            f"💰 Ваш баланс: {coins} монет\n"
            f"📊 {multiplier_text}\n\n"
            f"⚡ **Выберите бафф:**", 
            reply_markup=kb, 
            parse_mode="Markdown"
        )
        
    except Exception as e:
        print(f"Ошибка buffs_menu: {e}")
        await call.answer("❌ Ошибка при открытии магазина баффов", show_alert=True)
@dp.callback_query(lambda c: c.data.startswith("b_"))
async def buff_info_handler(call: CallbackQuery):
    """Информация о баффе"""
    try:
        # Формат: b_{user_id}_{buff_id}_{price}
        parts = call.data.split("_")
        if len(parts) < 4:
            await call.answer("❌ Ошибка данных", show_alert=True)
            return
        
        user_id = int(parts[1])
        buff_id = int(parts[2])
        price = int(parts[3])
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш магазин!", show_alert=True)
            return
        
        # Получаем название баффа по ID
        buff_names = list(BUFFS.keys())
        if buff_id >= len(buff_names):
            await call.answer("❌ Бафф не найден", show_alert=True)
            return
        
        buff_name = buff_names[buff_id]
        buff_data = BUFFS[buff_name]
        
        user = ensure_user(call.from_user.id)
        
        if user[1] >= price:
            status_text = "✅ Достаточно средств"
        else:
            status_text = f"❌ Не хватает {price - user[1]} монет"
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"💰 Купить за {price} монет", callback_data=f"buy_{user_id}_{buff_id}_{price}")],
            [InlineKeyboardButton(text="🔙 Назад к баффам", callback_data=f"buffs_menu:{user_id}")]
        ])
        
        text = f"⚡ **{buff_name}**\n\n"
        text += f"📝 {buff_data['description']}\n\n"
        text += f"💰 Цена: {price} монет\n"
        text += f"💳 Ваш баланс: {user[1]} монет\n"
        text += f"{status_text}"
        
        await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Ошибка buff_info_handler: {e}")
        await call.answer("❌ Ошибка", show_alert=True)
        
@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def buy_buff_handler(call: CallbackQuery):
    """Покупка баффа"""
    try:
        # Формат: buy_{user_id}_{buff_id}_{price}
        parts = call.data.split("_")
        if len(parts) < 4:
            await call.answer("❌ Ошибка данных", show_alert=True)
            return
        
        user_id = int(parts[1])
        buff_id = int(parts[2])
        price = int(parts[3])
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        # Получаем название баффа по ID
        buff_names = list(BUFFS.keys())
        if buff_id >= len(buff_names):
            await call.answer("❌ Бафф не найден", show_alert=True)
            return
        
        buff_name = buff_names[buff_id]
        buff_data = BUFFS[buff_name]
        
        user = ensure_user(call.from_user.id)
        
        if user[1] < price:
            await call.answer(f"❌ Не хватает {price - user[1]} монет!", show_alert=True)
            return
        
        # Кнопки подтверждения
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да, купить", callback_data=f"confirm_{user_id}_{buff_id}_{price}")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data=f"b_{user_id}_{buff_id}_{price}")]
        ])
        
        await call.message.edit_text(
            f"❓ **Подтверждение покупки**\n\n"
            f"Вы хотите купить {buff_name} за {price} монет?\n\n"
            f"📝 {buff_data['description']}\n\n"
            f"💰 Ваш баланс: {user[1]} монет\n"
            f"💰 После покупки: {user[1] - price} монет",
            reply_markup=kb,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        print(f"Ошибка buy_buff_handler: {e}")
        await call.answer("❌ Ошибка", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_buy_buff_handler(call: CallbackQuery):
    """Подтверждение покупки баффа"""
    try:
        # Формат: confirm_{user_id}_{buff_id}_{price}
        parts = call.data.split("_")
        if len(parts) < 4:
            await call.answer("❌ Ошибка данных", show_alert=True)
            return
        
        user_id = int(parts[1])
        buff_id = int(parts[2])
        price = int(parts[3])
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        # Получаем название баффа по ID
        buff_names = list(BUFFS.keys())
        if buff_id >= len(buff_names):
            await call.answer("❌ Бафф не найден", show_alert=True)
            return
        
        buff_name = buff_names[buff_id]
        
        user = ensure_user(call.from_user.id)
        
        if user[1] < price:
            await call.answer(f"❌ Не хватает монет!", show_alert=True)
            return
        
        # Списание монет
        sql.execute("UPDATE users SET coins = coins - ? WHERE user_id = ?", (price, call.from_user.id))
        
        # Добавляем бафф в инвентарь (НЕ АКТИВИРУЕМ)
        add_user_buff(call.from_user.id, buff_name, 1)
        
        db.commit()
        
        await call.message.edit_text(
            f"✅ **Покупка успешна!**\n\n"
            f"Вы купили {buff_name}!\n"
            f"Бафф добавлен в инвентарь. Используйте команду **баффы**, чтобы активировать.",
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(2)
        await buffs_menu(call)
        
    except Exception as e:
        print(f"Ошибка confirm_buy_buff_handler: {e}")
        await call.answer("❌ Ошибка", show_alert=True)

        # ===== ДОБАВЛЯЕМ БАФФ В ИНВЕНТАРЬ (НЕ АКТИВИРУЕМ) =====
        add_user_buff(call.from_user.id, buff_name, 1)
        
        db.commit()
        
        await call.message.edit_text(
            f"✅ **Покупка успешна!**\n\n"
            f"Вы купили {buff_name}!\n"
            f"Бафф добавлен в инвентарь. Используйте команду **баффы**, чтобы активировать.",
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(2)
        await buffs_menu(call)
    
    except Exception as e:
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)
        
        await call.message.edit_text(
            f"✅ **Покупка успешна!**\n\n"
            f"Вы купили {buff_name}!\n\n"
            f"{effect_text}",
            parse_mode="Markdown"
        )
        
        # Возврат в меню баффов через 2 секунды
        await asyncio.sleep(2)
        await buffs_menu(call)
    
    except Exception as e:
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("select_drone"))
async def select_drone_target(call: CallbackQuery):
    """Выбор цели для дрона"""
    try:
        _, user_id, animal = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш выбор!", show_alert=True)
            return
        
        expires_at = int(time.time()) + 1800
        
        sql.execute("UPDATE users SET drone_target = ?, drone_expires = ? WHERE user_id = ?",
                   (animal, expires_at, call.from_user.id))
        db.commit()
        
        await call.message.edit_text(
            f"✅ **Дрон настроен!**\n\n"
            f"Цель: {animal}\n"
            f"📈 +10% шанс найти это животное в течение 30 минут.",
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(2)
        await buffs_menu(call)
    
    except Exception as e:
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("ultra_drone:"))
async def select_ultra_drone_target(call: CallbackQuery):
    """Выбор цели для ультра-звукового дрона"""
    try:
        parts = call.data.split(":")
        if len(parts) < 3:
            await call.answer("❌ Ошибка данных", show_alert=True)
            return
        
        user_id = int(parts[1])
        animal = parts[2]  # животное уже в callback
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш выбор!", show_alert=True)
            return
        
        expires_at = int(time.time()) + 1800
        
        sql.execute("UPDATE users SET drone_target = ?, drone_expires = ? WHERE user_id = ?",
                   (animal, expires_at, call.from_user.id))
        db.commit()
        
        await call.message.edit_text(
            f"✅ **Ультра-звуковой дрон настроен!**\n\n"
            f"Цель: {animal}\n"
            f"📈 +10% шанс найти это животное в течение 30 минут.",
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(2)
        await buffs_menu(call)
    
    except Exception as e:
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)

# ================== ВЫЖИВАНИЕ ==================
# ================== СОЗДАНИЕ ID ДЛЯ ЛОКАЦИЙ ==================
# ЭТО ДОЛЖНО БЫТЬ ПОСЛЕ ТОГО, КАК LOCATIONS УЖЕ ПОЛНОСТЬЮ ЗАПОЛНЕНА

LOCATION_IDS = {}
LOCATION_NAMES = {}
loc_counter = 0
for loc_name in LOCATIONS.keys():
    if loc_name != "Тайга":  # Тайгу пропускаем
        LOCATION_IDS[str(loc_counter)] = loc_name
        LOCATION_NAMES[loc_name] = str(loc_counter)
        loc_counter += 1

# Тайгу добавляем отдельно
LOCATION_IDS[str(loc_counter)] = "Тайга"
LOCATION_NAMES["Тайга"] = str(loc_counter)
@dp.callback_query(lambda c: c.data.startswith("survival_shop:"))
async def survival_shop(call: CallbackQuery):
    try:
        user_id = int(call.data.split(":")[1])
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваше меню!", show_alert=True)
            return
        
        user = ensure_user(user_id)
        level = get_level(user[2])
        
        keyboard = []
        for loc_name, loc_data in LOCATIONS.items():
            # УБИРАЕМ проверку на "Тайга" - теперь Тайга тоже доступна
            if can_use_location(level, loc_name):
                loc_id = LOCATION_NAMES.get(loc_name, str(len(keyboard)))
                keyboard.append([InlineKeyboardButton(
                    text=f"📍 {loc_name} (ур. {loc_data['level']}+)",
                    callback_data=f"surv_show:{user_id}:{loc_id}"
                )])
            else:
                keyboard.append([InlineKeyboardButton(
                    text=f"🔒 {loc_name} (нужен {loc_data['level']} уровень)",
                    callback_data="no_action"
                )])
        
        keyboard.append([InlineKeyboardButton(text="🔙 Назад в магазин", callback_data=f"back_to_shop:{user_id}")])
        
        await call.message.edit_text(
            f"💰 Ваш баланс: {user[1]} монет\n\n"
            f"🛡️ МАГАЗИН ВЫЖИВАНИЯ\n\n"
            f"Выберите локацию:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
        
    except Exception as e:
        print(f"Ошибка survival_shop: {e}")
        await call.answer(f"❌ Ошибка: {str(e)[:50]}", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("surv_show:"))
async def surv_show_items(call: CallbackQuery):
    try:
        parts = call.data.split(":")
        user_id = int(parts[1])
        loc_id = parts[2]  # короткий ID
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваше меню!", show_alert=True)
            return
        
        # Получаем название локации по ID
        location_name = LOCATION_IDS.get(loc_id)
        if not location_name:
            await call.answer("❌ Локация не найдена!", show_alert=True)
            return
        
        user = ensure_user(user_id)
        level = get_level(user[2])
        
        if not can_use_location(level, location_name):
            await call.answer("❌ Локация недоступна!", show_alert=True)
            return
        
        # Получаем предметы для этой локации
        available_items = []
        for item_name, item_data in SURVIVAL_ITEMS.items():
            if item_data.get("location") == location_name:
                available_items.append((item_name, item_data))
        
        if not available_items:
            await call.answer("❌ Нет предметов для этой локации", show_alert=True)
            return
        
        owned_items = get_user_survival_items(user_id)
        
        keyboard = []
        for item_name, item_data in available_items:
            if item_name in owned_items:
                keyboard.append([InlineKeyboardButton(
                    text=f"✅ {item_name} — УЖЕ КУПЛЕНО",
                    callback_data="no_action"
                )])
            else:
                # Используем короткий ID локации и короткое название предмета
                short_item = item_name.replace(" ", "_")[:20]
                keyboard.append([InlineKeyboardButton(
                    text=f"🛒 {item_name} — {item_data['price']}💰",
                    callback_data=f"surv_buy:{user_id}:{loc_id}:{short_item}"
                )])
        
        keyboard.append([InlineKeyboardButton(
            text="🔙 Назад к локациям",
            callback_data=f"survival_shop:{user_id}"
        )])
        
        await call.message.edit_text(
            f"💰 Ваш баланс: {user[1]} монет\n\n"
            f"📍 Локация: {location_name}\n\n"
            f"👇 Нажмите на предмет, чтобы купить:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
        
    except Exception as e:
        print(f"Ошибка surv_show_items: {e}")
        await call.answer(f"❌ Ошибка: {str(e)[:50]}", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("surv_buy:"))
async def surv_buy_item(call: CallbackQuery):
    try:
        parts = call.data.split(":")
        user_id = int(parts[1])
        loc_id = parts[2]
        short_item = parts[3]
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        # Восстанавливаем название локации
        location_name = LOCATION_IDS.get(loc_id)
        if not location_name:
            await call.answer("❌ Локация не найдена!", show_alert=True)
            return
        
        # Восстанавливаем название предмета
        item_name = None
        for name in SURVIVAL_ITEMS.keys():
            if name.replace(" ", "_")[:20] == short_item:
                item_name = name
                break
        
        if not item_name:
            await call.answer("❌ Предмет не найден!", show_alert=True)
            return
        
        item_data = SURVIVAL_ITEMS[item_name]
        
        user = ensure_user(user_id)
        
        if user[1] < item_data['price']:
            await call.answer(f"❌ Не хватает {item_data['price'] - user[1]} монет!", show_alert=True)
            return
        
        # Проверяем, не куплен ли уже
        owned = sql.execute(
            "SELECT 1 FROM survival_items WHERE user_id = ? AND item_name = ?",
            (user_id, item_name)
        ).fetchone()
        
        if owned:
            await call.answer("✅ У вас уже есть этот предмет!", show_alert=True)
            await surv_show_items(call)
            return
        
        # ===== ПОДТВЕРЖДЕНИЕ ПОКУПКИ =====
        # Формируем описание эффекта
        effect_text = ""
        if item_data.get('survival'):
            effect_text = "🛡️ **Защитный предмет** - защищает от урона окружающей среды"
        elif item_data.get('bonus'):
            bonus = item_data['bonus']
            if 'search_bonus' in bonus:
                effect_text = f"🔍 **Бонус:** +{bonus['search_bonus']}% к поиску животных"
            elif 'hit_bonus' in bonus:
                effect_text = f"🎯 **Бонус:** +{bonus['hit_bonus']}% к шансу попадания"
            elif 'exp_bonus' in bonus:
                effect_text = f"⭐ **Бонус:** +{bonus['exp_bonus']}% к опыту"
            else:
                effect_text = f"✨ **Бонус:** {bonus}"
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да, купить", callback_data=f"surv_confirm:{user_id}:{loc_id}:{short_item}")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data=f"surv_show:{user_id}:{loc_id}")]
        ])
        
        await call.message.edit_text(
            f"❓ **Подтверждение покупки**\n\n"
            f"📦 **{item_name}**\n"
            f"📝 {item_data['description']}\n"
            f"{effect_text}\n\n"
            f"💰 Цена: {item_data['price']} монет\n"
            f"💳 Ваш баланс: {user[1]} монет\n"
            f"💳 После покупки: {user[1] - item_data['price']} монет\n\n"
            f"📍 Локация использования: {location_name}",
            reply_markup=kb,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        print(f"Ошибка surv_buy_item: {e}")
        await call.answer(f"❌ Ошибка: {str(e)[:50]}", show_alert=True)
        
@dp.callback_query(lambda c: c.data.startswith("surv_confirm:"))
async def confirm_survival_purchase(call: CallbackQuery):
    """Подтверждение покупки предмета выживания"""
    try:
        parts = call.data.split(":")
        user_id = int(parts[1])
        loc_id = parts[2]
        short_item = parts[3]
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша покупка!", show_alert=True)
            return
        
        # Восстанавливаем данные
        location_name = LOCATION_IDS.get(loc_id)
        if not location_name:
            await call.answer("❌ Локация не найдена!", show_alert=True)
            return
        
        item_name = None
        for name in SURVIVAL_ITEMS.keys():
            if name.replace(" ", "_")[:20] == short_item:
                item_name = name
                break
        
        if not item_name:
            await call.answer("❌ Предмет не найден!", show_alert=True)
            return
        
        item_data = SURVIVAL_ITEMS[item_name]
        user = ensure_user(user_id)
        
        if user[1] < item_data['price']:
            await call.answer("❌ Не хватает монет!", show_alert=True)
            return
        
        owned = sql.execute(
            "SELECT 1 FROM survival_items WHERE user_id = ? AND item_name = ?",
            (user_id, item_name)
        ).fetchone()
        
        if owned:
            await call.answer("✅ У вас уже есть этот предмет!", show_alert=True)
            await surv_show_items(call)
            return
        
        # Покупка
        sql.execute(
            "INSERT INTO survival_items (user_id, item_name, location) VALUES (?, ?, ?)",
            (user_id, item_name, location_name)
        )
        sql.execute("UPDATE users SET coins = coins - ? WHERE user_id = ?", (item_data['price'], user_id))
        db.commit()
        
        await call.answer(f"✅ Вы купили {item_name}!", show_alert=True)
        
        await call.message.edit_text(
            f"✅ **Покупка успешна!**\n\n"
            f"📦 **{item_name}**\n"
            f"📝 {item_data['description']}\n\n"
            f"💰 Потрачено: {item_data['price']} монет\n"
            f"💳 Осталось: {user[1] - item_data['price']} монет",
            parse_mode="Markdown"
        )
        
        await asyncio.sleep(2)
        await surv_show_items(call)
        
    except Exception as e:
        print(f"Ошибка confirm_survival_purchase: {e}")
        await call.answer(f"❌ Ошибка: {str(e)[:50]}", show_alert=True)


#EJF;LEUFRIRHLIGFRO;LGRK;GKE;'RGK;SFJGPSRHGPISRHTGFFHHHHHHHHHHHHHHHHHHH

@dp.message(lambda msg: msg.text and msg.text.lower() == "тествыживание")
async def test_survival(msg: Message):
    """Тестовая команда для проверки выживания"""
    try:
        user_id = msg.from_user.id
        user = ensure_user(user_id)
        
        # Проверяем таблицу temp_shop_data
        temp_data = sql.execute("SELECT * FROM temp_shop_data WHERE user_id = ?", (user_id,)).fetchall()
        
        test_text = f"🧪 ТЕСТ ВЫЖИВАНИЯ\n\n"
        test_text += f"User ID: {user_id}\n"
        test_text += f"Баланс: {user[1]}\n"
        test_text += f"Уровень: {get_level(user[2])}\n\n"
        
        test_text += f"📊 temp_shop_data для user_id={user_id}:\n"
        if temp_data:
            for row in temp_data:
                test_text += f"  - {row}\n"
        else:
            test_text += "  (нет данных)\n\n"
        
        test_text += f"📊 survival_items для user_id={user_id}:\n"
        items = get_user_survival_items(user_id)
        if items:
            for item in items:
                test_text += f"  - {item}\n"
        else:
            test_text += "  (нет предметов)\n"
        
        await msg.answer(test_text)
        
    except Exception as e:
        log_error_detailed(e, "test_survival")
        await msg.answer(f"❌ Ошибка: {str(e)}")

# ================== НАВИГАЦИЯ ==================
@dp.callback_query(lambda c: c.data.startswith("back_to_shop"))
async def back_to_shop(call: CallbackQuery):
    """Возврат в главное меню магазина"""
    try:
        user_id = int(call.data.split(":")[1])
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваш магазин!", show_alert=True)
            return
        
        buttons = [
            [InlineKeyboardButton(text="🔫 Оружие", callback_data=f"weapons_menu:{user_id}")],
            [InlineKeyboardButton(text="🎩 Снаряжение", callback_data=f"equipment_menu:{user_id}")],
            [InlineKeyboardButton(text="⚡ Баффы", callback_data=f"buffs_menu:{user_id}")],
            [InlineKeyboardButton(text="🛡️ Выживание", callback_data=f"survival_shop:{user_id}")]  # ← ИСПРАВЛЕНО: survival_shop
        ]
        
        if is_event_active():
            buttons.append([InlineKeyboardButton(text="🎪 Ивент", callback_data="event_shop_menu")])
        
        buttons.append([InlineKeyboardButton(text="❌ Закрыть", callback_data="close_shop")])
        
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.edit_text("🏪 **Добро пожаловать в магазин!**\n\nВыберите категорию:", reply_markup=kb, parse_mode="Markdown")
    
    except Exception as e:
        await call.answer(f"❌ Ошибка: {str(e)}", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("survival_menu:"))
async def survival_menu_fix(call: CallbackQuery):
    """Фикс для старого названия survival_menu"""
    # Просто перенаправляем на survival_shop
    await survival_shop(call)

@dp.callback_query(lambda c: c.data == "close_shop")
async def close_shop(call: CallbackQuery):
    """Закрыть магазин"""
    await call.message.delete()

@dp.callback_query(lambda c: c.data == "no_action")
async def no_action(call: CallbackQuery):
    """Заглушка для неактивных кнопок"""
    await call.answer("ℹ️ Это действие недоступно", show_alert=True)

# ================== ЛОКАЦИИ ==================
@dp.message(lambda msg: msg.text and msg.text.lower() == "локации")
async def choose_location(msg: Message):
    user = ensure_user(msg.from_user.id, msg.from_user.username)
    level = get_level(user[2])
    
    buttons = []
    for name, data in LOCATIONS.items():
        available = level >= data["level"]
        status = "📍 " if user[4] == name else ""
        lock = "🔒 " if not available else ""
        level_req = f" (ур. {data['level']}+)" if not available else ""
        
        if available:
            buttons.append([InlineKeyboardButton(
                text=f"{status}{lock}{name}{level_req}",
                callback_data=f"loc_view:{msg.from_user.id}:{name}"
            )])
        else:
            buttons.append([InlineKeyboardButton(
                text=f"{lock}{name}{level_req}",
                callback_data="loc_locked"
            )])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await msg.answer(f"📍 Выберите локацию для просмотра (Ваш уровень: {level}):", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("loc_view"))
async def view_location(call: CallbackQuery):
    data_parts = call.data.split(":")
    if len(data_parts) < 3:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    owner_id = int(data_parts[1])
    location = data_parts[2]
    
    if owner_id != call.from_user.id:
        await call.answer("❌ Это не ваша локация!", show_alert=True)
        return
    
    user = ensure_user(call.from_user.id)
    level = get_level(user[2])
    
    if not can_use_location(level, location):
        await call.answer(f"❌ Эта локация доступна с уровня {LOCATIONS[location]['level']}!", show_alert=True)
        return
    
    is_event_location = (location == EVENT_LOCATION)
    animals_dict = EVENT_ANIMALS if is_event_location else LOCATIONS[location]["animals"]
    
    # Получаем статистику убийств (для ивентовой локации она может быть 0)
    stats = sql.execute("SELECT kills FROM location_stats WHERE user_id = ? AND location = ?", 
                       (call.from_user.id, location)).fetchone()
    kills = stats[0] if stats else 0
    
    # Формируем текст с животными
    animals_text = f"📍 **{location}**\n📊 Убийств в локации: {kills}\n\n"
    
    for group_name, animals_list in animals_dict.items():
        animals_text += f"**{group_name}:**\n"
        for animal in animals_list:
            trophy = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", 
                                (call.from_user.id, animal)).fetchone()
            has_animal = trophy is not None and trophy[0] > 0
            count = trophy[0] if trophy else 0
            
            mutations_data = sql.execute("SELECT mutation, count FROM trophy_mutations WHERE user_id = ? AND animal = ?",
                                         (call.from_user.id, animal)).fetchall()
            mutations_str = f" ({', '.join([m[0] for m in mutations_data])})" if mutations_data else ""
            
            if has_animal:
                animals_text += f"• {animal} - ✅ ({count}){mutations_str}\n"
            else:
                animals_text += f"• {animal} - ❌\n"
        animals_text += "\n"

     # ===== ПОДСКАЗКА ПО ОРУЖИЮ =====
    weapon_love = LOCATION_WEAPON_WEAKNESS.get(location, {}).get("love", [])
    weapon_hate = LOCATION_WEAPON_WEAKNESS.get(location, {}).get("hate", [])

    love_emojis = {"огненные": "🔥", "ледяные": "❄️", "ядовитые": "🧪", "электрические": "⚡", "тёмные": "🌑", "священные": "✨", "обычные": "⚪"}
    hate_emojis = {"огненные": "🔥", "ледяные": "❄️", "ядовитые": "🧪", "электрические": "⚡", "тёмные": "🌑", "священные": "✨", "обычные": "⚪"}

    animals_text += "\n━━━━━━━━━━━━━━━━━━━━\n"
    animals_text += "🎯 **Характеристики оружия:**\n"

    if weapon_love:
        love_str = ", ".join([f"{love_emojis.get(w, '')} {w}" for w in weapon_love])
        animals_text += f"✅ **Хорошо:** {love_str} (+15% попадание, +10% награда)\n"

    if weapon_hate:
        hate_str = ", ".join([f"{hate_emojis.get(w, '')} {w}" for w in weapon_hate])
        animals_text += f"❌ **Плохо:** {hate_str} (-20% попадание, -15% награда)\n"

    if not weapon_love and not weapon_hate:
        animals_text += "⚖️ Все типы оружия нейтральны в этой локации\n"
                
                # Кнопки (для ивентовой локации достижения не показываем)
      # Кнопки
    buttons = []
    if not is_event_location:
        buttons.append([InlineKeyboardButton(text="🏆 Достижения локации", callback_data=f"loc_ach:{call.from_user.id}:{location}")])
        # НОВАЯ КНОПКА - КОЛЛЕКЦИЯ
        buttons.append([InlineKeyboardButton(text="📦 Коллекция", callback_data=f"loc_collect:{call.from_user.id}:{location}")])
    buttons.append([InlineKeyboardButton(text="🗺️ Сменить локацию", callback_data=f"loc_change:{call.from_user.id}:{location}")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад к списку", callback_data=f"loc_list:{call.from_user.id}")])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    try:
        await call.message.edit_text(animals_text, reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        if "message is not modified" in str(e):
            await call.answer("ℹ️ Вы уже в этой локации")
        else:
            raise

@dp.callback_query(lambda c: c.data == "loc_locked")
async def loc_locked(call: CallbackQuery):
    await call.answer("❌ Эта локация недоступна на вашем уровне!", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("loc_change"))
async def change_location(call: CallbackQuery):
    data_parts = call.data.split(":")
    if len(data_parts) < 3:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    owner_id = int(data_parts[1])
    location = data_parts[2]
    
    if owner_id != call.from_user.id:
        await call.answer("❌ Это не ваша локация!", show_alert=True)
        return
    
    user = ensure_user(call.from_user.id)
    level = get_level(user[2])
    
    if not can_use_location(level, location):
        await call.answer(f"❌ Эта локация доступна с уровня {LOCATIONS[location]['level']}!", show_alert=True)
        return
    
    sql.execute("UPDATE users SET location = ? WHERE user_id = ?", (location, call.from_user.id))
    db.commit()
    
    await call.answer(f"✅ Локация изменена на {location}!", show_alert=True)
    
    # Обновляем текущее сообщение
    await view_location(call)

@dp.callback_query(lambda c: c.data.startswith("loc_list"))
async def location_list(call: CallbackQuery):
    data_parts = call.data.split(":")
    if len(data_parts) < 2:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    owner_id = int(data_parts[1])
    
    if owner_id != call.from_user.id:
        await call.answer("❌ Это не ваше меню!", show_alert=True)
        return
    
    user = ensure_user(call.from_user.id)
    level = get_level(user[2])
    
    buttons = []
    for name, data in LOCATIONS.items():
        available = level >= data["level"]
        status = "📍 " if user[4] == name else ""
        lock = "🔒 " if not available else ""
        level_req = f" (ур. {data['level']}+)" if not available else ""
        
        if available:
            buttons.append([InlineKeyboardButton(
                text=f"{status}{lock}{name}{level_req}",
                callback_data=f"loc_view:{call.from_user.id}:{name}"
            )])
        else:
            buttons.append([InlineKeyboardButton(
                text=f"{lock}{name}{level_req}",
                callback_data="loc_locked"
            )])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text(f"📍 Выберите локацию для просмотра (Ваш уровень: {level}):", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("loc_ach"))
async def location_achievements_view(call: CallbackQuery):
    data_parts = call.data.split(":")
    if len(data_parts) < 3:
        await call.answer("❌ Ошибка данных", show_alert=True)
        return
    
    owner_id = int(data_parts[1])
    location = data_parts[2]
    
    if owner_id != call.from_user.id:
        await call.answer("❌ Это не ваши достижения!", show_alert=True)
        return
    
    stats = sql.execute("SELECT kills FROM location_stats WHERE user_id = ? AND location = ?", 
                       (call.from_user.id, location)).fetchone()
    kills = stats[0] if stats else 0
    
    completed = sql.execute("SELECT achievement_type FROM location_achievements WHERE user_id = ? AND location = ? AND completed = 1",
                           (call.from_user.id, location)).fetchall()
    completed_types = [c[0] for c in completed]
    
    achievements_data = LOCATION_ACHIEVEMENTS_DATA.get(location, {})
    
    # Прогресс "90% видов"
    all_animals = []
    for animals_list in LOCATIONS[location]["animals"].values():
        all_animals.extend(animals_list)
    
    total_animals = len(all_animals)
    required_count = (total_animals * 9 + 9) // 10  # 90% округление вверх
    
    killed_animals = sql.execute("SELECT animal FROM trophies WHERE user_id = ?", (call.from_user.id,)).fetchall()
    killed_animals = [a[0] for a in killed_animals]
    killed_count = sum(1 for a in all_animals if a in killed_animals)
    
    percent = int(killed_count / total_animals * 100) if total_animals > 0 else 0
    
    # ========== ФОРМИРУЕМ ТЕКСТ ==========
    text = f"🏆 **Достижения локации: {location}**\n\n"
    text += f"📊 **Прогресс убийств:** {kills}/250\n\n"
    text += "─" * 20 + "\n\n"
    
    # Достижение 1: 90% видов
    if "all_species" in completed_types:
        text += "✅ **90% видов** - ПОЛУЧЕНО!\n"
    else:
        text += f"📌 **90% видов** - {killed_count}/{required_count} ({percent}%)\n"
        text += f"   🔸 Осталось убить: {max(0, required_count - killed_count)} новых видов\n"
    
    ach = achievements_data.get("all_species", {})
    if ach.get("status"):
        text += f"   🎁 Награда: Статус «{ach['status']}»\n"
    if ach.get("coins_reward"):
        text += f"   💰 +{ach['coins_reward']} монет\n"
    if ach.get("exp_reward"):
        text += f"   ⭐ +{ach['exp_reward']} опыта\n"
    text += "\n"
    
    # Достижение 2: 60 убийств
    if "60_kills" in completed_types:
        text += "✅ **60 убийств** - ПОЛУЧЕНО!\n"
    else:
        text += f"📌 **60 убийств** - {min(60, kills)}/60\n"
    
    ach = achievements_data.get("60_kills", {})
    if ach.get("title"):
        text += f"   🎁 Награда: Титул «{ach['title']}»\n"
    if ach.get("coins_reward"):
        text += f"   💰 +{ach['coins_reward']} монет\n"
    if ach.get("exp_reward"):
        text += f"   ⭐ +{ach['exp_reward']} опыта\n"
    text += "\n"
    
    # Достижение 3: 250 убийств
    if "250_kills" in completed_types:
        text += "✅ **250 убийств** - ПОЛУЧЕНО!\n"
    else:
        text += f"📌 **250 убийств** - {min(250, kills)}/250\n"
    
    ach = achievements_data.get("250_kills", {})
    if ach.get("quote"):
        text += f"   🎁 Награда: Цитата\n"
    if ach.get("coins_reward"):
        text += f"   💰 +{ach['coins_reward']} монет\n"
    if ach.get("exp_reward"):
        text += f"   ⭐ +{ach['exp_reward']} опыта\n"

     # Достижение 4: Полная коллекция (скин)
    if "full_collection" in completed_types:
        text += "✅ **Полная коллекция** - ПОЛУЧЕНО!\n"
    else:
        collected_count, _ = get_collection_progress(call.from_user.id, location)
        text += f"📌 **Полная коллекция** - {collected_count}/10 предметов\n"
    
    text += f"   🎁 Награда: +5000💰 +1000⭐ + скин профиля {location}\n"
    text += "\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад к локации", callback_data=f"loc_view:{call.from_user.id}:{location}")]
    ])
    
    await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data.startswith("loc_collect"))
async def location_collection(call: CallbackQuery):
    """Показать коллекционные предметы локации"""
    try:
        _, user_id, location = call.data.split(":")
        user_id = int(user_id)
        
        if user_id != call.from_user.id:
            await call.answer("❌ Это не ваша локация!", show_alert=True)
            return
        
        # Получаем все предметы игрока в этой локации
        collectibles = get_user_collectibles(user_id, location)
        
        # Получаем прогресс
        collected_count, total_count = get_collection_progress(user_id, location)
        
        # Формируем текст
        text = f"📦 **КОЛЛЕКЦИЯ ПРЕДМЕТОВ: {location}**\n\n"
        
        for group_name, items in LOCATION_COLLECTIBLES.get(location, {}).items():
            text += f"**{group_name}:**\n"
            
            # Получаем предметы игрока в этой группе
            user_items = collectibles.get(group_name, {})
            
            for item in items:
                count = user_items.get(item, 0)
                if count > 0:
                    text += f"  {item} ✅ ({count})\n"
                else:
                    text += f"  {item} ❌\n"
            text += "\n"
        
        text += f"━━━━━━━━━━━━━━━━\n"
        text += f"📊 Прогресс: {collected_count}/{total_count}\n"
        text += f"💡 Чтобы получить предметы, охотитесь в этой локации (шанс 10%)\n"
        text += f"🎁 За полную коллекцию (10/10) вы получите: +5000💰 +1000⭐ и скин профиля!"
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад к локации", callback_data=f"loc_view:{user_id}:{location}")]
        ])
        
        await call.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Ошибка location_collection: {e}")
        await call.answer("❌ Ошибка при загрузке коллекции", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("loc_back"))
async def location_back(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    
    if int(user_id) != call.from_user.id:
        await call.answer("❌ Это не ваше меню!", show_alert=True)
        return
    
    user = ensure_user(call.from_user.id)
    level = get_level(user[2])
    
    buttons = []
    for name, data in LOCATIONS.items():
        available = level >= data["level"]
        status = "📍 " if user[4] == name else ""
        lock = "🔒 " if not available else ""
        level_req = f" (ур. {data['level']}+)" if not available else ""
        
        if available:
            buttons.append([InlineKeyboardButton(
                text=f"{status}{lock}{name}{level_req}",
                callback_data=f"loc_set:{call.from_user.id}:{name}"
            )])
        else:
            buttons.append([InlineKeyboardButton(
                text=f"{lock}{name}{level_req}",
                callback_data="loc_locked"
            )])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text(f"📍 Выберите локацию (Ваш уровень: {level}):", reply_markup=kb)

# ================== СЕРИЯ ================== 
@dp.message(lambda msg: msg.text and msg.text.lower() == "серия")
async def daily_streak(msg: Message):
    """Получить награду за серию (каждые 12 часов)"""
    user = ensure_user(msg.from_user.id)
    current_streak = user[38] if len(user) > 38 else 0
    last_claim = user[39] if len(user) > 39 else 0
    now = int(time.time())
    
    streak_emoji = get_streak_emoji(current_streak)
    
    # Проверяем, можно ли получить награду
    if last_claim > 0 and (now - last_claim) < 43200:
        hours_left = (43200 - (now - last_claim)) // 3600
        minutes_left = ((43200 - (now - last_claim)) % 3600) // 60
        
        # Прогресс-бар
        elapsed = (now - last_claim)
        percent = int((elapsed / 43200) * 20)  # 20 символов в баре
        bar = "█" * percent + "░" * (20 - percent)
        
        text = f"🎯 **Ежедневная серия**\n\n"
        text += f"📅 Текущий день: {current_streak} {streak_emoji}\n\n"
        text += f"⏳ До следующей награды:\n"
        text += f"`{bar}`\n"
        text += f"⏰ {hours_left}ч {minutes_left}м\n\n"
        text += f"💡 Напишите `серия` снова через {hours_left}ч {minutes_left}м"
        
        await msg.answer(text, parse_mode="Markdown")
        return
    
    # Если можно получить награду
    success, result, streak, rewards = claim_daily_streak(msg.from_user.id)
    await msg.answer(result)
# ================== ЛОВУШКИ ==================
@dp.message(lambda msg: msg.text and msg.text.lower() in ["ловушки", "ловушка"])
async def traps_command(msg: Message):
    user = ensure_user(msg.from_user.id, msg.from_user.username)
    
    success, result = use_traps(msg.from_user.id)
    
    if not success:
        await msg.answer(result)
        return
    
    caught_animals = result
    
    if not caught_animals:
        await msg.answer("🪤 Вы поставили ловушки, но ничего не поймали.")
        return
    
    total_coins = 0
    total_exp = 0
    animals_text = "🪤 Вы поймали в ловушки:\n\n"
    
    for group, animal in caught_animals:
        if group in REWARDS:
            base_coins, base_exp = REWARDS[group]
            coins = base_coins // 2
            exp = base_exp // 2
            
            total_coins += coins
            total_exp += exp
            
            animals_text += f"• {animal} ({group}) — {coins}💰, {exp}⭐\n"
            
            trophy = sql.execute("SELECT count FROM trophies WHERE user_id = ? AND animal = ?", (msg.from_user.id, animal)).fetchone()
            if trophy:
                sql.execute("UPDATE trophies SET count = count + 1 WHERE user_id = ? AND animal = ?", (msg.from_user.id, animal))
            else:
                sql.execute("INSERT INTO trophies VALUES (?, ?, ?)", (msg.from_user.id, animal, 1))
    
    sql.execute("UPDATE users SET coins = coins + ?, exp = exp + ? WHERE user_id = ?", 
                (total_coins, total_exp, msg.from_user.id))
    
    # Проверяем достижения после использования ловушек
    new_achievements = check_achievements(msg.from_user.id)
    
    db.commit()
    
    if new_achievements:
        achievements_text = "\n\n🎉 Новые достижения:\n"
        for achievement_name in new_achievements:
            achievements_text += f"• {achievement_name}\n"
        animals_text += achievements_text
    
    animals_text += f"\n💰 Всего: {total_coins} монет, {total_exp} опыта"
    
    await msg.answer(animals_text)


# ================== ФУНКЦИЯ ОБНОВЛЕНИЯ БД ==================
def update_database():
    """Обновляет структуру базы данных при необходимости"""
    # Все колонки, которые должны быть в таблице users
    columns_to_add = [
        ("survival_hunt_count", "INTEGER DEFAULT 0"),
        ("survival_damage_count", "INTEGER DEFAULT 0"),
        ("diamond_bullet", "INTEGER DEFAULT 0"),
        ("immortality_staff", "INTEGER DEFAULT 0"),
        ("energy_drink", "INTEGER DEFAULT 0"),
        ("hunt_counter", "INTEGER DEFAULT 0"),
        ("golden_bullet", "INTEGER DEFAULT 0"),
        ("drone_target", "TEXT DEFAULT ''"),
        ("drone_expires", "INTEGER DEFAULT 0"),
        ("last_daily_gift", "INTEGER DEFAULT 0"),
        ("counterattack_streak", "INTEGER DEFAULT 0"),
        ("titan_escape_streak", "INTEGER DEFAULT 0"),
        ("trap_days_streak", "INTEGER DEFAULT 0"),
        ("last_trap_use", "INTEGER DEFAULT 0"),
        ("traps_used", "INTEGER DEFAULT 0"),
        ("heavy_traps", "INTEGER DEFAULT 0"),
        ("last_achievement_check", "INTEGER DEFAULT 0"),
        ("achievement_streak", "INTEGER DEFAULT 0"),
        ("deaths", "INTEGER DEFAULT 0"),
        ("current_title", "TEXT DEFAULT ''"),
        ("achievements_completed", "TEXT DEFAULT '{}'"),
        ("current_status", "TEXT DEFAULT ''"),
        ("current_quote", "TEXT DEFAULT ''"),
        ("daily_streak", "INTEGER DEFAULT 0"),
        ("last_daily_claim", "INTEGER DEFAULT 0"),
        ("no_cooldown_charges", "INTEGER DEFAULT 0"),
        ("profile_theme", "TEXT DEFAULT 'default'"),
        ("was_dead", "INTEGER DEFAULT 0")
    ]

    print("🔄 Проверка структуры базы данных...")
    
    for column_name, column_type in columns_to_add:
        try:
            sql.execute(f"SELECT {column_name} FROM users LIMIT 1")
            print(f"✓ Колонка {column_name} уже существует")
        except sqlite3.OperationalError:
            try:
                sql.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
                db.commit()
                print(f"✅ Добавлена колонка {column_name}")
            except Exception as e:
                print(f"❌ Ошибка при добавлении колонки {column_name}: {e}")
    
    # Проверяем существование таблиц
    tables_to_check = [
        ("survival_items", "CREATE TABLE IF NOT EXISTS survival_items (user_id INTEGER, item_name TEXT, location TEXT, UNIQUE(user_id, item_name), FOREIGN KEY (user_id) REFERENCES users(user_id))"),
        ("event_top", "CREATE TABLE IF NOT EXISTS event_top (user_id INTEGER, eggs INTEGER DEFAULT 0, PRIMARY KEY (user_id), FOREIGN KEY (user_id) REFERENCES users(user_id))")
    ]
    
    for table_name, create_sql in tables_to_check:
        try:
            sql.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
            print(f"✓ Таблица {table_name} уже существует")
        except sqlite3.OperationalError:
            try:
                sql.execute(create_sql)
                db.commit()
                print(f"✅ Создана таблица {table_name}")
            except Exception as e:
                print(f"❌ Ошибка при создании таблицы {table_name}: {e}")
    
    print("✅ Проверка структуры БД завершена")
    db.commit()

# ================== ЗАПУСК ==================
async def main():
    print("=" * 50)
    print("🔧 Обновление структуры базы данных...")
    update_database()

    print("🔄 Перенос старых трофеев...")
   # migrate_old_trophies()
    
    print("🔄 Сброс дневной статистики...")
    reset_daily_stats()

        # В начале main(), после создания таблиц
    sql.execute("DELETE FROM temp_shop_data WHERE created_at < ?", (int(time.time()) - 3600,))  # удаляем данные старше часа
    db.commit()
        
    print("🩺 Обновление здоровья игроков...")
    all_users = sql.execute("SELECT user_id FROM users").fetchall()
    for user in all_users:
        update_max_health(user[0])
    
    print("💖 Запуск автоматического восстановления здоровья...")
    health_regenerator.start_regeneration()

    # Запускаем фоновую задачу для обновления погоды
    async def weather_updater():
        while True:
            await asyncio.sleep(60)  # проверяем каждую минуту
            await update_weather()   # ← добавить await
    
    asyncio.create_task(weather_updater())

    print("🤖 Бот запущен! Ожидание сообщений...")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"👑 Админ Username: @{ADMIN_USERNAME}")
    print("=" * 50)
    print("📊 Доступные команды:")
    print("• /start - Начало работы")
    print("• Состояние - Проверить здоровье и восстановление")
    print("• Хант - Начать охоту (с кнопкой обнуления таймера за 450💰)")
    print("• Инв - Инвентарь (обновленный формат)")
    print("• Магазин - Магазин оружия и снаряжения")
    print("• Локации - Выбор локации")
    print("• Топы - Таблица лидеров")
    print("• Достижения - Ваши достижения (исправлено)")
    print("• Оформление — выбрать титул/цитату/статус")
    print("• Престиж - Получить престиж")
    print("• Ловушки - Использовать ловушки (раз в день после 00:00 Иркутск)")
    print("• Подарок - Ежедневный подарок (раз в день после 00:00 Иркутск)")
    print("• Выживание - Состояние предметов выживания")
    print("• Ивент - Информация об ивенте")
    print("• Справка - Помощь")
    print("=" * 50)
    print("🆕 НОВЫЕ ФУНКЦИИ И ИСПРАВЛЕНИЯ:")
    print("✅ Животные теперь добавляются в инвентарь при убийстве")
    print("✅ Награды (монеты и опыт) правильно начисляются")
    print("✅ Меню титулов с пагинацией (максимум 3 кнопки на страницу)")
    print("✅ ИСПРАВЛЕНИЕ: Нельзя охотиться при HP ≤ 25")
    print("✅ ИСПРАВЛЕНИЕ: Все баффы активируются только при покупке, не самопроизвольно")
    print("✅ Исправлены ошибки с животными: Бурый медведь, Белый медведь, Комодский варан")
    print("✅ Исправлена система выживания: урон ровно каждые 5 охот")
    print("✅ Привязаны правильные фразы атаки для каждого животного")
    print("✅ Убраны дублирующие фразы при контратаке (только фраза животного)")
    print("✅ Ловушки и подарок сбрасываются после 00:00 по Иркутскому времени")
    print("✅ Все админ-команды поддерживают 'алл' для всех игроков")
    print("✅ Исправлены названия животных и фразы атаки")
    print("=" * 50)
    print("🔧 Админ-команды:")
    print("• дипскип [@username|алл] - Сбросить таймер охоты")
    print("• дипмонеты <сумма> [@username|алл] - Выдать монеты")
    print("• дипопыт <сумма> [@username|алл] - Выдать опыт")
    print("• дипуровни <уровни> [@username|алл] - Выдать уровни")
    print("• дипзд <HP> [@username|алл] - Установить здоровье")
    print("• дипноль [@username|алл] - Полный сброс профиля")
    print("• дипл [@username|алл] - Сбросить ловушки")
    print("• диппод [@username|алл] - Сбросить подарок")
    print("• дипкил <кол-во> [@username|алл] - Добавить убийства")
    print("• дипжив \"животное\" <кол-во> [@username|алл] - Добавить животное")
    print("=" * 50)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        import traceback
        traceback.print_exc()
    finally:
        health_regenerator.stop_regeneration()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
