import tarfile
import platform
import sys
import os.path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# This method checks if a user already has a selenium webdriver installed in the project.
def missing_selenium_driver():
	if platform.system() == 'Windows' and os.path.isfile('bin/selenium-webdriver/geckodriver.exe'):
		return False
	elif (platform.system() == 'Darwin' or platform.system() == 'Linux') and os.path.isfile('bin/selenium-webdriver/geckodriver'):
		return False
	return True

# This method attempts to download the required selenium webdriver for the script to run for the user's system.
def download_selenium_driver():
	platform_being_used = platform.system()
	is_64bits = sys.maxsize > 2**32

	selenium_driver_download = "https://github.com/mozilla/geckodriver/releases/download/v0.29.0/"
	if platform_being_used == 'Linux':
		if is_64bits:
			selenium_driver_download += "geckodriver-v0.29.0-linux64.tar.gz"
		else:
			selenium_driver_download += "geckodriver-v0.29.0-linux32.tar.gz"
	elif platform_being_used == 'Windows':
		if is_64bits:
			selenium_driver_download += "geckodriver-v0.29.0-win64.zip"
		else:
			selenium_driver_download += "geckodriver-v0.29.0-win32.zip"
	elif platform_being_used == 'Darwin':
		selenium_driver_download += "geckodriver-v0.29.0-macos.tar.gz"
	else:
		raise Exception("Your OS isn't supported. Please download the Mozilla geckodriver for your system and place it in the bin/selenium-webdriver\
folder before trying to run the program again.")

	#Download+Extract the firefox(gecko) webdriver that is compatible with the users system:
	ftpstream = urlopen(selenium_driver_download)
	ziptar = None
	if platform_being_used == 'Windows':
		ziptar = ZipFile(BytesIO(ftpstream.read()))
	else:
		ziptar = tarfile.open(fileobj=ftpstream, mode="r|gz")
	
	ziptar.extractall("bin/selenium-webdriver/")

def wait(xpath, timeout=30):
	element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
	return element;

def wait_click(xpath, timeout=30):
	element = wait(xpath, timeout)
	element.click();

def get_driver_executable():
	driver_executable = r"bin/selenium-webdriver/geckodriver"
	if platform.system() == 'Windows':
		driver_executable += ".exe"
	return driver_executable

def initialize_selenium_driver():
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options, executable_path=get_driver_executable())
	print("Webadvisor Saver: Initiated!")
	return driver

#
# Starts here:
#

if missing_selenium_driver():
	print("Webadvisor Saver: Attempting to download Selenium driver required for saving.")
	try:
		download_selenium_driver()
	except (HTTPError, URLError) as e:
		print("ERROR: The link from which we tried to download the Selenium driver from isn't working. Please try again.")
		sys.exit()

driver = initialize_selenium_driver()

curr_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
scrape_output_target = "scripts/webadvisor/webadvisor-courses/scrape-"+curr_time+".html"
os.makedirs(os.path.dirname(scrape_output_target), exist_ok=True)

with open(scrape_output_target, "w") as scrape_output:
	print("Webadvisor Saver: Saved courses will be stored in "+scrape_output_target+"...")

	driver.get("https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?type=M&constituency=WBST&pid=CORE-WBST")
	# Main Student Menu Page:
	wait_click("//*[text() = 'Search for Sections']")

	# Search for Sections Page:
	term_select_xpath = "//select[@id='VAR1']"
	term_select = wait(term_select_xpath)
	term_option_xpath = term_select_xpath+"/option[@value!='']"
	term_options = [term.get_attribute('value') for term in term_select.find_elements_by_xpath(term_option_xpath)]

	print("Webadvisor Saver: Please be patient. We're processing Webadvisor data")

	for idx,term in enumerate(term_options): #term can be any of W21, F25, etc..
		if idx==0:
			scrape_output.write("<html><table id='descriptr-uog-courses'>")
		else:
			wait(term_select_xpath) #If "back" was used on previous loop, wait for page to load.

		wait_click(term_select_xpath+"/option[@value='"+term+"']") # Select W21 term from dropdown
		wait_click("//select[@id='VAR6']/option[@value='G']") # Select Guelph location from dropdown
		wait_click("//input[@value = 'SUBMIT']") # Submit section search form.
		wait("//h1[text()='Section Selection Results']")

		print("Webadvisor Saver: Saving courses in semester "+term+"("+str(idx+1)+" of "+str(len(term_options))+") for further processing.")

		# Section Selection Result page:
		# Wait til the page is done loading
		WebDriverWait(driver, 120).until(lambda driver: driver.execute_script("return document.readyState") == "complete");
		course_rows_html = driver.find_element(By.XPATH, "//div[@id='GROUP_Grp_WSS_COURSE_SECTIONS']/table/tbody").get_attribute('innerHTML')
		scrape_output.write(course_rows_html)

		if idx==len(term_options)-1:
			scrape_output.write("</table></html>")
		else:
			driver.back() #If there's more terms to process, go back.

	scrape_output.close();

driver.quit();
#sys.exit(); # Added to fix bug where the program wasn't quitting.
