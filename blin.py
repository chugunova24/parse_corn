from selenium import webdriver
from selenium_stealth import stealth
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")


ip_addr = ''
port = ''
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = "ip_addr:port"
prox.socks_proxy = "ip_addr:port"
prox.ssl_proxy = "ip_addr:port"
capabilities = DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)


options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=r"C:\Projects\parse_corn_bot\chromedriver.exe", \
                          desired_capabilities=capabilities)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )



URL = '''https://www.reuters.com/site-search/?query=a&date=past_24_hours&offset=0&section=all'''
# --ЕСТЬ, НО НЕТ--
# '''//div[contains(text(), ":")][not(contains(text(), ","))]'''
# проверка содержания ссылок  -- //*[contains(@href ,'nomika/13175455')]
xPATH = '''//div[@class="MediaStoryCard__body___1Iz8IK"]/a'''
xPATH_link = '''//div[@class="MediaStoryCard__body___1Iz8IK"]/a/@href'''

driver.get(URL)
time.sleep(5)
driver.execute_script("window.stop();")
print('window stop')
agent = driver.execute_script("return navigator.userAgent")
print(agent)
# ищет новости на сегодня
cell_news_arr = []
cell_news = driver.find_elements(By.XPATH, xPATH)
for i in cell_news:
        cell_news_arr.append(i.text)
print(cell_news_arr)

time.sleep(5)
driver.quit()