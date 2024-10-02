import os
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('discoverit-2024-aac136759c1b.json', scopes=scope)
client = gspread.authorize(creds)

# Open the spreadsheet
spreadsheet = client.open("Dana Masuk")  # Nama spreadsheet

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = "Selamat datang di Data Integrasi Pendaftaran DiscoverIT 2024.\nPilih layanan:\n" \
                      "/total - Total keseluruhan peserta\n" \
                      "/metode - Total peserta per metode\n" \
                      "/nama - Nama peserta yang sudah mendaftar"
    await update.message.reply_text(welcome_message)

# Function to handle the /total command
async def total_participants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheet = spreadsheet.worksheet("Pendaftaran Gform")
    total = sheet.acell("H5").value  # Total peserta di H5
    total_fee = int(total) * 100000  # Total biaya
    message = f"Total peserta: {total}\nTotal biaya: {total} * Rp100.000 = Rp{total_fee}"
    await update.message.reply_text(message)

# Function to handle the /metode command
async def total_by_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheet = spreadsheet.worksheet("Pendaftaran Gform")
    total_bri = sheet.acell("H2").value
    total_dana = sheet.acell("H3").value
    total_cash = sheet.acell("H4").value

    bri_fee = int(total_bri) * 100000
    dana_fee = int(total_dana) * 100000
    cash_fee = int(total_cash) * 100000

    message = (f"Total peserta BRI: {total_bri} - Total biaya: {total_bri} * Rp100.000 = Rp{bri_fee}\n"
               f"Total peserta DANA: {total_dana} - Total biaya: {total_dana} * Rp100.000 = Rp{dana_fee}\n"
               f"Total peserta CASH: {total_cash} - Total biaya: {total_cash} * Rp100.000 = Rp{cash_fee}")
    await update.message.reply_text(message)

# Function to handle the /nama command
async def participant_names(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheet = spreadsheet.worksheet("Pendaftaran Gform")
    names = sheet.col_values(4)[2:]  # Mengambil nama dari kolom D mulai dari D3
    message = "Daftar peserta yang sudah mendaftar:\n"
    for i, name in enumerate(names, start=1):
        message += f"{i}. {name}\n"
    
    await update.message.reply_text(message)

def main():
    # Inisialisasi Updater dengan ApplicationBuilder
    app = ApplicationBuilder().token("7732247490:AAHxQa3xDGhLzONdBM_bOso1CHCQ52cyFOA").build()

    # Tambahkan handler untuk perintah start
    app.add_handler(CommandHandler("start", start))
    # Tambahkan handler untuk perintah total
    app.add_handler(CommandHandler("total", total_participants))
    # Tambahkan handler untuk perintah metode
    app.add_handler(CommandHandler("metode", total_by_method))
    # Tambahkan handler untuk perintah nama
    app.add_handler(CommandHandler("nama", participant_names))

    # Jalankan bot
    app.run_polling()

if __name__ == '__main__':
    main()
