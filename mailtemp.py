import requests
import re
import time
import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://api.mail.tm"
confirmado_event = asyncio.Event()


def crear_email_temporal(username, password):
    domains = requests.get(f"{BASE_URL}/domains").json()
    domain = domains["hydra:member"][0]["domain"]
    email = f"{username}@{domain}"

    acc = requests.post(f"{BASE_URL}/accounts", json={
        "address": email,
        "password": password
    })

    if acc.status_code != 201:
        raise Exception("Error creando la cuenta de correo")

    token_response = requests.post(f"{BASE_URL}/token", json={
        "address": email,
        "password": password
    })

    token = token_response.json()['token']

    return email, token


async def confirmar_cuenta(token):
    headers = {"Authorization": f"Bearer {token}"}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        while True:
            inbox = requests.get(f"{BASE_URL}/messages", headers=headers).json()
            mensajes = inbox["hydra:member"]

            if mensajes:
                msg_id = mensajes[0]["id"]
                full_msg = requests.get(
                    f"{BASE_URL}/messages/{msg_id}",
                    headers=headers
                ).json()

                texto = full_msg.get("text", "")
                match = re.search(
                    r"https://login\.eset\.com/link/confirmregistration\S*",
                    texto
                )

                if match:
                    url = match.group(0).strip("[]")
                    await page.goto(url)
                    await page.wait_for_load_state("load")

                    print("Cuenta confirmada")
                    confirmado_event.set() 
                    break

            await asyncio.sleep(2)

        await asyncio.sleep(2)
