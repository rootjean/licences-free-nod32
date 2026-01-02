import random
import string
from playwright.async_api import async_playwright
from mailtemp import confirmado_event

def generar_usuario():
    return "".join(random.choices(string.digits, k=5))


def generar_password():
    chars = {
        "mayus": string.ascii_uppercase,
        "minus": string.ascii_lowercase,
        "nums": string.digits,
        "esp": "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    }

    password = [
        random.choice(chars["mayus"]),
        random.choice(chars["minus"]),
        random.choice(chars["nums"]),
        random.choice(chars["esp"]),
    ]

    all_chars = "".join(chars.values())
    password.extend(random.choices(all_chars, k=12 - len(password)))
    random.shuffle(password)

    return "".join(password)


async def registrar_cuenta(email, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://login.eset.com/register")

        await page.locator("#cc-accept").click()
        await page.locator(".css-9xm6po").fill(email)
        await page.locator(".css-f58z5q").click()

        await page.locator("#password").fill(password)
        await page.locator(".css-6rqqax").click()
        await page.locator(".css-f58z5q").click()

        print("Esperando confirmación...")
        await confirmado_event.wait()

        clave = await acciones_post_confirmacion(page)
        print(f"Clave =========> {clave}")

        await browser.close()



async def acciones_post_confirmacion(page):
    btn_next = page.locator(".css-f58z5q")

    await page.locator(".css-owa58g").click()

    await page.locator('label[for="trial"]').click()
    await btn_next.click()

    await page.locator('label[for="148"]').click()
    await btn_next.click()

    await btn_next.click()

    await page.locator('input[name="name"]').fill("JuanPedro")
    await btn_next.click()

    await btn_next.click()

    await page.locator('label[for="1"]').click()
    await btn_next.click()

    await page.locator(".css-owa58g").click()

    await page.locator(
        'button[data-label="dashboard-subscriptions-card-button"]'
    ).click()

    await btn_next.click()

    clave_locator = page.locator(
        'div[data-label="license-detail-license-key"] p'
    )

    await clave_locator.wait_for()
    return await clave_locator.inner_text()






