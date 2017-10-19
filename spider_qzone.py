from bs4 import BeautifulSoup
from selenium import webdriver
import time

#使用selenium

#登录QQ空间
def get_shuoshuo(qq):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://user.qzone.qq.com/{}/311'.format(qq)) #构造空间链接并访问
    time.sleep(3)
    try:
        driver.find_element_by_id('login_div')  #判断是否需要登录
        a = True
    except:
        a = False
    if a == True:
        try:
            driver.switch_to.frame('login_frame')
            driver.find_element_by_id('switcher_plogin').click()
            driver.find_element_by_id('u').clear()#选择用户名框
            driver.find_element_by_id('u').send_keys('1242670917')
            driver.find_element_by_id('p').clear()
            driver.find_element_by_id('p').send_keys('I2426709i74.')
            driver.find_element_by_id('login_button').click()
        except Exception as e:
            print(e)
        time.sleep(3)
    driver.implicitly_wait(3)
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon') # 通过是否有用户头像这个元素判断是否登录成功
        b = True
    except:
        b = False
        print('这个用户无法访问')
    if b == True:    # 如果登录成功就开始爬取内容
        driver.switch_to.frame('app_canvas_frame')
        content = driver.find_elements_by_css_selector('.content')
        stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        for con,sti in zip(content,stime):
            data = {
                'time':sti.text,
                'shuos':con.text
            }
            print(data)
        pages = driver.page_source
    while True:
        try:
            driver.find_element_by_link_text('下一页')
            d = True
        except:
            d = False
            break
        if b == True:
            driver.find_element_by_link_text('下一页').click()
            time.sleep(5)
            contents = driver.find_elements_by_css_selector('.content')
            times = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
            for c, t in zip(contents, times):
                datas = {
                    'qq': qq,
                    'time': t.text,
                    'shuos': c.text
                }
                print(datas)

    print("==========完成=============")
    driver.close()

if __name__ == '__main__':
    get_shuoshuo('1748898422')

