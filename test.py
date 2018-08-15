from selenium import webdriver
import time
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}


browser = webdriver.Chrome()
browser.get('http://www.114best.com/')
keyword = input('请输入搜索关键词：')
maxnum = 2


def login():
    button1 = browser.find_element_by_xpath('//*[@id="span_onuser_menu"]/a[2]')
    button1.click()
    time.sleep(1)
    browser.switch_to_frame(browser.find_element_by_id('showframe'))
    #上一行为跳转到登陆框
    text = input('请输入验证码：')
    username = input('请输入账号：')
    password = input('请输入密码：')
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
    time.sleep(3)
    #上面一大段为登陆
    #下面以首页的公司为例
    browser.refresh()


def search():
    search1 = browser.find_element_by_xpath('//*[@id="w"]')
    search1.clear()
    search1.send_keys(keyword)
    dianji = browser.find_element_by_xpath('//*[@id="query"]')
    dianji.click()


def craw():
    num = browser.find_elements_by_xpath('//*[@id="content"]/div[1]/div')
    for i in range(2, len(num)):
        company = browser.find_element_by_xpath('//*[@id="content"]/div[1]/div[' + str(i) + ']/div[1]/div[2]/a')
        company.click()
        all_tr = browser.find_elements_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/table/tbody/tr')
        time.sleep(3)
        for tr in range(1, len(all_tr) + 1):
            time.sleep(3)
            try:
                button = browser.find_element_by_xpath(
                    '//*[@id="content"]/div[1]/div[4]/div[1]/table/tbody/tr[' + str(tr) + ']/td[2]/span/a')
                button.click()
                time.sleep(1)
                tel_number = browser.find_element_by_xpath(
                    '//*[@id="content"]/div[1]/div[4]/div[1]/table/tbody/tr[' + str(tr) + ']/td[2]/b').text
                company_name = browser.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[1]/div[2]/div/h1/span').text.strip()
                print(company_name, end='')
                print(tel_number)
                data = {
                    'name': company_name,
                    'tel': tel_number
                }
                save_to_file(data)
                time.sleep(1)
                break
            except:
                #time.sleep(3)
                None
        #time.sleep(3)
        browser.back()
        time.sleep(3)
        # 抓取完之后在回到前一页面


def crawling():
    time.sleep(3)
    response = requests.get('http://www.114best.com/gs11/434180324.html', headers=headers)    #用一个公司的url测试是否请求成功
    if response.status_code == 403:
        print('访问失败，等待3分钟')
        time.sleep(180)     #这里可以改一下试一下，可能可以减少一点时间
        browser.refresh()
        craw()
    else:
        craw()


def next_page():

    for i in range(1, maxnum + 1):
        crawling()
        print('这一页爬取结束，即将爬取下一页')
        for m in range(8, 13):
            nextpage = browser.find_element_by_xpath('//*[@id="content"]/div[3]/a[' + str(m) + ']')
            if nextpage.text == '下一页>':
                nextpage.click()
                break
            else:
                None


def save_to_file(data):
    with open('114.csv', 'a') as f:
        f.write(data['name'] + ',' + data['tel'] + '\n')


def main():
    with open('114.csv', 'a') as f:
        f.write('名称, 电话' + '\n')
    login()
    search()
    next_page()
    browser.close()


if __name__ == '__main__':
    main()
