from selenium import webdriver
import time

driver = webdriver.Chrome()
url = 'https://kyfw.12306.cn/otn/resources/login.html'
driver.get(url)
driver.find_element_by_class_name('login-hd-account').click()

input_username = driver.find_element_by_id('J-userName')
input_password = driver.find_element_by_id('J-password')

input_username.click()
time.sleep(1)
input_username.send_keys('18362050564')
input_password.click()
time.sleep(1)
input_password.send_keys('wushuang992974')

time.sleep(10)

driver.get("https://kyfw.12306.cn/otn/leftTicket/init")
