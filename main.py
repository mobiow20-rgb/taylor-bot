import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# توکن امن و جدید خودت رو اینجا جایگزین کن
BOT_TOKEN = "8812988037:AAF_Y3QorclQSleYqTbWmrcWjVk-jzEaU0Q"

# دیتابیس آلبوم‌ها و آهنگ‌ها
ALBUMS = {
    "TS ★": [
        "CQACAgIAAxkBAAMhajAhy8BOat3XaqAw4TFBJaNw-N4AAgUHAAKlTulJtvemcHJHzKg8BA",
        "CQACAgIAAxkBAAMjajAip7WJT-EeEN9DiEgHJPiJTl0AAgYHAAKlTulJdwRu_645p8Q8BA",
        "CQACAgIAAxkBAAMyajAnSXuQXA07etmVdUVDARPLQsMAAgcHAAKlTulJ5a5BPT8L_kU8BA",
        "CQACAgIAAxkBAAM0ajAniNFVsxLrgotHKn1HqB3WJWEAAggHAAKlTulJd9x1tdmLrcY8BA",
        "CQACAgIAAxkBAAM2ajAno5cT1uJfv_IMJUW3MHjFUYQAAgkHAAKlTulJfD1jUdc_vJA8BA",
        "CQACAgIAAxkBAAM4ajAnu0dE7Vau54aPWz_SN8zFiqgAAgoHAAKlTulJGkW-CZOshTQ8BA",
        "CQACAgIAAxkBAAM6ajAn04_tCAABdrQFwqz4RahZ3yFTAAILBwACpU7pSTNPIi6YfIzQPAQ",
        "CQACAgIAAxkBAAM8ajAn7ypf48bLNJYRNRXJbei1HrIAAgwHAAKlTulJA_m1JrcAAacDPAQ",
        "CQACAgIAAxkBAAM-ajAoH_PHMiJxItfXRfs1ENRkJP8AAg0HAAKlTulJvWiav3V1Byw8BA",
        "CQACAgIAAxkBAANAajAoMMY-OivLe85qA2RF5G-Lzz8AAg4HAAKlTulJDFS49CEJ7J88BA",
        "CQACAgIAAxkBAANCajAoQc2KvN4U0bO_pygDN87DzXcAAg8HAAKlTulJn1O4javZdRU8BA",
        "CQACAgIAAxkBAANEajAoYOOwV2h3uqymD8rISvyLlYAAAhAHAAKlTulJvfA700OrTQI8BA",
        "CQACAgIAAxkBAANEajAoYOOwV2h3uqymD8rISvyLlYAAAhAHAAKlTulJvfA700OrTQI8BA",
        "CQACAgIAAxkBAANJajAok6Z_CE1C4UEoDKgk4U9fWXoAAhIHAAKlTulJGAyDaEhW9lc8BA",
        "CQACAgIAAxkBAANLajAoqFND6-prG4wSbJwME3GokIYAAhMHAAKlTulJYZw2Xgw6udo8BA"
    ], 
    
    "FEARLESS ★": [
        "CQACAgIAAxkBAANjajAqwOMOWUVmnL8Kuk7qeauqxtgAAsReAAJBLiBLRf6KvvmTFGM8BA",
        "CQACAgIAAxkBAANlajArK2yAvFtWf2hYoFoJe2F6kgkAAmVtAAKwfThLenekJOYjGv48BA",
        "CQACAgIAAxkBAANnajAvoT4Zd1A0l8xoY-9mp0cnOaoAAglYAAJ-SFhJpYK-tEiCJEs8BA",
        "CQACAgIAAxkBAANpajAvtsryd5QkSMfrQUVkEzEgJc0AAhV0AAIbJvBJVxnMQiViWbk8BA",
        "CQACAgIAAxkBAANrajAv-N4HKDde6AFX8AFkEFUHvEoAArlhAAL5W7lK_AqbzyNUzRE8BA",
        "CQACAgIAAxkBAANuajAwtr1pCPw4XqXTAAHpwdyDcv0aAAIDWAACfkhYSSNoYI63yFWdPAQ",
        "CQACAgIAAxkBAANwajAw5AABzbb-z4dFBb_pHL3o10EMAAJ6cwACv9n4SbPMXWzGSblMPAQ",
        "CQACAgIAAxkBAANyajAw952p7Ne6EzfZlLkCs_3BglEAAntzAAK_2fhJI-gpIPxx7VY8BA",
        "CQACAgIAAxkBAAN0ajAxEyBFHo3gc-iLf0dgErMaxikAAhZ0AAIbJvBJqy4pFyVWHjQ8BA",
        "CQACAgIAAxkBAAN2ajAxbRtAhuJXby4UsInLIMWpSZ8AApJqAAJSkvlKDvJ2MByLmiM8BA",
        "CQACAgIAAxkBAAN4ajAxti7Ntv_ojdtW7ttga2_Dn1gAAmOAAAInzuFJ2k90fS1Byp08BA",
        "CQACAgIAAxkBAAN6ajAxzx7Tjg6O8fVQ7gABvnt9OQefAAJ-cwACv9n4SSh8dvatvzN-PAQ",
        "CQACAgIAAxkBAAN8ajAx4FZZKTkXkbOVjSzit22qWlcAAn9zAAK_2fhJyq--0f7s1jU8BA",
        "CQACAgIAAxkBAAN-ajAx9PD6YME8b-WJsTBSr4cxOgQAAnVzAAK_2fhJRXhcafZutKA8BA",
        "CQACAgIAAxkBAAOAajAyCrYUMs-uSddCXgT7D7t3gVwAAlZ6AAL8DuFJicuI486zmtQ8BA",
        "CQACAgIAAxkBAAOCajAyJZMMLIoL6HU2JF9NMp6irOgAAnZzAAK_2fhJ_qbH61hEdMY8BA",
        "CQACAgIAAxkBAAOEajAyOGBAxelpWDBAlIu-OHeaeaMAAndzAAK_2fhJ_NmD1pzhWBk8BA",
        "CQACAgIAAxkBAAOGajAyS2omC7ofi8xVdel3Az6MJFIAAnhzAAK_2fhJRWn9cSvO1js8BA",
        "CQACAgIAAxkBAAOIajAyXEPAzRvXlCBDS8LYkRIx5mwAAhl0AAIbJvBJuoI-xssxCf08BA"
    ],

    "SPEAK NOW ★": [
        "CQACAgIAAxkBAAOlajAzY5-9hMFH5L5wfvse0BrXdHoAAvR1AAIGmgFK9pgTAd4pCt48BA",
        "CQACAgIAAxkBAAOnajAzeYSlxm2ezoketYWPQTH7_sEAAohmAAKe9rhIR08JMlKLPQg8BA",
        "CQACAgIAAxkBAAOpajAzi4Dt6QfDGgWOwkr19kdgV18AAlZsAAJWmyBKDLK0FlfR5Q48BA",
        "CQACAgIAAxkBAAOrajAz2fAq9bFRqCSHxw6o5FbfFawAAh1cAAJQOchK1MJ56DOPz7s8BA",
        "CQACAgIAAxkBAAOtajAz8L6ZCAxwdaFb4U8FapuaKQoAAmJkAAIBOThLfr2OFxhdngABPAQ",
        "CQACAgIAAxkBAAOvajA0AnpqaSxy2HaFT_S6mIoPLJ8AAgdkAALtDRhLZ6eVXUWtaC48BA",
        "CQACAgIAAxkBAAOxajA0EtTyoKZmGSMGSu4scfC5GnAAAntyAAJ1glFLtfCHVHCk7IU8BA",
        "CQACAgIAAxkBAAO1ajA1nkitsQHI5Hgt6sib10iSIlQAAjpbAALR9ilIjJSCXwcjCyE8BA",
        "CQACAgIAAxkBAAO3ajA10MRIbTxxzi69dAnfOmcM_-QAAj1lAAJ75NhKNwABWjccQvJNPAQ",
        "CQACAgIAAxkBAAO5ajA146AdbKVuCfxJYP3CFSSpfSoAAg9zAAJto-hJd_ah-juOev88BA",
        "CQACAgIAAxkBAAO7ajA19zQRh6J6Rc939r8mHAIV9_gAAvt1AAJb6jhJQAe1-5MFAo08BA",
        "CQACAgIAAxkBAAO9ajA2C4_sma_k8Ci4fMXryz02lmAAAgJ3AAK8_rlIhqAevkek5K08BA",
        "CQACAgIAAxkBAAO_ajA2G2QyuhGaBbv28tCU7IYTzp0AApFrAAJcYqFIMOhGGr9DuxE8BA",
        "CQACAgIAAxkBAAPBajA2LPuen-5Hmtc1wrMiBLXmU2wAAqOFAALIn7hLgPWk9IVDEiA8BA",
        "CQACAgIAAxkBAAPDajA2Qn5CNne2yxG5P3phfa5-O_MAAv11AAJb6jhJBT5tSjpjyQ08BA",
        "CQACAgIAAxkBAAPFajA2Vi75lUTFpu_lg0AT_5jJFE8AAg5zAAJto-hJ7kbGxfY6ctI8BA",
        "CQACAgIAAxkBAAPHajA2bL3c3EBquaZMCzm-oEiyp8kAAuBsAAJHugABSR0EH-B0b2LxPAQ",
        "CQACAgIAAxkBAAPJajA2iZS8jzVbjph5VbZD09AuCJUAAmdrAAK7Y-hKRv5DdWiirZ48BA"
    ],

    "RED ★": [
        "CQACAgIAAxkBAAPkajGB91fDxyHlFzYZlOsG0JddFIQAAq9qAAKt1VlLLWiOY-heFuU8BA",
        "CQACAgIAAxkBAAPmajGCfYAEEHd3qEFsFASHJpWST8cAAvxhAAJdJjhJ3cGPPpbB_ws8BA",
        "CQACAgIAAxkBAAPoajGClFSNaYVASbn8AZFhVPvGR10AAnpgAALD7JlLNAo89ErY7r88BA" ,
        "CQACAgIAAxkBAAIBFmoysuGYxCk3u2qWsiMLqwULMagaAALYZQACFCMgSRqhEKfpR8vlPAQ" ,
        "CQACAgIAAxkBAAIBGGoysxEEQsoobPEb9kucq-po3G5FAAL2XAACphEoSouwaask0dFrPAQ" ,
        "CQACAgIAAxkBAAIBGmoysyg_pmk6YOg1-pVqV7qqEcVGAAICWAACfkhYSd73rDamkcOHPAQ",
        "CQACAgIAAxkBAAIBHGoysz_skDfYn5SMFAABjvj2OkSY2wACDmEAAoqvoErIA-vSxEshSzwE",
        "CQACAgIAAxkBAAIBHmoys1XUuK9OueK1iQFwt7AT2bsrAAKJWQAC-0VBSfLaUQRBkngRPAQ",
        "CQACAgIAAxkBAAIBIGoys2m5Ga3pp07nqFMHOLkQTloLAAIPYQACiq-gSu0hgYK3_Yj-PAQ",
        "CQACAgIAAxkBAAIBImoys31HhOReTiE0fmkU-Na0eDPRAAIQYQACiq-gSmdcsubiYFwjPAQ",
        "CQACAgIAAxkBAAIBJGoys5Be_EpUIT1vVMS7JumdSGMoAAKHYQACNrmISurW8H3MYuq0PAQ",
        "CQACAgIAAxkBAAIBJmoys6Wv3slv4hH8wiGUNhmRvr0rAAISYQACiq-gSiyj2e3wQ2r2PAQ",
        "CQACAgIAAxkBAAIBKGoys7pzifUVOCEGttMWFaff_qX_AAIRYQACiq-gSoEUtTaH2oPxPAQ",
        "CQACAgIAAxkBAAIBKmoys9rr1U9Ackte3fi8voYWN1izAAIQZQACbaQQSejO1q24MXbyPAQ",
        "CQACAgIAAxkBAAIBLGoys_LkQngiN1oJ8CZ-Rgs9hqWWAAITYQACiq-gSmx29kzvrJ_BPAQ",
        "CQACAgIAAxkBAAIBLmoytBTuJaZOkewXWZ9VBZcac0VgAAJ7YAACw-yZS-_n58D-u3OoPAQ",
        "CQACAgIAAxkBAAIBMGoytCy5pojMD8IH1xNnzdApZX3mAAKTeQACEX6xSISgTWELsrzjPAQ",
        "CQACAgIAAxkBAAIBMmoytET9okNvOn2R483CEmNg9wAB3wAClXkAAhF-sUiOEZoa1W2IdDwE",
        "CQACAgIAAxkBAAIBNmoytfEaxD1rs7l6ofidMhbH8uZ7AAKYeQACEX6xSHYt7BRzF1yMPAQ",
        "CQACAgIAAxkBAAIBOGoytioxQ3V1mvh8Uj6NrquBQacsAAKZeQACEX6xSDn4svz1LL8lPAQ",
        "CQACAgIAAxkBAAIBOmoytj3NnfA71-JVkWT724eqhPcjAAKaeQACEX6xSPU3lJdVkUHWPAQ",
        "CQACAgIAAxkBAAIBNGoytFzxB_hBecqWt4uis4yJaiBkAAKXeQACEX6xSECHzptPL1JUPAQ" 
    ],
    "1989 ★": ["آیدی_فایل_اینجا"],
    "REPUTATION ★": ["آیدی_فایل_اینجا"],
    "LOVER ★": ["آیدی_فایل_اینجا"],
    "FOLKLORE ★": ["آیدی_فایل_اینجا"],
    "EVERMORE ★": ["آیدی_فایل_اینجا"],
    "MIDNIGHTS ★": ["آیدی_فایل_اینجا"],
    "TTPD ★": ["آیدی_فایل_اینجا"],
    "TLOSG ★": ["آیدی_فایل_اینجا"],
    "FEARLESS TV ★": ["آیدی_فایل_اینجا"],
    "RED TV ★": ["آیدی_فایل_اینجا"],
    "SPEAK NOW TV ★": ["آیدی_فایل_اینجا"],
    "1989 TV ★": ["آیدی_فایل_اینجا"],
    
    # مینی آلبوم‌ها
    "holiday": ["آیدی_فایل_اینجا"],
    "rhapsody": ["آیدی_فایل_اینجا"],
    "beautiful_eyes": ["آیدی_فایل_اینجا"],
    
    # آلبوم‌های لایو
    "speak_now_live": ["آیدی_فایل_اینجا"],
    "clear_channel": ["آیدی_فایل_اینجا"],
    "itunes_soho": ["آیدی_فایل_اینجا"],
    "1989_live": ["آیدی_فایل_اینجا"],
    "rep_tour": ["آیدی_فایل_اینجا"],
    "lover_paris": ["آیدی_فایل_اینجا"],
    "long_pond": ["آیدی_فایل_اینجا"],
    "eras_tour": ["آیدی_فایل_اینجا"]
}

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎵 آلبوم‌های موسیقی تیلور", callback_data="music_menu")]
    ])

