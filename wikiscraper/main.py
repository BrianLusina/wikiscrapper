import requests
import operator
import json
from tabulate import tabulate
import sys
from wikiscraper import constants
from wikiscraper import get_word_list, remove_stop_words, create_frequency_table

# if the search word is too small, throw error
if len(sys.argv) < 2:
    print("Enter valid string")
    exit()

# get the search word
string_query = sys.argv[1]

# to remove stop words or not
if len(sys.argv) > 2:
    search_mode = True
else:
    search_mode = False

# create our URL
url = constants.WIKI_API_LINK + string_query


def main(url):
    # great for HTTP requests
    try:
        # use requests to retrieve raw data from wiki API URL we
        # just constructed
        response = requests.get(url)

        # format that data as a JSON dictionary
        data = json.loads(response.content.decode("utf-8"))

        # page title, first option
        # show this in web browser
        wikipedia_page_tag = data['query']['search'][0]['title']

        # get actual wiki page based on retrieved title
        url = constants.WIKI_LINK + wikipedia_page_tag
        # get list of words from that page
        page_word_list = get_word_list(url)
        # create table of word counts, dictionary
        page_word_count = create_frequency_table(page_word_list)
        # sort the table by the frequency count
        sorted_word_frequency_list = sorted(page_word_count.items(), key=operator.itemgetter(1), reverse=True)
        # remove stop words if the user specified
        if search_mode:
            sorted_word_frequency_list = remove_stop_words(sorted_word_frequency_list)

        # sum the total words to calculate frequencies
        total_words_sum = 0
        for key, value in sorted_word_frequency_list:
            total_words_sum = total_words_sum + value

        # just get the top 20 words
        if len(sorted_word_frequency_list) > 20:
            sorted_word_frequency_list = sorted_word_frequency_list[:20]

        # create our final list which contains words, frequency (word count), percentage
        final_list = []
        for key, value in sorted_word_frequency_list:
            percentage_value = float(value * 100) / total_words_sum
            final_list.append([key, value, round(percentage_value, 4)])

        # headers before the table
        print_headers = ['Word', 'Frequency', 'Frequency Percentage']

        # print the table with tabulate
        print(tabulate(final_list, headers=print_headers, tablefmt='orgtbl'))

    # throw an exception in case it breaks
    except requests.exceptions.Timeout:
        print("The server didn't respond. Please, try again later.")


if __name__ == "__main__":
    main(url)
