from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import options
from selenium.webdriver.support.wait import WebDriverWait


# TODO:
# Añadir un timeout error except para cuada uno de los waits
# Añadir el headlessly
url = 'www.apothekenindex.at'


type(options)

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://selenium.dev")


driver.quit()

help(webdriver)