def get_albums_keyboard():
    return InlineKeyboardMarkup([
        # آلبوم‌های اصلی
        [InlineKeyboardButton("Taylor Swift ★", callback_data="TS ★"), InlineKeyboardButton("Fearless ★", callback_data="FEARLESS ★")],
        [InlineKeyboardButton("Speak Now ★", callback_data="SPEAK NOW ★"), InlineKeyboardButton("Red ★", callback_data="RED ★")],
        [InlineKeyboardButton("1989 ★", callback_data="1989 ★"), InlineKeyboardButton("reputation ★", callback_data="REPUTATION ★")],
        [InlineKeyboardButton("Lover ★", callback_data="LOVER ★"), InlineKeyboardButton("folklore ★", callback_data="FOLKLORE ★")],
        [InlineKeyboardButton("evermore ★", callback_data="EVERMORE ★"), InlineKeyboardButton("Midnights ★", callback_data="MIDNIGHTS ★")],
        [InlineKeyboardButton("The Tortured Poets Department ★", callback_data="TTPD ★")],
        [InlineKeyboardButton("The Life of a Showgirl ★", callback_data="TLOSG ★")],
        [InlineKeyboardButton("Fearless (TV) ★", callback_data="FEARLESS TV ★"), InlineKeyboardButton("Red (TV) ★", callback_data="RED TV ★")],
        [InlineKeyboardButton("Speak Now (TV) ★", callback_data="SPEAK NOW TV ★"), InlineKeyboardButton("1989 (TV) ★", callback_data="1989 TV ★")],
        
        # تیتر مینی آلبوم‌ها
        [InlineKeyboardButton("👇 --- مینی آلبوم‌های تیلور --- 👇", callback_data="ignore")],
        [InlineKeyboardButton("Holiday Collection", callback_data="holiday"), InlineKeyboardButton("Rhapsody Originals", callback_data="rhapsody")],
        [InlineKeyboardButton("Beautiful Eyes", callback_data="beautiful_eyes")],
        
        # تیتر آلبوم‌های لایو
        [InlineKeyboardButton("👇 --- آلبوم‌های لایو --- 👇", callback_data="ignore")],
        [InlineKeyboardButton("Speak Now World Tour", callback_data="speak_now_live"), InlineKeyboardButton("Clear Channel 2008", callback_data="clear_channel")],
        [InlineKeyboardButton("iTunes Live from SoHo", callback_data="itunes_soho"), InlineKeyboardButton("1989 World Tour", callback_data="1989_live")],
        [InlineKeyboardButton("reputation Stadium Tour", callback_data="rep_tour"), InlineKeyboardButton("Lover (Live from Paris)", callback_data="lover_paris")],
        [InlineKeyboardButton("folklore: long pond studio", callback_data="long_pond")],
        [InlineKeyboardButton("The Eras Tour - Live", callback_data="eras_tour")],
        
        # دکمه بازگشت
        [InlineKeyboardButton("🔙 برگشت به منوی اصلی", callback_data="back_to_main")]
    ])

