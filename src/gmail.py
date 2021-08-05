import asyncio
import time
from pyppeteer import launch
from pyppeteer.errors import ElementHandleError, NetworkError
from pyvirtualdisplay import Display
import sys
import nest_asyncio
import logging

nest_asyncio.apply()


async def gmailLogin(username, password, url):
    display = Display(visible=0, size=(800, 800))
    display.start()
    browser = await launch(
        options={
            'headless': False,
            # 'executablePath': 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            'ignoreDefaultArgs': ['--enable-automation'],
            'args': ['--no-sandbox', '--disable-gpu'],
        })
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    await test(page, username, password, url)
    print(1)
    # 点击安全检测页面的DONE
    # await page.click('div > content > span')#如果本机之前登录过，并且page.setUserAgent设置为之前登录成功的浏览器user-agent了，
    # 就不会出现安全检测页面，这里如果有需要的自己根据需求进行更改，但是还是推荐先用常用浏览器登录成功后再用python程序进行登录。


async def test(page, username, password, url):
    await page.goto(url)
    # 输入Gmail
    # await page.click("#switcher_plogin")
    # await page.type('#u', username)
    # await page.type('#p', password)
    await page.type('#fm-login-id', username)
    await page.type('#fm-login-password', password)

    # 点击下一步
    await page.click("button[type='submit']")
    content = await page.content()
    print(content)
    a = 12
    # time.sleep(1)


if __name__ == '__main__':
    username = '827732439@qq.com'
    password = 'ying4216321'
    url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?target=self&appid=522005705&daid=4&s_url=https://mail.qq.com/cgi-bin/readtemplate?check=false%26t=loginpage_new_jump%26vt=passport%26vm=wpt%26ft=loginpage%26target=&style=25&low_login=1&proxy_url=https://mail.qq.com/proxy.html&need_qr=0&hide_border=1&border_radius=0&self_regurl=http://zc.qq.com/chs/index.html?type=1&app_id=11005?t=regist&pt_feedback_link=http://support.qq.com/discuss/350_1.shtml&css=https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input_for_xmail51328e.css'
    url = "https://login.taobao.com/member/login.jhtml?spm=a21wu.241046-hk.754894437.1.41cab6cb3wPlvK&f=top&redirectURL=https%3A%2F%2Fworld.taobao.com%2F"
    url = "https://login.taobao.com/member/login.jhtml?spm=a21wu.241046-hk.754894437.1.41cab6cbHvVpS6&f=top&redirectURL=https%3A%2F%2Fworld.taobao.com%2F"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gmailLogin(username, password, url))
