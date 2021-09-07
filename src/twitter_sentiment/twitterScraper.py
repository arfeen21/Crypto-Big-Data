import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions
from selenium.webdriver import Chrome
import time
import pandas as pd

#imports from other folders
from bd3.src.twitter_sentiment.twitterdata.extract_twitterdata import getdata_from_tweet
from bd3.src.twitter_sentiment.login.login import login_to_twitter 
from bd3.src.twitter_sentiment.search_and_filter.filterData import find_search_input_and_enter_criteria,change_page,generate_tweet_id
from bd3.src.twitter_sentiment.scrollfunction.scroll import scroll_page

driver = Chrome()



'''
hier wordt de data opgeslagen in een csv file , maar het kan beter door pandas te gebruiken i.p.v csv
'''
def save_tweet_data_to_csv(records, filepath, mode='a+'):
    header = ['User', 'Handle', 'PostDate', 'TweetText','LikeCount']
    with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(header)
        if records:
            writer.writerow(records)


'''
hier worden de tweets van de view gepakt
'''
def collect_all_tweets_from_current_view(driver, lookback_limit=25):
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    if len(page_cards) <= lookback_limit:
        return page_cards
    else:
        return page_cards[-lookback_limit:]


'''
hier worden alle methodes aangeroepen
'''
def main(username, password, search_term, filepath, page_sort='Latest'):
    save_tweet_data_to_csv(None, filepath, 'w')  # create file for saving records
    last_position = None
    end_of_scroll_region = False
    unique_tweets = set()

    driver 
    logged_in = login_to_twitter(username, password, driver)
    if not logged_in:
        return
    time.sleep(3)

    search_found = find_search_input_and_enter_criteria(search_term, driver)
    if not search_found:
        return

    change_page(page_sort, driver)

    while not end_of_scroll_region:
        cards = collect_all_tweets_from_current_view(driver)
        for card in cards:
            try:
                tweet = getdata_from_tweet(card)
            except exceptions.StaleElementReferenceException:
                continue
            if not tweet:
                continue
            tweet_id = generate_tweet_id(tweet)
            if tweet_id not in unique_tweets:
                unique_tweets.add(tweet_id)
                save_tweet_data_to_csv(tweet, filepath)
        last_position, end_of_scroll_region = scroll_page(driver, last_position)
    driver.quit()



#wachtwoord en path naar de csv
if __name__ == '__main__':
    usr = "AnalysisBd3"
    pwd = "BigData01"
    path = 'test.csv'
    advancedSearchbar = '(from:elonmusk) lang:en until:2021-03-31 since:2020-10-01 -filter:links -filter:replies'

    main(usr, pwd, advancedSearchbar, path)



#hier zet je het om naar een mooiere dataframe , die we wat beter kunnen begrijpen/gebruiken
import pandas as pd
df = pd.read_csv(r'C:\Users\Arfeen\Documents\ProjectBD\test.csv')

df = pd.DataFrame(df)
df.head(1)

df.to_csv('mooietest.csv')
