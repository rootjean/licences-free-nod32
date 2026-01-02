from playwright.sync_api import sync_playwright
import time
import random
import string
import asyncio
from playwright.async_api import async_playwright

from mailtemp import confirmado_event,crear_email_temporal, confirmar_cuenta



def generar_usuario():
    return "".join(random.choice(string.digits) for _ in range(5))


def generar_password():
    mayus = string.ascii_uppercase
    minus = string.ascii_lowercase
    nums = string.digits
    esp = "!@#$%^&*()_+-=[]{}|;:,.<>?/"

    password = [
        random.choice(mayus),
        random.choice(minus),
        random.choice(nums),
        random.choice(esp),
    ]

    all_chars = mayus + minus + nums + esp
    while len(password) < 12:
        password.append(random.choice(all_chars))

    random.shuffle(password)
    return "".join(password)


async def registrar_cuenta(email, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://login.eset.com/register")

        await page.wait_for_selector("#cc-accept")
        await page.click("#cc-accept")

        await page.fill(".css-9xm6po", email)
        await page.click(".css-f58z5q")

        await page.fill("#password", password)
        await page.click(".css-6rqqax")
        await page.click(".css-f58z5q")

        print("Esperando confirmación...")
        await confirmado_event.wait()

        await acciones_post_confirmacion(page)

        while True:
            await asyncio.sleep(1)


async def acciones_post_confirmacion(page):
    await page.wait_for_selector(".css-owa58g")
    await page.click(".css-owa58g")

    await page.wait_for_selector(".css-klw4i7")
    await page.click('label[for="trial"]')
    await page.click(".css-f58z5q")
    
    await page.wait_for_selector(".css-1n3hg2q")
    await page.click('label[for="148"]')
    await page.click(".css-f58z5q")
    
    await page.wait_for_selector(".css-f58z5q")
    await page.click(".css-f58z5q")

    await page.fill(".css-9xm6po", "JuanPedro")
    await page.click(".css-f58z5q")

    await page.wait_for_selector(".css-c2hiim")
    await page.click(".css-f58z5q")

    await page.wait_for_selector(".css-1n3hg2q")
    await page.click('label[for="1"]')
    await page.click(".css-f58z5q")
    
    await page.wait_for_selector(".css-owa58g")
    await page.click(".css-owa58g")  

    await page.wait_for_selector('button[data-label="dashboard-subscriptions-card-button"]')
    await page.click('button[data-label="dashboard-subscriptions-card-button"]')

    await page.click(".css-f58z5q")

    clave_locator = page.locator(
        'div[data-label="license-detail-license-key"] p'
    )

    await clave_locator.wait_for()
    clave = await clave_locator.inner_text()

    print(clave)



