from selenium import webdriver
import time

class FindJobs:

    '''
    一个前程无忧自动投简历的爬虫，暂时只是按照给定的链接投，没有对登录验证码做自动处理，后续会考虑
    '''

    def login(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://login.51job.com/login.php?lang=c') #构造空间链接并访问
        time.sleep(3)
        try:
            driver.find_element_by_id('loginname')  # 判断是否需要登录
            a = True
        except:
            a = False
        if a == True:
            try:
                driver.find_element_by_id('loginname').send_keys('15917916221')
                driver.find_element_by_id('password').send_keys('Nihaomingtian9.')
                driver.find_element_by_id('login_btn').click()
                try:
                    driver.find_element_by_id('verifycode') # 判断是否需要输入验证码
                    key = input('请输入验证码： ')
                    driver.find_element_by_id('verifycode').send_keys(key)
                    driver.find_element_by_id('login_btn').click()
                except Exception as e:
                    print('你已经登录成功')
                time.sleep(2)
                return driver
            except Exception as e:
                print(e)


    def apply_job(self,driver):
        try:
            jobs_list = driver.find_elements_by_xpath("//div[@class='dw_table']/div[@class='el']") # get job list
        except Exception as e:
            print('get job list failed ! closing the tab')
        for job in jobs_list:
            try:
                job_url = job.find_element_by_tag_name('a').get_attribute('href')
                job.find_element_by_tag_name('a').click()
                time.sleep(2)
            except Exception as e:
                print('got error when get_job: ',e)
            handles = driver.window_handles
            for handle in handles:
                if handle != driver.current_window_handle:
                    driver.switch_to_window(handle)
                    break

            try:
                job_name = driver.find_element_by_xpath("//div[@class='cn']/h1").text.strip()
                company = driver.find_element_by_xpath("//div[@class='cn']/p[@class='cname']").text.strip()
                salary = driver.find_element_by_xpath("//div[@class='cn']/strong").text.strip()

                driver.find_element_by_xpath("//a[@id='app_ck']/img").click()
                print(job_name+'-----'+'职位申请成功！')
                print('公司名称: '+company+'  待遇: '+salary+'  职位链接： '+job_url)
                time.sleep(1)
            except Exception as e:
                print('apply job failed',e)
            driver.close()
            driver.switch_to_window(handles[0])

    def get_next_page(self):
        try:
            driver.find_element_by_xpath("//div[@class='p_in']/ul/li[last()]/a").click()
            time.sleep(3)
        except Exception as e:
            print('failed to get next page',e)
        handles = driver.window_handles
        if len(handles) < 2:
            return False
        for handle in handles:
            if handle != driver.current_window_handle:
                driver.switch_to_window(handle)
                break

    def open_page(self,url):
        try:
            driver.get(url)
            time.sleep(4)
            return driver
        except Exception as e:
            print(e)


if __name__ == '__main__':
    jobs = FindJobs()
    driver = jobs.login()
    urls = ['http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=040000&keyword=Python%20%E5%BC%80%E5%8F%91&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9']
    for url in urls:
        while True:
            driver = jobs.open_page(url)     # 打开一个链接
            jobs.apply_job(driver)           # 申请职位列表全部职位
            jobs.get_next_page()


