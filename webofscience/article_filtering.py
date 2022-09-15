from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time


class ArticleFiltering:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_year_filter(self, years):
        for year in years:
            self.tick_year_chb(year)
        self.click_refine_years()

    def tick_year_chb(self, year):
        chb_year = self.driver.find_element(By.XPATH, f"//*[@value='PY.{year}']/parent::*")
        chb_year.click()

    def click_refine_years(self):
        btn_refine = self.driver.find_element(By.XPATH,
                                              "//*[@id='filter-section-PY']/div/div/div/button[3]")
        btn_refine.click()

    def populate_countries(self):
        self.driver.find_element(By.CSS_SELECTOR, "#filter-section-CU > button").click()
        self.driver.find_element(By.XPATH, "//*[@id='filter-section-CU']/div//button[1]/span[1]").click()

        countries = ["ARGENTINA", "AUSTRALIA", "AUSTRIA", "BELGIUM", "CYPRUS", "CZECH REPUBLIC", "USA", "SINGAPORE",
                     "SOUTH KOREA", "TAIWAN", "TURKEY", "NORTH IRELAND", "ENGLAND", "CANADA", "GERMANY", "ITALY", "SPAIN",
                 "JAPAN", "FRANCE", "POLAND", "NETHERLANDS", "PORTUGAL", "SWEDEN", "DENMARK", "FINLAND", "MOROCCO", "NORWAY",
                   "GREECE",  "SCOTLAND", "SWITZERLAND", "ROMANIA", "IRELAND", "JORDAN",
                 "WALES", "NEW ZEALAND", "LUXEMBOURG",  "ESTONIA", "UKRAINE", "KUWAIT", "LATVIA", "LITHUANIA", "MEXICO",
                 "SLOVENIA", "UZBEKISTAN", "PALESTINE"]
        for country in countries:
            self.driver.find_element(By.XPATH, f"//*[@value='CU.{country}']/parent::*").click()
        time.sleep(1)
        btn_refine_countries = self.driver.find_element(By.XPATH, "/html/body/app-wos/main//div[2]//div[2]/app-refine-see-all-shared//div[8]/button[3]/span[1]")
        self.driver.execute_script("arguments[0].click();", btn_refine_countries)

