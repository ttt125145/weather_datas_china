"""获取各城市地区链接"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time,json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get('https://www.weather.com.cn/')
time.sleep(1)

elem1 =driver.find_element(By.CSS_SELECTOR, "div[class='search clearfix'] > input")
elem1.click()
time.sleep(0.1)

provinces = driver.find_elements(By.CSS_SELECTOR,"dd[id='searchCityList'] > a")
pro_titles = [province.get_attribute('title') for province in provinces]


h_provinces = {}
sup_city = ['北京','上海','天津','重庆']

for t in pro_titles:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,f"dd[id='searchCityList'] > a[title='{t}']" )))
    #等待该省市加载
    pro = driver.find_element(By.CSS_SELECTOR,f"dd[id='searchCityList'] > a[title='{t}']")
    driver.execute_script("arguments[0].click();", pro) 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"dd[id='cityList_city'] > a")))
    #等待所有辖区加载
    a = pro.get_attribute('title') 
    if a in sup_city:  
        areas = driver.find_elements(By.CSS_SELECTOR,"dd[id='cityList_city'] > a")
        h_areas = {}
        for area in areas:
            h_areas[area.text] = area.get_attribute('href')
        h_provinces[t] = h_areas
    else:
        h_cities = {}
        cities = driver.find_elements(By.CSS_SELECTOR,"dd[id='cityList_city'] > a")
        titles = [city.get_attribute('title') for city in cities]
        for title in titles:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "dd[id='cityList_city']")))
            time.sleep(0.1)
            while  len(driver.find_element(By.CSS_SELECTOR,f"dd[id='cityList_city']").find_elements(By.TAG_NAME, 'a')) == 0:
            #意外的空栏情况
                back = driver.find_element(By.CSS_SELECTOR,"div[class='province-top'] > p > span[class='province-back']")
                driver.execute_script("arguments[0].click();", back)#返回全国
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,f"dd[id='searchCityList'] > a[title='{t}']" )))
                #等待该省市加载
                pro = driver.find_element(By.CSS_SELECTOR,f"dd[id='searchCityList'] > a[title='{t}']")
                driver.execute_script("arguments[0].click();", pro)#读取点击该省

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"dd[id='cityList_city'] > a[title='{title}']")))
            #等待此城市元素加载出来
            city = driver.find_element(By.CSS_SELECTOR,f"dd[id='cityList_city'] > a[title='{title}']")
            h_areas = {}           
            driver.execute_script("arguments[0].click();", city)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"dd[id='cityList_city'] > a")))
            #等待城市下地区加载出来
            areas = driver.find_elements(By.CSS_SELECTOR,"dd[id='cityList_city'] > a")
            for area in areas:
                h_areas[area.text] = area.get_attribute('href')
            h_cities[title] = h_areas

            back = driver.find_element(By.CSS_SELECTOR,"div[class='province-top'] > p > span[class='province-back']")
            driver.execute_script("arguments[0].click();", back)#返回省下城市
        
        h_provinces[t] = h_cities
       
        back = driver.find_element(By.CSS_SELECTOR,"div[class='province-top'] > p > span[class='province-back']")
        driver.execute_script("arguments[0].click();", back)#返回全国
        pro = driver.find_element(By.CSS_SELECTOR,f"dd[id='searchCityList'] > a[title='{t}']")
    driver.execute_script("arguments[0].click();", pro) 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"dd[id='cityList_city'] > a")))
        
js_href = json.dumps(h_provinces,ensure_ascii=False,indent=2)
with open('天气数据/urls.json','w',encoding='utf-8')as f:
    f.write(js_href)