from bs4 import BeautifulSoup
import requests
import re
from stop_words import get_stop_words
from wikiscraper.constants import WIKI_API_LINK, WIKI_LINK


# get the words
def get_word_list(url):
    word_list = []
    # raw data
    source_code = requests.get(url)
    # convert to text
    plain_text = source_code.text
    # lxml format
    soup = BeautifulSoup(plain_text, 'lxml')

    # find the words in paragraph tag
    for text in soup.findAll('p'):
        if text.text is None:
            continue
        # content
        content = text.text
        # lowercase and split into an array
        words = content.lower().split()

        # for each word
        for word in words:
            # remove non-chars
            cleaned_word = clean_word(word)
            # if there is still something there
            if len(cleaned_word) > 0:
                # add it to our word list
                word_list.append(cleaned_word)

    return word_list


# clean word with regex
def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+', '', word)
    return cleaned_word


def create_frequency_table(word_list):
    # word count
    word_count = {}
    for word in word_list:
        # index is the word
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count


# remove stop words
def remove_stop_words(frequency_list):
    stop_words = get_stop_words('en')

    temp_list = []
    for key, value in frequency_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list
