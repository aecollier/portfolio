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
    html = browser.page_source
    browser.close()
    return random_word, html

def pick_quote(html):
    soup = BeautifulSoup(html, features = 'lxml')
    quotes = soup.find_all('div', class_='quoteText')
    random_int = random.randint(0,19)
    random_quote = quotes[random_int]
    quote = random_quote.text
    print(quote)
    with open('daily_quote.txt','w', encoding="utf-8") as fp:
        fp.write(quote)
    return(quote)


def send_email(random_word, quote):
    reciever = input("Please enter your email address, or hit enter to print today's quote! ")
    if reciever:
        with open('daily_quote.txt', 'r', encoding="utf-8") as fp:
            msg = EmailMessage()
            msg.set_content(fp.read())
        msg['Subject'] = f"Today's word is {random_word}"
        msg['From'] = 'dailyquotesac@gmail.com'
        msg['To'] = reciever
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()
    else:
        print(f"Today's word is {random_word}")
        print()
        print("And today's quote is: ")
        print(quote)



def main():
    random_word, html = pick_word()
    quote = pick_quote(html)
    send_email(random_word, quote)


    # print("Your word was: "+random_word)
    # print()
    # print("Your quote was: ")
    # print(pick_quote(html))
if __name__ == "__main__":
    main()