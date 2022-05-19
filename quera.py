import os
from typing import List
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


jobs=[]

def show_job(arr :List[WebElement]):
    for element in arr:
        job_dict={}
        job_title = element.find_element_by_xpath(".//h2[@class='chakra-heading css-1d6x238']/a/span").text
        print(f"عنوان شغل : {job_title}")
        job_dict["title"]=job_title
        company_name = element.find_element_by_xpath(".//p[@class='chakra-text css-1m52y4d']").text
        print(f"نام شرکت : {company_name}")
        job_dict["company"]=company_name
        # location = element.find_elements_by_xpath(".//p[@class='chakra-text css-1m52y4d']").text
        # print(f"محل کار:{location}")
        link = element.find_element_by_xpath(".//h2[@class='chakra-heading css-1d6x238']/a").get_attribute('href')
        job_dict["link"]=link
        print(f"اطلاعات بیشتر {link}")
        jobs.append(job_dict)
        print("----------------------------------------")
    
       


def crawl(data):    
    page=1
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,executable_path=f'{os.path.abspath(os.getcwd())}/geckodriver')
    driver.get(f"https://quera.ir/magnet/jobs?search={data}&page={page}")
    driver.implicitly_wait(10)
    try:
        # arr=wait.until(ec.visibility_of_all_elements_located((By.TAG_NAME,'article')))
        arr=driver.find_elements_by_tag_name('article')
        if not arr:
            print("!شغل مورد نظر در کوئرا یافت نشد")
        else:
            show_job(arr)
            while arr :
                page+=1
                driver.get(f"https://quera.ir/magnet/jobs?search={data}&page={page}")
                driver.implicitly_wait(10)
                arr=driver.find_elements_by_tag_name('article')
                if arr:
                    show_job(arr)
            print("!کاوش در کوئرا به پایان رسید")
   
    finally:
        driver.quit()







