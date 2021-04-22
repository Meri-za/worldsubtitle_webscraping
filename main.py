import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class scrap:
    def __init__(self, name):
        self.name = name
    def path(self):
        path = os.getcwd()
        path = os.path.join(path, self.name)
        os.mkdir(path)
        os.chdir(path)
        os.system('clear')
    def main(self):
        path = "https://worldsubtitle.info/"
        driver = webdriver.Chrome('chromedriver', options=self.chrome_options)
        driver.get(path)
        search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='s']")))
        search.clear()
        search.send_keys(self.name)
        search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))).click()
        link = driver.find_element_by_xpath('//*[@title="{}"]'.format(self.name)).click()
        downloads = driver.find_elements_by_link_text('دانلود با لینک مستقیم')
        self.downloads = [links.get_attribute('href') for links in downloads]
    def request(self):
        counter = 1
        print("< -- Yay I Found it , Wait To Download Starting -- >")
        for links in self.downloads:
            response = requests.get(links, allow_redirects=True)
            type = response.headers['Content-Type']
            if type == "application/x-rar-compressed":
                with open ('{}-{}.rar'.format(self.name , counter), 'wb') as f:
                    f.write(response.content)
                    print(response.request.url,">>",response.status_code)
                    counter += 1
            else:
                with open ('{}-{}.zip'.format(self.name , counter), 'wb') as f:
                    f.write(response.content)
                    print(response.request.url,">>",response.status_code)
                    counter += 1
    def headless(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')


name = input("Type Name (Ex:: Movie >> Avatar 2009 , series >> Supernatural)>").title()
print("< -- Wait to Find the MOvie -- >")
app = scrap(name)
app.headless()
app.main()
app.path()
app.request()