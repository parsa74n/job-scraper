import os
from typing import List
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

def show_jobs(arr: List[WebElement],driver):
    for element in arr:
        job_title = element.find_element_by_xpath(
            ".//div[@class='col-12 d-flex justify-content-between px-0 mb-2']/span[@class='col-10 col-lg-10 font-weight-bolder px-0 text-black']").text
        print(f"عنوان شغل : {job_title}")
        company_name = element.find_element_by_xpath(".//span[@class='text-black']").text
        print(f"نام شرکت : {company_name}")
        location = element.find_element_by_xpath(".//span[@class='text-muted font-size-6']").text
        print(f"محل کار : {location}")
        base = driver.current_window_handle
        link=element.find_element_by_tag_name('a')
        link_href=link.get_attribute('href')
        print(f"اطلاعات بیشتر {link_href}")
        driver.switch_to.window(base)
        print("----------------------------------------")

def crawl(data:str):
    # data = input('please enter a job:')
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,executable_path=f'{os.path.abspath(os.getcwd())}/geckodriver')
    page = 1
    driver.get(f"https://jobvision.ir/jobs?keyword={data}&page={page}")
    # wait=WebDriverWait(driver,10)
    driver.implicitly_wait(10)
    try:
        # arr=wait.until(ec.visibility_of_all_elements_located((By.TAG_NAME, "job-card")))
        arr=driver.find_elements_by_tag_name('job-card')
        if not arr:
            print('!شغل مورد نظر در حاب ویژن یافت نشد')
        else:
            show_jobs(arr,driver)
            while arr:
                page += 1
                driver.get(f"https://jobvision.ir/jobs?keyword={data}&page={page}")
                driver.implicitly_wait(10)
                # arr=wait.until(ec.visibility_of_all_elements_located((By.TAG_NAME, "job-card")))
                arr=driver.find_elements_by_tag_name('job-card')
                if arr:
                    show_jobs(arr,driver)
                
            print("!کاوش در جابویژن به پایان یافت")

    finally:
        driver.quit()
