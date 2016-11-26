from bs4 import BeautifulSoup
import requests
import re
import operator
import json
from tabulate import tabulate
import sys
from stop_words import get_stop_words


# get data from wikipedia

wiki_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wiki_link = "https://en.wikipedia.org/wiki/"

# evaluate the user input
if len(sys.argv) < 2:
    print("Enter a valid string")
    exit()

# get the search word
string_query = sys.argv[1]

if len(sys.argv) > 2:
    search_mode = True
else:
    search_mode = False

# create our url
url = wiki_api_link + string_query


def get_word_list(url_link):
    word_list = []
    # raw data
    source_code = requests.get(url=url_link)

    # convert to text
    plain_text = source_code.text

    # lxml format
    soup = BeautifulSoup(plain_text, "lxml")

    # find words in paragraphs
    for text in soup.findAll("p"):
        if text.text is None:
            continue
        # content
        content = text.text

        # lower case and split to array
        words = content.lower().split()

        # for each word, remove non-characters, if there is still something there, add to our word list
        for word in words:
            cleaned_words = clean_word(word)
            if len(cleaned_words) > 0:
                word_list.append(cleaned_words)

    return word_list


def clean_word(word):
    cleaned_word = re.sub("[A-Za-z]", "", word)
    return cleaned_word


def create_freq_table(word_list):
    word_count = {}
    for word in word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


def remove_stop_words(frequency_list):
    stop_words = get_stop_words(language="en")
    temp_list = []
    for key, value in frequency_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list

try:
    response = requests.get(url=url)
    data = json.loads(response.content.decode('utf-8'))

    # format this data
    wiki_page_tag = data["query"]["search"][0]["title"]

    # create our new url
    url_link = wiki_link + wiki_page_tag
    page_word_list = get_word_list(url)

    # create table of word count
    page_word_count = create_freq_table(page_word_list)
    sorted_word_freq_list = sorted(page_word_count.items, key=operator.itemgetter(1), reverse=True)

    # remove stop words
    if search_mode:
        sorted_word_freq_list = remove_stop_words(sorted_word_freq_list)

    # sum the total words to calculate the frequencies
    total_words = 0
    for key, value in sorted_word_freq_list:
        total_words += value

    # get the top 20 words
    if len(sorted_word_freq_list) > 20:
        sorted_word_freq_list = sorted_word_freq_list[:20]

    # create final list, words, + frequency + percentage
    final_list = []
    for key, value in sorted_word_freq_list:
        percentage = float(value * 100) / total_words
        final_list.append([key, value, round(percentage, 4)])

    print_headers = ["Word", "Frequency", "Percentage"]

    # print the table
    print(tabulate(tabular_data=final_list, headers=print_headers, tablefmt="orgtbl"))

except requests.exceptions.Timeout:
    print("The server did not respond please try again later")
