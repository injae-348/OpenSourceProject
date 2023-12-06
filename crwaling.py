import sys
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
        self.driver.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%A0%84%EB%82%A8%EB%8C%80")
       
    def search(self, breed) :
        s_input = self.driver.find_element(By.XPATH, "//input[@id='nx_query']")
        s_input.clear()

        if breed == 'cat-Abyssinian' :
            s_input.send_keys("아비니시안 고양이")
        elif breed == 'cat-Bengal' :
            s_input.send_keys("벵갈 고양이")
        elif breed == 'cat-Birman' :
            s_input.send_keys("버먼 고양이")
        elif breed == 'cat-Bombay' :
            s_input.send_keys("봄베이 고양이")
        elif breed == 'cat-British_Shorthair' :
            s_input.send_keys("브리티시 쇼트헤어 고양이")
        elif breed == 'cat-Egyptian_Mau' :
            s_input.send_keys("이집션 마우 고양이")
        elif breed == 'cat-Maine_Coon' :
            s_input.send_keys("메인쿤 고양이")
        elif breed == 'cat-Persian' :
            s_input.send_keys("페르시안 고양이")
        elif breed == 'cat-Ragdoll' :
            s_input.send_keys("랙돌 고양이")
        elif breed == 'cat-Russian_Blue' :
            s_input.send_keys("러시안 블루 고양이")
        elif breed == 'cat-Siamese' :
            s_input.send_keys("샴 고양이")
        elif breed == 'cat-Sphynx' :
            s_input.send_keys("스핑크스 고양이")
        elif breed == 'dog-american_bulldog' :
            s_input.send_keys("아메리칸 불독")
        elif breed == 'dog-american_pit_bull_terrier' :
            s_input.send_keys("아메리칸 핏불 테리어")
        elif breed == 'dog-basset_hound' :
            s_input.send_keys("바셋 하운드")
        elif breed == 'dog-beagle' :
            s_input.send_keys("비글")
        elif breed == 'dog-boxer' :
            s_input.send_keys("복서")
        elif breed == 'dog-chihuahua' :
            s_input.send_keys("치와와")
        elif breed == 'dog-english_cocker_spaniel' :
            s_input.send_keys("잉글리시 코커 스패니얼")
        elif breed == 'dog-english_setter' :
            s_input.send_keys("르웰린")
        elif breed == 'dog-german_shorthaired' :
            s_input.send_keys("저먼 쇼트헤어드 포인터")
        elif breed == 'dog-great_pyrenees' :
            s_input.send_keys("그레이트 피레니즈")
        elif breed == 'dog-havanese' :
            s_input.send_keys("하바나")
        elif breed == 'dog-japanese_chin' :
            s_input.send_keys("제페니스 친")
        elif breed == 'dog-keeshond' :
            s_input.send_keys("키스혼드")
        elif breed == 'dog-leonberger' :
            s_input.send_keys("레온베르거")
        elif breed == 'dog-miniature_pinscher' :
            s_input.send_keys("미니어처 핀셔")
        elif breed == 'dog-newfoundland' :
            s_input.send_keys("뉴펀들랜드")
        elif breed == 'dog-pomeranian' :
            s_input.send_keys("포메라니안")
        elif breed == 'dog-pug' :
            s_input.send_keys("퍼그")
        elif breed == 'dog-saint_bernard' :
            s_input.send_keys("세인트 버나드")
        elif breed == 'dog-samoyed' :
            s_input.send_keys("사모예드")
        elif breed == 'dog-scottish_terrier' :
            s_input.send_keys("스코티시 테리어")
        elif breed == 'dog-shiba_inu' :
            s_input.send_keys("시바 이누")
        elif breed == 'dog-staffordshire_bull_terrier' :
            s_input.send_keys("스타포드셔 불 테리어")
        elif breed == 'dog-wheaten_terrier' :
            s_input.send_keys("휘튼 테리어")
        elif breed == 'dog-yorkshire_terrier' :
            s_input.send_keys("요크셔테리어")
        else :
            print("검색할 수 없는 품종입니다.")
            return

        s_input.send_keys(Keys.ENTER)
        news_titles = self.driver.find_elements(By.XPATH, "//a[@class='news_tit']")
        for index, value in enumerate(news_titles):
            print(f"{index+1} : {value.text} [link : {value.get_attribute('href')}]")
            if index == 4:
                break
        pass
    

if __name__ == "__main__":
    breed = sys.argv[1]
    c = CRAWLING()
    c.main()
    #while True:    #반복문 사용하려면 input~~ 줄과 c.search~~줄을 while문에 맞출 것
    # input_data = input("원하는 품종을 입력해 주세요. : ")
    # c.search(input_data)
    c.search(breed)

