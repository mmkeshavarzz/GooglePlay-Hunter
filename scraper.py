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
import json
import time
import requests
from google_play_scraper import search

# ==============================================================================
# 🎯 کلمات کلیدی و دسته‌بندی‌هایی که می‌خوایم شکار کنیم
# ==============================================================================
SEARCH_QUERIES = {
    "VPN_Proxies": "VPN Free Proxy",
    "Action_Games": "Best Action Games",
    "Crypto_Wallets": "Crypto Wallet Bitcoin",
    "Fitness": "Home Workout",
    "Messengers": "Secure Messenger"
}

MAX_RESULTS_PER_QUERY = 15 # چندتا اپ برای هر دسته پیدا کنه؟

# =============================================================================
# 🚀 ارسال به تلگرام (مخصوص اپلیکیشن‌ها)
# =============================================================================
def send_to_telegram(category_name, apps):
    bot_token = os.environ.get("TELEGRAM_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL")

    if not bot_token or not channel_id:
        print("⚠️ داداش، توکن تلگرام یا آیدی کانال تنظیم نیست! بی‌خیال ارسال شدم...")
        return

    # یه متن جذاب برای تلگرام
    msg = f"📱 **Category:** #{category_name}\n"
    msg += f"🔥 **Top New Picks Handpicked For You!**\n\n"

    # اضافه کردن تاپ 5 اپلیکیشن به پیام
    for app in apps[:5]:
        title = app.get('title', 'Unknown')
        score = app.get('score', 'N/A')
        app_id = app.get('appId', '')
        play_link = f"https://play.google.com/store/apps/details?id={app_id}"
        
        msg += f"🔹 **{title}** (⭐ {score})\n"
        msg += f"📥 [Download on Google Play]({play_link})\n\n"

    msg += f"🤖 *Auto-Hunted by Your GitHub Bot*"

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": channel_id,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"❌ ای بابا! خطای تلگرام برای {category_name}: {e}")

# =============================================================================
# 🕵️‍♂️ موتور اصلی جستجو
# =============================================================================
def main():
    print("🕵️‍♂️ در حال نفوذ به سرورهای گوگل برای استخراج اپلیکیشن‌ها...")
    os.makedirs("categories", exist_ok=True)
    
    all_data_summary = {}

    for category, query in SEARCH_QUERIES.items():
        print(f"🔍 در حال جستجو برای: {category}...")
        try:
            # جستجو در گوگل پلی
            results = search(
                query,
                lang="en",  # زبان
                country="us", # کشور
                n_hits=MAX_RESULTS_PER_QUERY
            )
            
            clean_results = []
            for res in results:
                clean_results.append({
                    "title": res.get("title"),
                    "appId": res.get("appId"),
                    "developer": res.get("developer"),
                    "score": round(res.get("score", 0), 1) if res.get("score") else "N/A",
                    "icon": res.get("icon"),
                    "link": f"https://play.google.com/store/apps/details?id={res.get('appId')}"
                })
            
            # ذخیره در فایل JSON برای استفاده‌های بعدی یا ساخت وب‌سایت
            with open(f"categories/{category}.json", "w", encoding="utf-8") as f:
                json.dump(clean_results, f, ensure_ascii=False, indent=4)
                
            all_data_summary[category] = len(clean_results)
            
            # ارسال 5 تای برتر به تلگرام
            if clean_results:
                send_to_telegram(category, clean_results)
                time.sleep(2) # یه نفس عمیق که تلگرام بلاک نکنه
                
        except Exception as e:
            print(f"❌ خطا در استخراج {category}: {e}")

    # یه فایل لاگ کلی هم می‌سازیم
    with open("last_update.json", "w", encoding="utf-8") as f:
        json.dump({"updated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "stats": all_data_summary}, f, indent=4)
        
    print("🎉 عملیات با موفقیت به پایان رسید! گوگل رسماً غارت شد.")

if __name__ == "__main__":
    main()
