'''
File dependencies are in requirements.txt, install using pip install -r requirements.txt .
Please include positive_words.txt in the working directory as well.

Project Quote Generator
The program takes user input of a book title, scrapes that book's description for Goodreads, takes the longest
word from that description, and returns a Goodreads quote to the user that's tagged with that word. If
the user does not provide a title, the script will take a random word from a text file and return
a random tagged quote.

The program moves slowly as it's a lot of Selenium execution. It will default
to showing the Selenium web browser, but this can be turned off by answering
the first prompt to the user. 

Thank you!
'''

from selenium import webdriver
import random
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def soupify(browser):
    '''helper function for converting page to beautiful soup object.'''
    html = browser.page_source
    soup = BeautifulSoup(html, features = 'lxml')
    return soup

def get_recent_read(headless):
    '''
    Takes user input of a book title and scrapes the book description from Goodreads.
    Returns a tuple of the title the user entered and the scraped description.
    '''
    book_title = input("Enter a book you've enjoyed recently, or hit enter for a random quote: ")
    if not book_title:
       return ''
    
    # intialize chrome webdriver
    if headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    else:
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print('Fetching your book from goodreads!')
    browser.get('https://www.goodreads.com/quotes')
    time.sleep(3)
    search = browser.find_element(by=By.XPATH, value="//input[@name='q']")
    search.send_keys(book_title) # search for the book title
    browser.find_element(by=By.XPATH, value = "//button[@aria-label='Search']").click()
    time.sleep(1)
    browser.find_element(by=By.XPATH, value = "//a[@class='bookTitle']").click()
    time.sleep(5)
    soup = soupify(browser)
    # get page contents and find description.
    div = soup.find('div', id = 'description')
    if div:
        spans = div.find_all('span')
        desc_text = spans[1].text
    browser.close()
    return (book_title.title(), desc_text)

def get_word_from_desc(desc):
    '''
    Takes a book description as scraped by get_recent_read. Removes a portion of stopwords, sorts in descending order,
    and returns the longest word from the description. Choosing to return the longest under the surface assumption 
    that a longer word will be more interesting/relevant for later steps.
    '''
    # NLTK would be better for this purpose, but it's a hassle to install, so hard-coding a list of some stopwords instead. 
    stop_words = [ 'we', 'her','of', 'she', 'he', 'stop', 'the', 'to', 'and', 'a', 'in', 'it', 'is', 'i', 'that', 'had', 'on', 'for', 'were', 'was','an','at']
    desc_list = desc.split()
    possible_words = [word.lower() for word in desc_list if word.lower() not in stop_words and word.lower().isalpha()]
    # throw out duplicates and sort
    possible_words = set(possible_words)
    sorted_words = sorted(possible_words, key = len, reverse=True)
    print("Picked a word out from your book's description.")
    return sorted_words[0]

def pick_random_word():
    '''
    This list of positive sentiment words was created by  Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
    Proceedings of the ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
    Washington, USA. They asked that this paper be cited.

    In the case that the user doesn't enter a book title, this function is called instead. 
    It returns a random word from this list of positive sentiment words.  
    '''
    word_list = []
    with open('positive_words.txt','r') as fp:
        for line in fp:
            word_list.append(line.strip())
    word_list = word_list[35:] #remove documentation at beginning of file
    return random.choice(word_list)

def pick_quote(random_word, headless):
    '''
    Takes a word either generated at random or parsed from the user's book selection. 
    Searches Goodreads Quotes for this word and returns the top quote that's tagged with this word. 
    '''
    # intialize chrome webdriver
    if headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) # installs and initializes
    else:
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # installs and initializes
    print("Picking a quote from Goodreads!")
    browser.get('https://www.goodreads.com/quotes')
    time.sleep(3)
    # find search elements
    search = browser.find_element(by=By.XPATH, value="//input[@id='explore_search_query']")
    search.click()
    search.send_keys(random_word)
    browser.find_element(by=By.XPATH, value = "//input[@name='commit']").click()
    time.sleep(4)
    soup = soupify(browser)
    browser.close()
    quotes = soup.find_all('div', class_='quoteText')
    random_quote = quotes[0]
    quote = random_quote.text.strip()
    return(quote)

def main():
    specify_headless = input("Would you like to watch the web scraping run? Type 'y' if you do and 'n' if not. ")
    if specify_headless.lower() in ['n', 'no']:
        headless = True
    else:
        headless = False
    
    user_selection = get_recent_read(headless) # includes tuple of title and extracted description
    if not user_selection:
        # if get_recent_read() returns an empty string, go ahead with generating a random quote
        random_word = pick_random_word()
        quote = pick_quote(random_word, headless)
        print()
        print(f"Your random word is {random_word}.")
        print()
        print(f"And the quote generated by {random_word} is:\n")
        print(quote)
    
    else:
        random_word = get_word_from_desc(user_selection[1])
        quote = pick_quote(random_word, headless)
        print()
        print(f"The word selected from your latest read {user_selection[0]} is {random_word}.")
        print()
        print(f"And the quote generated by {random_word} is:\n")
        print(quote)

if __name__ == "__main__":
    main()