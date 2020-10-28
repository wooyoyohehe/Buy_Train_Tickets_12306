from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
browser = webdriver.Chrome()

starting_station = '南京'
destination = '千岛湖'
date = '2020-11-15'
# 最大化浏览器
browser.maximize_window()

url = 'https://www.12306.cn/index/'
# 打开浏览器预设网址
browser.get(url)
input1 = browser.find_element_by_id('fromStationText')
input2 = browser.find_element_by_id('toStationText')
input3 = browser.find_element_by_id('train_date')

input1.click()
input1.send_keys(starting_station)
o_InputSelect = browser.find_elements_by_class_name("ralign")
for i in o_InputSelect:
    if i.text == starting_station:
        i.click()
        break

input2.click()
input2.send_keys(destination)
o_InputSelect = browser.find_elements_by_class_name("ralign")
for i in o_InputSelect:
    if i.text == destination:
        i.click()
        break


# 使用js代码删掉日期的readonly属性，自己手动输入日期
js = 'document.getElementById("train_date").removeAttribute("readonly")'
browser.execute_script(js)
input3.clear()
input3.send_keys(date)
button = browser.find_element_by_id('search_one')

# 由于展开的日期搜索框挡住了查询按钮，导致按钮不可点击，要进行操作关闭日期选择框
# 鼠标左键点击左上角空白处，关闭日期选择框， 1为x坐标， 1为y坐标
# 也可以直接定位查询按钮坐标
# 查询页面上某个元素的方法：
# 1、检索元素 2、console 3、输入document.getElementById('element').getBoundingClientRect()
ActionChains(browser).move_by_offset(1, 1).click().perform()
button.click()

# print(browser.page_source)
# browser.close() #关闭浏览器
