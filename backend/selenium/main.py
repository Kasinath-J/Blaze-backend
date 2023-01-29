
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")


serv_obj = Service("backend\selenium_test\chromedriver.exe")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver = webdriver.Chrome(service=serv_obj,options=chrome_options)
driver.get("https://www.linkedin.com/in/panchumarthi-abhinav/")
# content = driver.find_element(By.CSS_SELECTOR, 'pre').text
# print(content)
# driver.close()