import re
from selenium import webdriver
from beautifulscraper import BeautifulSoup


class GetCurrencies:
    """
    Module responsible for scraping value of currencies from website
    and save it to json file
    """

    # method which includes formula for separation data from DOM about currency value
    @staticmethod
    def separate_value(tag, id_name, soup):
        return (re.search(r'\d[,]\d*', str(soup.find(tag, attrs={'id': id_name}))).group()).replace(',', '.')

    # method collect data from website and save it to json file
    @staticmethod
    def scrap_currencies():
        try:
            # set a new option avoiding open new browser window
            options = webdriver.ChromeOptions()
            options.arguments.append('headless')

            # set browser
            driver = webdriver.Chrome(options=options)

            # go to website
            driver.get('https://www.mybank.pl/')

            # collecting content from website
            content = driver.page_source
            soup = BeautifulSoup(content, features='html.parser')

            # closing browser
            driver.quit()

            # settings values of currencies according downloaded data
            eur = GetCurrencies.separate_value('td', 'EURPLN_NBP', soup=soup)
            usd = GetCurrencies.separate_value('td', 'USDPLN_NBP', soup=soup)
            gbp = GetCurrencies.separate_value('td', 'GBPPLN_NBP', soup=soup)
            nok = GetCurrencies.separate_value('td', 'NOKPLN_NBP', soup=soup)
            chf = GetCurrencies.separate_value('td', 'CHFPLN_NBP', soup=soup)
            btc = re.search(r'>[0-9]*<', str(soup.find('strong', attrs={'id': 'BTC'}))).group().replace('<',
                                                                                                        '').replace(
                '>', '')

            # saving data to json file
            f = open('scraper/currencies.json', 'w+')
            f.write('{' + '"EUR": ' + eur + ',\n'
                    + '"USD": ' + usd + ',\n'
                    + '"GBP": ' + gbp + ',\n'
                    + '"NOK": ' + nok + ',\n'
                    + '"CHF": ' + chf + ',\n'
                    + '"BTC": ' + btc + '\n' + '}')
            f.close()

        except:
            pass


if __name__ == "__main__":
    GetCurrencies.scrap_currencies()
