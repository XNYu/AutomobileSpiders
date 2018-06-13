from selenium import webdriver
import time
browser = webdriver.Chrome()

file = open("F:/163links.txt","a")
file2 = open("F:/163.txt","r")
for l in file2:
    browser.get(l)
    js="var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)
    time.sleep(3)
    input = browser.find_elements_by_xpath("//div[@class='sec-list']//div[@class='item-cont']")
    for link in input:
        l = link.find_element_by_xpath("./h3/a")
        l = l.get_attribute("href")
        comment = link.find_element_by_xpath(".//span[@class='item-comment']")
        comment = comment.text
        file.write(l+","+comment+"\n")
file.close()
file2.close()
