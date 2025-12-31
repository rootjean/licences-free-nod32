from playwright.sync_api import sync_playwright
import time
import random
import string
import asyncio
import requests
import re
from playwright.async_api import async_playwright

def user():
    cararc = string.ascii_letters

    user = [random.choice(cararc)]

    while len(user) < 6:
        user.append(random.choice(cararc))
    random.shuffle(user)
    return "".join(user)
        


def contra():
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    especiales = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    numeros = string.digits

    contra = [
        random.choice(mayusculas),
        random.choice(minusculas),
        random.choice(especiales),
        random.choice(numeros)
    ]

    todos = mayusculas + minusculas + especiales + numeros
    while len(contra) < 12:
        contra.append(random.choice(todos))
    random.shuffle(contra)
    return "".join(contra)






with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    pages = []

    for i in range(1):
        page = browser.new_page()
        page.goto("https://login.eset.com/register")
        pages.append(page)

    for page in pages:
        page.wait_for_selector("#cc-accept")
        page.click("#cc-accept")



        page.fill(".css-9xm6po", "use3659085@airsworld.net") # VALORE EMAIL
        page.click(".css-f58z5q")
        page.fill("#password", contra())
        page.click(".css-6rqqax")
        page.click(".css-f58z5q")


    time.sleep(2000)

    browser.close()
