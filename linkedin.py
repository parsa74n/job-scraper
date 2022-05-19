import threading
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,JavascriptException


find_btn_flag=False
n=0
def show_job(element :WebElement):
    global n
    
    title=element.find_element(By.XPATH,".//h3[@class='base-search-card__title']").text
    print(f"job title : {title}")
    company_name=element.find_element(By.XPATH,".//h4[@class='base-search-card__subtitle']").text
    print(f"company name : {company_name}")
    location=element.find_element(By.XPATH,".//span[@class='job-search-card__location']").text
    print(f"location : {location}")
    info=element.find_element_by_tag_name("a")
    link=info.get_attribute('href')
    print(f"more info : {link}")
    n=n+1
    print(n)
    print("----------------------------------------------")
    

def click_btn(driver):
    global find_btn_flag
    while not find_btn_flag:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.execute_script('document.getElementsByClassName("infinite-scroller__show-more-button infinite-scroller__show-more-button--visible")[0].click();')
        except JavascriptException:
            find_btn_flag=True
            break
            

def crawl(data:str,location:str):
    options = Options()
    global find_btn_flag
    options.headless = True
    driver = webdriver.Firefox(options=options,executable_path=f'{os.path.abspath(os.getcwd())}/geckodriver')
    driver.get(f"https://www.linkedin.com/jobs/search?keywords={data}&location={location}")
    driver.implicitly_wait(5)
    is_thread_run=False
    try:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")     
        arr=driver.find_elements(By.XPATH,"//ul[@class='jobs-search__results-list']/li")
        child=arr[0]
        show_job(child)
        m=0
        t=threading.Thread(target=click_btn,args=(driver,))
        while True:
            try:
                child=child.find_element(By.XPATH,"following-sibling::li")

                show_job(child)
                m=m+1
                if(m==10):
                    m=0
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                
            except NoSuchElementException: 
                if not is_thread_run:
                    is_thread_run=True
                    t.start()
                if find_btn_flag:
                    print('crawling in linkedin ends!!!')     
                    break 
               
    except(IndexError,NoSuchElementException) as e:
        print('your job title not found!!!!')
    finally:
        driver.quit()