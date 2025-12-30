import re
import requests
import time
import asyncio
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright




BASE_URL = "https://api.mail.tm"
domain_names = requests.get(f"{BASE_URL}/domains").json()
domain = domain_names['hydra:member'][0]['domain']

user = "use3659085"
email = f"{user}@{domain}"
passw = "Pass123"


print("Creando cuenta...")

account = requests.post(f"{BASE_URL}/accounts", json={
    "address": email,
    "password": passw
})

if account.status_code != 201:
  print("Account creatin failed !!!!!! ")
  #exit()

token_response = requests.post(f"{BASE_URL}/token", json={
    "address": email,
    "password": passw
})

token = token_response.json()['token']

headers = {"Authorization": f"Bearer {token}"}

print(f"Email ***{email}*** is ready")

print("Waiting for incoming message...")

async def confirm_account():
    # Iniciar Playwright
    async with async_playwright() as p:
        
        browser = await p.chromium.launch(headless=False) 
        page = await browser.new_page()

        while True:
            inbox = requests.get(f"{BASE_URL}/messages", headers=headers).json()
            messages = inbox["hydra:member"]

            if messages:
                for msg in messages:
                    full_msg = requests.get(
                        f"{BASE_URL}/messages/{msg['id']}",
                        headers=headers
                    ).json()

                    text = full_msg["text"]
                    match = re.search(r'https://login\.eset\.com/link/confirmregistration\S*', text)

                    if match:
                        confirm_url = match.group(0)
                        print("Abriendo enlace de confirmación...")
                        confirm_url = confirm_url.strip("[]")
                        print(f"URL limpia: {confirm_url}")
                        time.sleep(2)
                        
                        await page.goto(confirm_url)

                        try:
                            await page.wait_for_load_state('load')

                            print("✅ Cuenta confirmada")
                        except Exception as e:
                            print(f"❌ Error al hacer clic en el botón: {e}")

                        break  
                break 

            await asyncio.sleep(10)
        time.sleep(19)
        await browser.close()

asyncio.run(confirm_account())


