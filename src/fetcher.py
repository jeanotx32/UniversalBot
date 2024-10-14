from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
chromedriver_location = Service(r"util\chromedriver.exe")
prefs = {}
#options.add_experimental_option("detach", True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")
#options.add_argument("--headless=new")
options.add_experimental_option('prefs', prefs)
options.add_argument(r"user-data-dir=tmp\selenium")
options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome(service= chromedriver_location, options=options)

driver.get('https://www.decisionproblem.com/')