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



def init_browser(no_show):
    '''
    Helper function for setting up a webdriver.
    Parameters:
        no_show: a boolean representing whether or not the user wants to see the web scraper run
    '''
    if no_show:
        # if the user doesn't want to watch the scraper run, we set the driver to headless, so no window pops up. 
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    else:
        # otherwise, invoke webdriver which defaults to showing the window as it scrapes.
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return browser

def soupify(browser):
    '''
    Helper function for converting page to beautiful soup object.
    Parameters:
        browser: a selenium webdriver instance 
    '''
    html = browser.page_source
    soup = BeautifulSoup(html, features = 'lxml')
    return soup

def get_recent_read(no_show):
    '''
    Asks for user input of a book title and scrapes the book description from Goodreads.
    Returns a tuple of the title the user entered and the scraped description, if the user provides
    a book title, else it returns an empty string.
    Parameters:
        no_show: a boolean representing whether or not the user wants to see the web scraper run
    '''
    book_title = input("Enter the title of a book you've enjoyed recently, or hit enter for a random quote: ")
    if not book_title:
       return ''
    
    # initialize chrome webdriver
    browser = init_browser(no_show)
    print('Fetching your book from goodreads!')
    browser.get('https://www.goodreads.com/quotes')
    time.sleep(3) # Ensure page loads

    # Find search elements
    search_input = browser.find_element(by = By.XPATH, value = "//input[@name='q']")
    submit_button = browser.find_element(by=By.XPATH, value = "//button[@aria-label='Search']")

    # Input book title and click search icon
    search_input.send_keys(book_title) 
    submit_button.click()
    time.sleep(2)

    # Once on new page, click on the first book title
    browser.find_element(by=By.XPATH, value = "//a[@class='bookTitle']").click()
    time.sleep(5)

    # turn browser html into a Beautiful soup object for further parsing.
    soup = soupify(browser)
    # get page contents and find description.
    div = soup.find('div', id = 'description')
    if div:
        spans = div.find_all('span') # the book description lives in a series of spans
        desc_text = spans[1].text # the second one has the information I want. 
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
    In the case that the user doesn't enter a book title, this function is called instead. 
    It returns a random word from a file of positive words.  

    This list of positive sentiment words was created by  Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
    Proceedings of the ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
    Washington, USA. They asked that this paper be cited.
    '''
    word_list = []
    with open('positive_words.txt','r') as fp:
        for line in fp:
            word_list.append(line.strip())
    word_list = word_list[35:] #remove documentation at beginning of file
    return random.choice(word_list)

def pick_quote(random_word, no_show):
    '''
    Takes a word either generated at random or parsed from the user's book selection. 
    Searches Goodreads Quotes for this word and returns the top quote that's tagged with this word. 
    Parameters:
        no_show: a boolean representing whether or not the user wants to see the web scraper run
    Returns: string representing a quote scraped from Goodreads. 
    '''
    # intialize chrome webdriver
    browser = init_browser(no_show)
    print("Picking a quote from Goodreads!")
    browser.get('https://www.goodreads.com/quotes')
    time.sleep(3) # ensure page loads
    
    # find search elements
    search_input = browser.find_element(by=By.XPATH, value="//input[@id='explore_search_query']") # even though this looks similar to the function above, the elements are named differently so have to do it again. 
    submit_button = browser.find_element(by=By.XPATH, value = "//input[@name='commit']")

    # send word and click submit button
    search_input.click().send_keys(random_word)
    submit_button.click()
    time.sleep(4)

    # get page html and extract quote
    soup = soupify(browser)
    browser.close() 
    quotes = soup.find_all('div', class_='quoteText')
    quote = quotes[0].text.strip()
    return(quote)

def main():
    specify_no_show = input("Would you like to watch the web scraper run? Type 'y' if you do and 'n' if not. ")
    if specify_no_show.lower() in ['n', 'no']:
        no_show = True
    else:
        no_show = False # if users says yes or nothing, the scraper will display windows as it scrapes
    
    user_selection = get_recent_read(no_show) # tuple of book title and desc, if given
    if not user_selection:
        # if get_recent_read() returns an empty string, go ahead with generating a random quote
        random_word = pick_random_word()
        quote = pick_quote(random_word, no_show)
        print(f"\nYour random word is {random_word}.")
        print(f"\nAnd the random quote generated by {random_word} is:\n")
        print(quote)
    
    else:
        desc_word = get_word_from_desc(user_selection[1]) 
        quote = pick_quote(desc_word, no_show)
        print(f"\nThe word selected from your latest read {user_selection[0]} is {desc_word}.")
        print(f"\nAnd the random quote generated by {desc_word} is:\n")
        print(quote)

if __name__ == "__main__":
    main()