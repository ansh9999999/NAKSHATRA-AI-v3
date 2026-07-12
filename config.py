import os

# ===========================
# PROJECT
# ===========================

PROJECT_NAME = "NAKSHATRA AI v3"
VERSION = "3.0"

# ===========================
# DELTA API
# ===========================

BASE_URL = "https://api.india.delta.exchange/v2"

DELTA_API_KEY = os.getenv("DELTA_API_KEY")
DELTA_API_SECRET = os.getenv("DELTA_API_SECRET")

# ===========================
# TELEGRAM
# ===========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ===========================
# SYMBOLS
# ===========================

BTC_SYMBOL = "BTCUSD"
ETH_SYMBOL = "ETHUSD"

# ===========================
# TIMEFRAME
# ===========================

TIMEFRAME = "5m"

# ===========================
# SIGNAL SETTINGS
# ===========================

MIN_CONFIDENCE = 85

VOLUME_MULTIPLIER = 1.5

ATR_MULTIPLIER = 1.20

SCAN_INTERVAL = 300
