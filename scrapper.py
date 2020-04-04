import re
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def get_links(row):
    classes = row.get_attribute('class').split(' ')
    if(any(True for item in classes if item in products)):
        first_td = row.find_element_by_tag_name('td')
        row_anchor = first_td.find_element_by_tag_name('a')
        return [row_anchor.get_attribute('href')]

    return []


url = 'http://www.apothekenindex.at'
products = ['productListing-odd', 'productListing-even']

# TODO:
# Añadir un timeout error except para cuada uno de los waits

options = Options()
options.page_load_strategy = 'eager'

# TODO: remove the comentary
# options.set_headless(False)

driver = WebDriver(ChromeDriverManager().install(), options=options)
driver.get(url)

# paso 1) obtener todos los links

table = driver.find_element_by_class_name('infoBoxContents')
states = table.find_elements_by_class_name('parent')
links = []

for state in states:
    state_list = state.find_element_by_tag_name('ul')
    state_anchors = state_list.find_elements_by_tag_name('a')
    links += [a.get_attribute('href')
              for a in state_anchors if a.get_attribute('title') == '']

pharmacies_links = []

for link in links:
    driver.get(link)
    product_table = WebDriverWait(driver, 5).until(
        lambda e: e.find_element_by_class_name('productListing'))

    # Skip first row which is the header
    rows = product_table.find_elements_by_tag_name('tr')[1:]
    for row in rows:
        classes = row.get_attribute('class').split(' ')
        if(any(True for item in classes if item in products)):
            first_td = row.find_element_by_tag_name('td')
            row_anchor = first_td.find_element_by_tag_name('a')
            pharmacies_links += [row_anchor.get_attribute('href')]


len(pharmacies_links)

# troublshooting
locations = []
regular_exp = r'http\:\/\/.*?\/.*?\/(.*)?\/(.*)?\/.*'
p = re.compile(regular_exp)
for l in pharmacies_links:
    m = p.match(l)
    if (m.group(1) == 'oberoesterreich' or m.group(1) == 'steiermark'):
        locations += [m.group(2)]

locations
data = pd.DataFrame(locations, columns=['locations'])
print(data.groupby('locations').size())

# driver.quit()
