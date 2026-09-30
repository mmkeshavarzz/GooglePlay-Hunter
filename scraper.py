"""
=============================================================================
*  Project: Google Play Store Hunter & Auto Categorizer
*  Author: mm.keshavarz | Crafted by Senior Assistant
*  Features:
*    - Multi-Category App Scraper (Action, Tools, VPN, etc.)
*    - Dynamic Data Extraction (Title, Rating, Installs, Direct Link)
*    - Clean folder structuring (JSON/Markdown)
*    - 🚀 Auto-Broadcast Top Apps to Telegram!
=============================================================================
"""

import os
import requests

# ==============================================================================
# 🎯 دسته‌بندی‌های رسمی گوگل‌پلی (بیش از 30 دسته اصلی بازی و اپلیکیشن)
# ==============================================================================
# 💡 نکته سینیور: تو پایتون اگه از کتابخونه google_play_scraper استفاده می‌کنی، 
# می‌تونی از ماژول Category یا همین اسم‌های استاندارد برای جستجوی دقیق‌تر استفاده کنی!
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

MAX_RESULTS_PER_CATEGORY = 30 # یه ذره بیشتر می‌گیریم که بعد از فیلتر، حداقل 10 تا بمونه!

# =============================================================================
# 🚀 ارسال به تلگرام (مخصوص اپلیکیشن‌های بالای ۴ ستاره و خفن)
# =============================================================================
def send_to_telegram(category_name, top_apps, new_apps):
    """
    تابع ارسال پیام به تلگرام. 
    توجه: اپلیکیشن‌هایی به این تابع پاس داده می‌شن که از قبل تو اسکریپت اصلی 
    فیلتر شدن (مثلا فقط بالای 4 ستاره هستن).
    """
    bot_token = os.environ.get("TELEGRAM_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL")

    if not bot_token or not channel_id:
        print("⚠️ داداش، توکن تلگرام یا آیدی کانال تنظیم نیست! من چطوری پیام بفرستم آخه؟ 🤷‍♂️")
        return

    # فیلتر کردن اپ‌هایی که امتیازشون بالای 4 هست (محض اطمینان مضاعف)
    premium_top = [app for app in top_apps if app.get('score', 0) >= 4.0][:10]
    premium_new = [app for app in new_apps if app.get('score', 0) >= 4.0][:10]

    # اگه هیچ اپی پیدا نشد، ضایع بازی در نیاریم و پیام خالی نفرستیم!
    if not premium_top and not premium_new:
        print(f"👻 برای دسته {category_name} هیچ اپلیکیشن بالای 4 ستاره‌ای پیدا نشد! عبور می‌کنیم...")
        return

    # یه متن جذاب و لاکچری برای تلگرام
    msg = f"🗂 **Category:** #{category_name.replace('_', '')}\n"
    msg += f"🔥 **Top Premium Picks (⭐️ 4.0+)**\n"
    msg += f"━━━━━━━━━━━━━━━━━━\n\n"

    # بخش اول: 10 اپلیکیشن برتر کلی
    if premium_top:
        msg += f"🏆 **Top 10 Best Apps:**\n"
        for idx, app in enumerate(premium_top, 1):
            title = app.get('title', 'Unknown')
            score = app.get('score', 'N/A')
            app_id = app.get('appId', '')
            play_link = f"https://play.google.com/store/apps/details?id={app_id}"
            
            msg += f"{idx}. **[{title}]({play_link})** (⭐ {score:.1f})\n"
        msg += "\n"

    # بخش دوم: 10 اپلیکیشن برتر جدید
    if premium_new:
        msg += f"✨ **Top 10 New Releases:**\n"
        for idx, app in enumerate(premium_new, 1):
            title = app.get('title', 'Unknown')
            score = app.get('score', 'N/A')
            app_id = app.get('appId', '')
            play_link = f"https://play.google.com/store/apps/details?id={app_id}"
            
            msg += f"{idx}. **[{title}]({play_link})** (⭐ {score:.1f})\n"
        msg += "\n"

    msg += f"━━━━━━━━━━━━━━━━━━\n"
    msg += f"🤖 *Auto-Hunted with ❤️ by Our GitHub Bot*"

    # ارسال نهایی به تلگرام
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": channel_id,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True # پیش‌نمایش لینک‌ها رو می‌بندیم که پیام شلوغ نشه
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ بوم! دسته‌بندی {category_name} با موفقیت به تلگرام شلیک شد! 🎯")
        else:
            print(f"❌ ای بابا! تلگرام ناز کرد. کد خطا: {response.status_code}")
            
    except Exception as e:
        print(f"❌ وایسا ببینم... یه خطای عجیب برای {category_name} پیش اومد: {e}")


# =============================================================================
# 🕵️‍♂️ موتور اصلی جستجو
# =============================================================================
# این بخش رو جایگزین تابع main قبلی کن
from google_play_scraper import search, Sort # این ایمپورت ها رو یادت نره

def main():
    print("🕵️‍♂️ در حال نفوذ به سرورهای گوگل برای استخراج اپلیکیشن‌ها...")
    os.makedirs("categories", exist_ok=True)
    
    all_data_summary = {}

    # اینجا دیگه از OFFICIAL_CATEGORIES استفاده می‌کنیم
    for category in OFFICIAL_CATEGORIES:
        print(f"🔍 در حال جستجو برای: {category}...")
        try:
            # ۱. گرفتن برنامه‌های برتر
            top_results = search(
                category,
                lang="en",
                country="us",
                n_hits=MAX_RESULTS_PER_CATEGORY
            )
            
            # ۲. گرفتن برنامه‌های جدید (با تغییر مرتب‌سازی)
            new_results = search(
                category,
                lang="en",
                country="us",
                n_hits=MAX_RESULTS_PER_CATEGORY,
                sort=Sort.NEWEST # برای گرفتن جدیدترین ها
            )
            
            # اینجا می‌تونی دیتای تمیز رو استخراج کنی (مثل کد قبلیت)
            # و بعد بفرستی برای تلگرام:
            send_to_telegram(category, top_results, new_results)
            import time
            time.sleep(2) # یه نفس عمیق
                
        except Exception as e:
            print(f"❌ خطا در استخراج {category}: {e}")

    print("🎉 عملیات با موفقیت به پایان رسید! گوگل رسماً غارت شد.")

if __name__ == "__main__":
    main()

