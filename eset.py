from playwright.sync_api import sync_playwright
import time
import random
import string
import asyncio
from mailtemp import crear_email_temporal, confirmar_cuenta



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


def registrar_cuenta(email, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://login.eset.com/register")

        page.wait_for_selector("#cc-accept")
        page.click("#cc-accept")

        page.fill(".css-9xm6po", email)
        page.click(".css-f58z5q")

        page.fill("#password", password)
        page.click(".css-6rqqax")
        page.click(".css-f58z5q")


        #page_mail = browser.new_page()
        #page_mail.goto("https://mail.tm/es/")

        time.sleep(2)
        #browser.close()
