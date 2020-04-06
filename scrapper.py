from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd


def get_links(row):
    classes = row.get_attribute('class').split(' ')
    if(any(True for item in classes if item in products)):
        first_td = row.find_element_by_tag_name('td')
        row_anchor = first_td.find_element_by_tag_name('a')
        return [row_anchor.get_attribute('href')]
    return []


url = 'http://www.apothekenindex.at'
products = ['productListing-odd', 'productListing-even']
results = pd.DataFrame(
    columns=['Name', 'Address', 'Tel', 'Fax', 'Email', 'Schedule', 'Link'])
options = Options()
options.page_load_strategy = 'eager'
# options.set_headless(False)
driver = WebDriver(ChromeDriverManager().install(), options=options)
driver.get(url)

# step 1) get all states links
table = driver.find_element_by_class_name('infoBoxContents')
states = table.find_elements_by_class_name('parent')
states_links = []

for state in states:
    state_list = state.find_element_by_tag_name('ul')
    state_anchors = state_list.find_elements_by_tag_name('a')
    states_links += [a.get_attribute('href')
                     for a in state_anchors if a.get_attribute('title') == '']

# Step 2) get all pharmacies links
pharmacies_links = []
for state_link in states_links:
    page = state_link
    has_next = True
    while has_next is True:
        driver.get(page)

        product_table = WebDriverWait(driver, 5).until(
            lambda e: e.find_element_by_class_name('productListing'))

        # Skip first row which is the header
        rows = product_table.find_elements_by_tag_name('tr')[1:]
        for row in rows:
            pharmacies_links += get_links(row)

        next_page_links = driver.find_elements_by_class_name('pageResults')
        has_next = False
        for next_page_link in next_page_links:
            if(next_page_link.get_attribute('title') == ' nächste Seite '):
                page = next_page_link.get_attribute('href')
                has_next = True

# Step 3) get all pharmacies information
telephone_re = re.compile(r'Tel\:\s{0,}(.*)')
fax_re = re.compile(r'Fax\:\s{0,}(.*)')
email_re = re.compile(r'mailto\:(.*)')
address_condition = "//*[text()='Adresse']//following::p"
contact_condition = "//*[text()='Kontakt']//following::p"

for pharmacy in pharmacies_links:
    # driver.get(pharmacy)
    driver.get(pharmacy)
    try:
        name = WebDriverWait(driver, 5).until(
            lambda b: b.find_element_by_class_name('apodetail').text)
    except Exception as e:
        name = ''
        print(pharmacy, 'no Name')
        print(e)

    try:
        address_info = WebDriverWait(driver, 5).until(
            lambda b: b.find_elements_by_xpath(address_condition))[0:2]

        address = '\n'.join([x.get_attribute('textContent').strip(' ')
                             for x in address_info
                             if x.get_attribute('textContent').strip(' ')
                             != ''])
    except Exception as e:
        address = ''
        print(pharmacy, 'no address')
        print(e)

    try:
        contact_info = WebDriverWait(driver, 5).until(
            lambda b: b.find_elements_by_xpath(contact_condition))[0:3]
    except Exception as e:
        print(pharmacy, 'no contact info')
        print(e)

    try:
        tel = telephone_re.match(
            contact_info[0].get_attribute('textContent')).group(1)
    except Exception as e:
        tel = ''
        print(pharmacy, ': No Tel')
        print(e)

    try:
        fax = fax_re.match(
            contact_info[1].get_attribute('textContent')).group(1)
    except Exception as e:
        fax = ''
        print(pharmacy, ': No Fax')
        print(e)
        pass

    try:
        email_string = contact_info[2].find_element_by_tag_name(
            'a').get_attribute('href')
        email = email_re.match(email_string).group(1)
    except Exception as e:
        email = ' '
        print(pharmacy, ': No Email')
        print(e)

    try:
        schedule_table = driver.find_element_by_xpath(
            "//*[text()='Öffnungszeiten']//following::table")

        table_rows = schedule_table.find_elements_by_tag_name('tr')

        schedule = dict()
        for row in table_rows:
            td = row.find_elements_by_tag_name('td')
            schedule[td[0].get_attribute(
                'textContent')] = td[1].get_attribute('textContent')
    except Exception as e:
        schedule = ''
        print(pharmacy, ': No Schedule')
        print(e)

    results.loc[len] = [name, address, tel, fax, email, schedule, pharmacy]
