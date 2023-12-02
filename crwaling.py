from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By


class CRAWLING:
    def __init__(self) -> None:
        self.init_driver()

    def init_driver(self):
        self.chrome_service = Service(ChromeDriverManager().install())
        self.driver = None

    def main(self):
        self.driver = webdriver.Chrome(service=self.chrome_service)
        self.driver.get("https://naver.com")
        s_input = self.driver.find_element(By.XPATH, "//input[@id='query']")

        s_input.send_keys("리트리버")
        s_input.send_keys(Keys.ENTER)
        self.driver.find_element(By.XPATH, "//div[@class='btn_next _next']").click()
        self.driver.find_elements(By.XPATH, "//div[@class='flick_bx']")[6].click()

        news_titles = self.driver.find_elements(By.XPATH, "//a[@class='news_tit']")
        for index, value in enumerate(news_titles):
            print(f"{index+1} : {value.text}")
        pass


if __name__ == "__main__":
    c = CRAWLING()
    c.main()
