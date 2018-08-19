from selenium import webdriver
import time
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}


browser = webdriver.Chrome()
browser.get('http://www.114best.com/')
keyword = input('请输入搜索关键词：')
maxnum = 20


def login():
    button1 = browser.find_element_by_xpath('//*[@id="span_onuser_menu"]/a[2]')
    button1.click()
    time.sleep(1)
    browser.switch_to_frame(browser.find_element_by_id('showframe'))            #跳转到登陆框
    username = input('请输入账号：')
    password = input('请输入密码：')
    text = input('请输入验证码：')
    username_button = browser.find_element_by_xpath('//*[@id="login-username"]')
    username_button.clear()
    username_button.send_keys(username)
    password_button = browser.find_element_by_xpath('//*[@id="login-password"]')
    password_button.clear()
    password_button.send_keys(password)
    yzm_button = browser.find_element_by_xpath('//*[@id="login-verifycode"]')
    yzm_button.clear()
    yzm_button.send_keys(text)
    login_button = browser.find_element_by_xpath('//*[@id="login-submit"]')
    login_button.click()
    time.sleep(3)                                                               #上面一大段为登陆
    browser.refresh()


def search():               #此为输入关键词函数，进行搜索
    search1 = browser.find_element_by_xpath('//*[@id="w"]')
    search1.clear()
    search1.send_keys(keyword)
    dianji = browser.find_element_by_xpath('//*[@id="query"]')
    dianji.click()


def get_info(i):
    company = browser.find_element_by_xpath('//*[@id="content"]/div[1]/div[' + str(i) + ']/div[1]/div[2]/a')
    company.click()             #这两行为进入公司的信息页面
    all_tr = browser.find_elements_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/table/tbody/tr')       #获取信息总数
    time.sleep(3)
    for tr in range(1, len(all_tr) + 1):
        time.sleep(3)
        try:
            button = browser.find_element_by_xpath(
                '//*[@id="content"]/div[1]/div[4]/div[1]/table/tbody/tr[' + str(tr) + ']/td[2]/span/a')
            button.click()      #点击之后才能获取详细内容
            time.sleep(1)
            datas = {}
            name = browser.find_element_by_xpath(
                '//*[@id="content"]/div[1]/div[1]/div[1]/div[2]/div/h1/span').text.strip() + '：'
            print(name)         #获取公司名称并存入表中
            with open('114.csv', 'a') as f:			#前面的114.csv为文件名，可以跟自己爬取的内容进行更改
                f.write(name + '\n')
            for rt in range(1, len(all_tr) + 1):
                first = browser.find_element_by_xpath(
                    '//*[@id="content"]/div[1]/div[4]/div[1]/table/tbody/tr[' + str(rt) + ']/td[1]')
                second = browser.find_element_by_xpath(
                    '//*[@id="content"]/div[1]/div[4]/div[1]/table/tbody/tr[' + str(rt) + ']/td[2]')
                key = first.text.split('：')[0].replace(u'\u3000', u' ')
                value = second.text
                data = {
                    key: value
                }
                datas.update(data)          #获取单个公司的详细信息
            print(datas)
            save_to_file(datas)             #调用存入函数
            time.sleep(1)
            break
        except:
            None
    browser.back()
    time.sleep(3)
    # 抓取完之后在回到前一页面


def choose():
    response = requests.get('http://www.114best.com/gs11/434180324.html', headers=headers)  # 用一个公司的url测试是否请求成功
    return response.status_code


def craw():
    num = browser.find_elements_by_xpath('//*[@id="content"]/div[1]/div')
    for m in range(2, len(num)):
        time.sleep(2)
        response = choose()
        if response == 403:
            print('\033[0;31m访问失败，等待1分钟！\033[0m')
            time.sleep(60)  # 这里可以改一下试一下，可能可以减少一点时间
            browser.refresh()
            while choose() == 403:
                print('\033[0;31m访问失败，等待1分钟！\033[0m')
                time.sleep(60)  # 这里可以改一下试一下，可能可以减少一点时间
                browser.refresh()
            get_info(m)
        else:
            get_info(m)


def next_page():
        try:
            for m in range(1, 15):          #这里的15可以更改，为了能爬取下来，所以取较大的数
                nextpage = browser.find_element_by_xpath('//*[@id="content"]/div[3]/a[' + str(m) + ']')
                if nextpage.text == '下一页>':
                    nextpage.click()
                    break
                else:
                    None
        except:
            None


def crawling():
    for i in range(1, maxnum + 1):
        craw()
        print('第' + str(i) + '页爬取结束，即将爬取下一页')
        time.sleep(0.5)
        response = choose()
        if response == 403:
            print('\033[0;31m下一页访问失败，等待1分钟！\033[0m')
            time.sleep(60)  # 这里可以改一下试一下，可能可以减少一点时间
            browser.refresh()
            while choose() ==403:
                print('\033[0;31m下一页访问失败，等待1分钟！\033[0m')
                time.sleep(60)  # 这里可以改一下试一下，可能可以减少一点时间
                browser.refresh()
            next_page()
        else:
            next_page()


def save_to_file(data):         #此函数将信息存入表格
    with open('114.csv', 'a') as f:			#前面的114.csv为文件名，可以跟自己爬取的内容进行更改
        for keys in data.keys():
            keys = keys + ','
            f.write(keys)
        f.write('\n')
        for values in data.values():
            values = values + ','
            f.write(values)
        f.write('\n\n')


def main():     #定义主函数，调用其他函数
    login()
    search()
    crawling()
    print('\033[0;31m爬取结束( •̀ ω •́ )y\033[0m')
    browser.close()     #爬取结束后浏览器自动关闭


if __name__ == '__main__':
    main()
