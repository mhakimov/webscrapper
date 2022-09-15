import time
from webofscience.author import Author
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class Scrappy:
    def __init__(self, driver):
        self.driver = driver


    def get_authors_info(self, old_list, authors):
        try:
            url = self.driver.current_url
            url_start = url[0:123]
            domain = url[0:48]
            self.collect_info_from_all_pages(url_start, domain, old_list, authors)
        except Exception as e:
            print(e)
            return authors


    def collect_info_from_all_pages(self, url_start, domain, old_list, authors):
        for i in range(136, 150):
            if i > 1:
                self.driver.get(url_start + str(i))
            time.sleep(5)
            self.scroll_down_screen(18)
            articles_page = self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            soup = BeautifulSoup(articles_page, 'lxml')
            articles_section = soup.find('app-records-list', class_='app-records-list')
            links = []
            if articles_section is not None:
                link_elements = articles_section.findAll('a', class_='title title-link font-size-18 ng-star-inserted')
                for le in link_elements:
                    links.append(le['href'])

            self.collect_info_from_all_records_on_page(link_elements, domain, links, old_list, authors, i)
            if len(authors) > 1500:
                return authors


    def collect_info_from_all_records_on_page(self, link_elements, domain, links, old_list, new_list, i):
        for j in range(1, len(link_elements)):
            time.sleep(1)
            self.driver.get(domain + links[j])
            article_page = self.driver.page_source
            soup = BeautifulSoup(article_page, 'lxml')
            main_article = soup.find('div', id='snMainArticle')
            self.append_authors(main_article, old_list, new_list, i, j)
        return new_list

    def append_authors(self, main_article, old_list, authors, i, j):
        if main_article == None:
            return
        article_name = main_article.find('h2', id='FullRTa-fullRecordtitle-0').text
        publication_date_el = main_article.find('span', id='FullRTa-pubdate')
        if publication_date_el == None:
            publication_date = ''
        else:
            publication_date = publication_date_el.text

        email_elements = main_article.findAll('a', cdxanalyticscategory='wos-author-email-addresses')
        for ee in email_elements:
            if any(author.email == ee.text for author in old_list):
                print(f'{i} {j} {ee.text} exists in the old list')
            elif any(author.email == ee for author in authors):
                print(f'{i} {j} {ee.text} exists in the current list')
            elif ee.text.endswith('.cn'):
                print((f'{i} {j} {ee.text} domain is in .cn'))
            elif ee.text.endswith('.in'):
                print((f'{i} {j} {ee.text} domain is in .in'))
            else:
                authors.append(Author(ee.text, article_name, publication_date))



    def scroll_down_screen(self, times):
        y = 1000
        for timer in range(0, times):
            self.driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 1000
            time.sleep(1.5)


    def click_record(self, index):
        lnk_record = self.driver.find_element(By.CSS_SELECTOR, f"app-record:nth-child({index}) div:nth-child(1) > app-summary-title > h3 > a")
        lnk_record.click()





