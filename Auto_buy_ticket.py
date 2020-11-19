# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

username='1836205****'
password='*************'
starting_station = '北京'
destination = '南京'
# 日期的格式是‘yyyy-mm-dd’
date = '2020-11-20'

driver = webdriver.Chrome()
url = 'https://kyfw.12306.cn/otn/resources/login.html'
driver.get(url)
driver.maximize_window()
driver.find_element_by_class_name('login-hd-account').click()

input_username = driver.find_element_by_id('J-userName')
input_password = driver.find_element_by_id('J-password')
input_username.click()
input_username.send_keys(username)

input_password.click()
input_password.send_keys(password)
# verification code needed here, sometimes causes bugs

up_box = driver.find_element_by_id("login_slide_box")
while not up_box.is_displayed():
    time.sleep(1)
print("验证码输入正确！")
# driver.find_element_by_id('J-login').click()

driver.implicitly_wait(1)
# 加入拖动鼠标滑动滑块的动作链
slider = driver.find_element_by_id("nc_1_n1z")
# 对div_tag进行滑动操作
action = ActionChains(driver)  # 实例化一个动作对象
action.click_and_hold(slider).perform()  # 点击且长按不放

# 规避检测使用selenium的解决方法 滑块登录那边要用到
script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
driver.execute_script(script)
# for i in range(5):
#     # perform 让动作链立即执行
action.move_by_offset(340, 0).perform()

while(driver.current_url != "https://kyfw.12306.cn/otn/view/index.html"):
    time.sleep(0.5)
    print("登录中......")
print ("登陆成功!")

time.sleep(1)
driver.find_element_by_xpath("//a[@class='btn btn-primary ok']").click()
driver.find_element_by_xpath("//a[@name='g_href']").click()


input1 = driver.find_element_by_id('fromStationText')
input2 = driver.find_element_by_id('toStationText')
input3 = driver.find_element_by_id('train_date')
input1.click()
input1.send_keys(starting_station)
InputSelect = driver.find_elements_by_class_name("ralign")
for i in InputSelect:
    if i.text == starting_station:
        i.click()
        break

input2.click()
input2.send_keys(destination)
InputSelect = driver.find_elements_by_class_name("ralign")
for i in InputSelect:
    if i.text == destination:
        i.click()
        break

js = 'document.getElementById("train_date").removeAttribute("readonly")'
driver.execute_script(js)
input3.clear()
input3.send_keys(date)
button = driver.find_element_by_id('search_one')
ActionChains(driver).move_by_offset(1, 1).click().perform()
driver.find_element_by_xpath("//li[@id='isHighDan']").click()
button.click()
driver.implicitly_wait(3)

# 把当前窗口切换为新跳出来的窗口
all_handles = driver.window_handles
now_handle = driver.current_window_handle
for handle in all_handles:
    if handle != now_handle:
        driver.switch_to.window(handle)

ticket_info = driver.find_element_by_xpath("//td[@id='SWZ_24000000G10G']")
i = 1
while True:
    WebDriverWait(driver, 1000).until(
        ec.presence_of_element_located((By.XPATH, "//tbody[@id='queryLeftTable']/tr"))
    )
    ticket_info = driver.find_element_by_xpath("//td[@id='SWZ_24000000G10G']")
    if ticket_info.text == '--' or ticket_info.text == '候补' or ticket_info.text == '无':
        driver.refresh(5)
    print("正在第"+ str(i) +"次刷票....")
    i += 1

else:
    print("现在有票，正在锁定.....")
driver.find_element_by_xpath("//tr[@id='ticket_24000000G10G']/td/a[@class='btn72']").click()
time.sleep(3)
while driver.current_url != "https://kyfw.12306.cn/otn/confirmPassenger/initDc":
    time.sleep(0.5)
print("进入乘客确认界面，默认选择第一位乘客")
driver.find_element_by_xpath("//input[@id='normalPassenger_0']").click()
driver.find_element_by_xpath("//a[@id='submitOrder_id']").click()
time.sleep(1)
verify_box = driver.find_element_by_id("content_checkticketinfo_id")
while not verify_box.is_displayed():
    time.sleep(0.5)
driver.find_element_by_xpath("//div[@id='erdeng1']/ul[@class='seat-list']/li/a[@id='1F']").click()
driver.find_element_by_xpath("//a[@id='qr_submit_id']").click()
if driver.find_element_by_xpath("//div[@id='content_defaultwarningAlert_id']").is_displayed():
    print("本次列车剩余席位已无法满足您的选座需求，系统为您自动分配了其他席位，请确认后继续支付或取消订单。")
    driver.find_element_by_id("qd_closeDefaultWarningWindowDialog_id").click()
print("恭喜你，可以回家过年了!!!!!!")


