from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

import threading
import os
from threading import Lock

delay=0

#listid
##button
makePaperclip_Id='//*[@id="btnMakePaperclip"]'
buy_wire_Id='//*[@id="btnBuyWire"]'
buy_autoclipper_Id='//*[@id="btnMakeClipper"]'
btnLowerPrice_Id = '//*[@id="btnLowerPrice"]'
btnRaisePrice_Id = '//*[@id="btnRaisePrice"]'


##info
funds_Id='//*[@id="funds"]'
wire_lenght_Id='//*[@id="wire"]'
margin_id='//*[@id="margin"]'
autoclipper_cost_Id='//*[@id="clipperCost"]'
wire_price_Id='//*[@id="wireCost"]'
nb_paper_clip_Id='//*[@id="clips"]'
nb_unsold_clip_Id='//*[@id="unsoldClips"]'

options = Options()
chromedriver_location = Service(r"util\chromedriver.exe")
prefs = {}
#options.add_experimental_option("detach", True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")
#options.add_argument("--headless=new")
options.add_experimental_option('prefs', prefs)
#options.add_argument(r"user-data-dir=tmp\selenium")
options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome(service= chromedriver_location, options=options)

driver.get('https://www.decisionproblem.com/paperclips/index2.html')
#driver.get('https://www.arealme.com/click-speed-test/fr/')
#time.sleep(1000)

#fonction clicks
def click_Make_Paperclip():
	driver.find_element("xpath",makePaperclip_Id).click()

def click_lower_price():
	driver.find_element("xpath",btnLowerPrice_Id).click()

def click_higher_price():
	driver.find_element("xpath",btnRaisePrice_Id).click()

def click_buy_wire():
	driver.find_element("xpath",buy_wire_Id).click()

def click_buy_autoClipper():
	driver.find_element("xpath",buy_autoclipper_Id).click()






#fonction get info
def get_funds(fundsB):
	try:
		funds = driver.find_element("xpath",funds_Id)
		return float(funds.text.replace(',','.'))
	except:
		return fundsB

def get_price_autoClipper(price_ACB):
	try:
		price_AC = driver.find_element("xpath",autoclipper_cost_Id)
		return float(price_AC.text.replace(',','.'))
	except:
		return price_ACB

def get_lenght_wire_left(wire_leftB):
	try:
		
		wire_left = driver.find_element("xpath",wire_lenght_Id)
		return float(wire_left.text.replace(',',''))
	except:
		return wire_leftB

def get_price_wire(wire_priceB):
	try:
		wire_price = driver.find_element("xpath",wire_price_Id)
		return float(wire_price.text.replace(',','.'))
	except:
		return wire_priceB

def get_nombre_paperclip(nb_paperclipB):
	try:
		nb_paperclip = driver.find_element("xpath",nb_paper_clip_Id)
		return float(nb_paperclip.text.replace(',','.'))
	except:
		return nb_paperclipB


def get_unsold_clip(nb_paperclip_unsoldB):
	try:
		nb_paperclip_unsold = driver.find_element("xpath",nb_unsold_clip_Id)
		return float(nb_paperclip_unsold.text.replace(',',''))
	except:
		return nb_paperclip_unsoldB

def get_margin(marginB):
	try:
		margin = driver.find_element("xpath",margin_id)
		return float(margin.text.replace(',','.'))
	except:
		return marginB






def data_fetcher(lock):
	global nb_paperclip 
	global money 
	global wire_left 
	global price_wire 
	global price_AC
	global margin 
	global unsold_clip
	
	nb_paperclip = 0
	margin = 0
	price_wire = 0
	unsold_clip = 0
	money = 0
	wire_left = 0
	price_AC = 0
	

	while True:
		lock.acquire()
		start_time = time.time()
		price_AC = get_price_autoClipper(price_AC)
		unsold_clip = get_unsold_clip(unsold_clip)
		margin = get_margin(margin)
		price_wire = get_price_wire(price_wire)
		nb_paperclip = get_nombre_paperclip(nb_paperclip)
		money = get_funds(money)
		wire_left = get_lenght_wire_left(wire_left)
		print(f'{price_wire}----------------------------')
		lock.release()
		print("--- data fetch EN %s sec ---\n" % (time.time() - start_time))
		#time.sleep(0.5)


def auto_clicker_make_paperClip():
	#Make_Paperclip=driver.find_element("xpath",makePaperclip_Id)
	#Make_Paperclip.click()
	while True:
		driver.execute_script("clipClick(1)")

def price_ajuster(lock):
	while True:
		lock.acquire()
		start_time = time.time()

		#unsold_clip = get_unsold_clip(unsold_clip)
		#print(unsold_clip)
		#margin = get_margin(margin)
		#print(margin)
		if unsold_clip >= 200 and margin >= 0.02:

			click_lower_price()
			time.sleep(delay)
		if unsold_clip <= 100 and margin <= 0.4:

			click_higher_price()
			time.sleep(delay)
		lock.release()
		print("PRICE AJUSTER--- data fetch EN %s sec ---\n" % (time.time() - start_time))

def bobine_buyer(lock):
	while True:
		
		lock.acquire()
		start_time = time.time()
		#price_wire = get_price_wire(price_wire)
		#money = get_funds(money)
		if price_wire <= 20 and money >= price_wire:
			click_buy_wire()
		lock.release()
		print("--- SPOOL BUYER EN %s sec ---\n" % (time.time() - start_time))
		time.sleep(delay)

def bot_debile_infini(lock):
	while True:
		
		lock.acquire()
		start_time = time.time()
		#click_Make_Paperclip()
		#nb_paperclip = get_nombre_paperclip(nb_paperclip)
		#money = get_funds(money)
		#wire_left = get_lenght_wire_left(wire_left)
		#price_wire = get_price_wire(price_wire)
		print(f'----------------------------{price_wire}')
		if wire_left <= 5000 and money >= price_wire:
			click_buy_wire()
		if driver.find_element("xpath", buy_autoclipper_Id).is_displayed():
			#price_AC = get_price_autoClipper(price_AC)
			if wire_left >= 5000 and money >= price_AC:
				click_buy_autoClipper()
		lock.release()
		time.sleep(delay)
		print("--- BOT DEBILE EN %s sec ---\n" % (time.time() - start_time))


lock = Lock()		
t0 = threading.Thread(target=data_fetcher, name='data fetcher',args=(lock,))
t1 = threading.Thread(target=auto_clicker_make_paperClip, name='auto_clicker')
t2 = threading.Thread(target=bot_debile_infini, name='Bot debile',args=(lock,))
t3 = threading.Thread(target=price_ajuster, name='price ajuster',args=(lock,))
t4 = threading.Thread(target=bobine_buyer, name='bobine buyer',args=(lock,))
#t3 = threading.Thread(target=auto_clicker_make_paperClip, name='auto_clicker2')



#data_fetcher()
#bot_debile_infini()


t0.start()
t1.start()
t2.start()
t3.start()
t4.start()

#t0.join()
#t1.join()
#t2.join()
#t3.join()
#t4.join()


time.sleep(1000)
#bot_debile_infini()
#time.sleep(1000)