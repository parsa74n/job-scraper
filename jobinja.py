import os
from typing import List
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
jobs=[]

def show_jobs(arr : List[WebElement]):
    for element in arr:
        job_dict={}
        title=element.find_element_by_class_name('c-jobListView__titleLink').text
        print(f"عنوان شغل: {title}")
        job_dict["title"]=title
        company_name = element.find_elements_by_class_name('c-jobListView__metaItem')[0].text
        job_dict["company"]=company_name
        print(f"نام شرکت:{company_name}")
        location = element.find_elements_by_class_name('c-jobListView__metaItem')[1].text
        job_dict['location']=location
        print(f"محل کار:{location}")
        link = element.find_element_by_tag_name('a').get_attribute('href')
        job_dict['link']=link
        print(f"اطلاعات بیشتر {link}")
        jobs.append(job_dict)
        print("----------------------------------------")

def crawl(data:str):
    options = Options()
    options.headless = True
    page = 1
    driver = webdriver.Firefox(options=options,executable_path=f'{os.path.abspath(os.getcwd())}/geckodriver')
    driver.get(f"https://jobinja.ir/jobs?&filters%5Bjob_categories%5D%5B0%5D=&filters%5Bkeywords%5D%5B0%5D={data}&filters%5Blocations%5D%5B0%5D=&page={page}&preferred_before=1652660511&sort_by=relevance_desc")
    driver.implicitly_wait(10)
    try:
        arr = driver.find_elements_by_xpath("//li[@class='o-listView__item o-listView__item--hasIndicator c-jobListView__item o-listView__item__application  ']")
        if not arr:
            print('شغل مورد نظر در جابینجا یافت نشد!')
        else:
            show_jobs(arr)
            while arr:            
                page += 1
                # driver.get(f"https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B%5D={data}&page={page}")
                driver.get(f"https://jobinja.ir/jobs?&filters%5Bjob_categories%5D%5B0%5D=&filters%5Bkeywords%5D%5B0%5D={data}&filters%5Blocations%5D%5B0%5D=&page={page}&preferred_before=1652660511&sort_by=relevance_desc")
                driver.implicitly_wait(10)
                arr = driver.find_elements_by_xpath("//li[@class='o-listView__item o-listView__item--hasIndicator c-jobListView__item o-listView__item__application  ']")
                if arr:
                    show_jobs(arr)
            print('کاوش در جابینجا به پایان رسید!')

    finally:
        
        driver.quit()
