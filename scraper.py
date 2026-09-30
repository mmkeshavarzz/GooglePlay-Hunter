"""
=============================================================================
*  Project: Google Play Store Hunter & Auto Categorizer
*  Author: mm.keshavarz | Crafted by Senior Assistant
*  Features:
*    - Multi-Category App Scraper (Action, Tools, VPN, etc.)
*    - Anti-Ban Delay System (Bypassing 429 errors)
*    - NoneType Exception Handling for unrated apps
*    - 🚀 Auto-Broadcast Top Apps to Telegram!
=============================================================================
"""

import os
import requests
import time
import random
from google_play_scraper import search

# ==============================================================================
# 🎯 دسته‌بندی‌های رسمی گوگل‌پلی
# ==============================================================================
OFFICIAL_CATEGORIES = [
    # 📱 اپلیکیشن‌ها
    "ART_AND_DESIGN", "AUTO_AND_VEHICLES", "BEAUTY", "BOOKS_AND_REFERENCE", 
    "BUSINESS", "COMICS", "COMMUNICATION", "DATING", "EDUCATION", "ENTERTAINMENT", 
    "EVENTS", "FINANCE", "FOOD_AND_DRINK", "HEALTH_AND_FITNESS", "HOUSE_AND_HOME", 
    "LIFESTYLE", "MAPS_AND_NAVIGATION", "MEDICAL", "MUSIC_AND_AUDIO", 
    "NEWS_AND_MAGAZINES", "PARENTING", "PERSONALIZATION", "PHOTOGRAPHY", 
    "PRODUCTIVITY", "SHOPPING", "SOCIAL", "SPORTS", "TOOLS", "TRAVEL_AND_LOCAL", 
    "VIDEO_PLAYERS", "WEATHER",
    # 🎮 بازی‌ها
    "GAME_ACTION", "GAME_ADVENTURE", "GAME_ARCADE", "GAME_BOARD", "GAME_CARD", 
    "GAME_CASINO", "GAME_CASUAL", "GAME_EDUCATIONAL", "GAME_MUSIC", "GAME_PUZZLE", 
    "GAME_RACING", "GAME_ROLE_PLAYING", "GAME_SIMULATION", "GAME_SPORTS", "GAME_STRATEGY"
]

MAX_RESULTS_PER_CATEGORY = 30

# =============================================================================
# 🚀 ارسال به تلگرام
# =============================================================================
def send_to_telegram(category_name, top_apps, new_apps):
    bot_token = os.environ.get("TELEGRAM_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL")

    if not bot_token or not channel_id:
        print("⚠️ توکن تلگرام یا آیدی کانال تنظیم نیست!")
        return

    # 🛡️ حل باگ NoneType: استفاده از (app.get('score') or 0)
    premium_top = [app for app in top_apps if (app.get('score') or 0) >= 4.0][:10]
    premium_new = [app for app in new_apps if (app.get('score') or 0) >= 4.0][:10]

    if not premium_top and not premium_new:
        print(f"👻 برای دسته {category_name} اپلیکیشن بالای 4 ستاره پیدا نشد!")
        return

    msg = f"🗂 **Category:** #{category_name.replace('_', '')}\n"
    msg += f"🔥 **Top Premium Picks (⭐️ 4.0+)**\n"
    msg += f"━━━━━━━━━━━━━━━━━━\n\n"

    if premium_top:
        msg += f"🏆 **Top 10 Best Apps:**\n"
        for idx, app in enumerate(premium_top, 1):
            title = app.get('title', 'Unknown')
            score = app.get('score') or 0
            app_id = app.get('appId', '')
            play_link = f"https://play.google.com/store/apps/details?id={app_id}"
            msg += f"{idx}. **[{title}]({play_link})** (⭐ {score:.1f})\n"
        msg += "\n"

    if premium_new:
        msg += f"✨ **Top 10 New Releases:**\n"
        for idx, app in enumerate(premium_new, 1):
            title = app.get('title', 'Unknown')
            score = app.get('score') or 0
            app_id = app.get('appId', '')
            play_link = f"https://play.google.com/store/apps/details?id={app_id}"
            msg += f"{idx}. **[{title}]({play_link})** (⭐ {score:.1f})\n"
        msg += "\n"

    msg += f"━━━━━━━━━━━━━━━━━━\n"
    msg += f"🤖 *Auto-Hunted with ❤️ by Our GitHub Bot*"

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": channel_id,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ دسته‌بندی {category_name} به تلگرام شلیک شد! 🎯")
        else:
            print(f"❌ خطای تلگرام. کد: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطای ارسال به تلگرام برای {category_name}: {e}")

# =============================================================================
# 🕵️‍♂️ موتور اصلی جستجو
# =============================================================================
def main():
    print("🕵️‍♂️ در حال نفوذ به سرورهای گوگل برای استخراج اپلیکیشن‌ها...")
    os.makedirs("categories", exist_ok=True)
    
    for category in OFFICIAL_CATEGORIES:
        print(f"🔍 جستجو برای: {category}...")
        try:
            top_results = search(
                category,
                lang="en",
                country="us",
                n_hits=MAX_RESULTS_PER_CATEGORY
            )
            
            new_results = search(
                f"{category} new",
                lang="en",
                country="us",
                n_hits=MAX_RESULTS_PER_CATEGORY
            )
            
            send_to_telegram(category, top_results, new_results)
            
            # 🛡️ حل باگ ۴۲۹ (Rate Limit): استراحت تصادفی بین 4 تا 7 ثانیه تا گوگل شک نکنه
            sleep_time = random.uniform(4.0, 7.0)
            print(f"💤 استراحت برای {sleep_time:.1f} ثانیه...")
            time.sleep(sleep_time)
                
        except Exception as e:
            print(f"❌ خطا در استخراج {category}: {e}")

    print("🎉 عملیات به پایان رسید! گوگل با موفقیت غارت شد. 😎")

if __name__ == "__main__":
    main()