# --- تابع جدید برای ارسال در پس‌زمینه ---
async def send_album_in_background(chat_id, album_choice, bot):
    for file_id in ALBUMS[album_choice]:
        if file_id == "آیدی_فایل_اینجا":
            continue
        try:
            await bot.send_audio(chat_id=chat_id, audio=file_id)
            # یک مکث نیم ثانیه‌ای طلایی برای جلوگیری از بلاک شدن توسط تلگرام
            await asyncio.sleep(0.5) 
        except Exception as e:
            print(f"Error sending audio: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name
    welcome_text = (
        f"{first_name} به چنل آرشیو میس امریکانا خوش آمدید 🤍\n\n"
        "یکی از گزینه های زیر رو برای ادامه انتخاب کن 👇"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice = query.data 
    
    if choice == "ignore":
        return
        
    elif choice == "back_to_main":
        first_name = update.effective_user.first_name
        text = f"{first_name} به چنل آرشیو میس امریکانا خوش آمدید 🤍\n\nیکی از گزینه های زیر رو برای ادامه انتخاب کن 👇"
        await query.edit_message_text(text=text, reply_markup=get_main_menu_keyboard())
        
    elif choice == "music_menu":
        text = "به پلی‌لیست کامل تیلور سوییفت خوش اومدی! 🎸\nیک آلبوم رو برای پخش انتخاب کن:"
        await query.edit_message_text(text=text, reply_markup=get_albums_keyboard())
        
    elif choice in ALBUMS:
        await query.edit_message_text(text=f"در حال ارسال آهنگ‌ها... 🎧")
        
        # --- اینجا کار رو به پس‌زمینه می‌سپاریم تا ربات آزاد بشه ---
        asyncio.create_task(send_album_in_background(update.effective_chat.id, choice, context.bot))

async def get_audio_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.audio:
        audio_id = update.message.audio.file_id
        await update.message.reply_text(f"🎧 شناسه این آهنگ (کد زیر را کپی کنید):\n\n{audio_id}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.AUDIO, get_audio_id))

    print("Taylor Swift Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()