from selenium import webdriver
import random
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage

def pos_words():
    '''This list of positive sentiment words was created by 
        Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
        Proceedings of the ACM SIGKDD International Conference on Knowledge 
        Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
        Washington, USA. They asked that this paper be cited.'''
    word_list = []
    with open('positive_words.txt','r') as fp:
        for line in fp:
            word_list.append(line.strip())
    return word_list[35:] #remove documentation at beginning of file

def pick_word():
    browser = webdriver.Chrome(executable_path=r'C:/Users/abiga/Documents/AVC/chromedriver.exe')
    browser.get('https://www.goodreads.com/quotes')
    time.sleep(3)
    search = browser.find_element_by_xpath("//input[@id='explore_search_query']")
    random_word = random.choice(pos_words())
    search.click()
    search.send_keys(random_word)
    browser.find_element_by_xpath("//input[@name='commit']").click()
    time.sleep(4)
    #random_word = 'jubilant'
    #browser.get('https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=jubilant&commit=Search')
    html = browser.page_source
    browser.close()
    return random_word, html

def pick_quote(html):
    soup = BeautifulSoup(html, features = 'lxml')
    quotes = soup.find_all('div', class_='quoteText')
    random_int = random.randint(0,19)
    random_quote = quotes[random_int]
    author = random_quote.find('span', class_='authorOrTitle')
    work = random_quote.find('a', class_='authorOrTitle')
    quote_extras = random_quote.text.strip().split('―')
    quote = quote_extras[0]+'\n ―'
    if author:
        quote += ' '+author.text.strip()
    if work:
        quote += ' '+work.text.strip()
    return(quote)

def get_recent_read():
    #title = input("Enter a book you've enjoyed recently, or hit enter for a random quote: ")
    #if not title:
    #    return ''
    title = 'dune'
    browser = webdriver.Chrome(executable_path=r'C:/Users/abiga/Documents/AVC/chromedriver.exe')
    browser.get('https://www.amazon.com/')
    time.sleep(3)
    # first set search parameters to books because that's what we're after
    filter_books = browser.find_element_by_xpath("//select[@id='searchDropdownBox']")
    filter_books.click()
    browser.find_element_by_xpath("//option[@value='search-alias=stripbooks']").click()
    time.sleep(3)

    searchbar = browser.find_element_by_xpath("//input[@id='twotabsearchtextbox']")
    searchbar.send_keys(title.strip())
    browser.find_element_by_xpath("//input[@id='nav-search-submit-button']").click()
    time.sleep(5)
    browser.find_element_by_xpath("//div[@cel_widget_id='MAIN-SEARCH_RESULTS-2']").click()
    time.sleep(5)
    browser.close()

    



def main():
    get_recent_read()
    # if not user_selection:
    #     # if get_recent_read() returns an empty string, go ahead with generating a random quote
    #     random_word, html = pick_word()
    #     quote = pick_quote(html)
    #     print(f"Today's word is {random_word}.")
    #     print()
    #     print("And today's quote is:\n")
    #     print(quote)
    
    # else:


    # print("Your word was: "+random_word)
    # print()
    # print("Your quote was: ")
    # print(pick_quote(html))
if __name__ == "__main__":
    main()