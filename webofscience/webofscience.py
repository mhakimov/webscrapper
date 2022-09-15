import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from webofscience.article_filtering import ArticleFiltering
from webofscience.csv_utils import CsvUtils
from webofscience.scrapping import Scrappy

import constants as const

class Webofscience(webdriver.Chrome):

    def __init__(self, switchoff=True):
        self.chrome_path = os.path.join(const.ROOT_DIR, const.CHROMEDRIVER)
        self.switchoff = switchoff
        self.authors = []
        options = webdriver.ChromeOptions()
        #this argument is needed to skip 2-factor authentication step
        options.add_argument(f"user-data-dir={const.CHROME_SUPPORT_FOLDER}")
        options.headless = True
        super(Webofscience, self).__init__(self.chrome_path, chrome_options=options)
        self.implicitly_wait(20)

    def __enter__(self):
        print("Entering")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.switchoff:
            self.quit()

    def land_libguides_page(self):
        self.get(const.LIBGUIDES_URL)

    def navigate_to_webofscience(self):
        lnk_web_of_science = self.find_element(By.CSS_SELECTOR,
                                                      "#s-lg-content-14267618 > p:nth-child(5) > a > span")
        lnk_web_of_science.click()
        self.switch_to.window(self.window_handles[1])


    def search_for_theme(self, theme):
        txf_research_field = self.find_element(By.ID, "mat-input-0")
        txf_research_field.send_keys(theme)
        btn_search = self.find_element(By.XPATH, "//*[@id='snSearchType']/div[3]/button[2]")
        self.execute_script("arguments[0].click();", btn_search)

    def start_from(self, url):
        self.get(url)


    def apply_filtering(self):
        filtering = ArticleFiltering(driver=self)
        filtering.apply_year_filter(['2020', '2021', '2022', '2023'])
        filtering.populate_countries()

    def read_old_csv(self, filename):
        reading = CsvUtils()
        existing_list = reading.read_csv(filename)
        return existing_list

    def collect_authors_info(self):
        old_list = self.read_old_csv(const.GENERATED_RECORDS_FILE)
        collecting = Scrappy(self)
        collecting.get_authors_info(old_list, self.authors)
        self.create_csv(self.authors, 'new_csv.csv')


    def create_csv(self, authors, filename):
        csv = CsvUtils()
        csv.write_csv(authors, filename)


