import requests
import sys

from bs4 import BeautifulSoup

args = sys.argv
lg_from = args[1]
lg_to = args[2]
word = args[3]
languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']


def create_urls():
    list_of_urls = []
    if lg_to == 'all':
        for i in languages:
            if i != lg_from:
                list_of_urls.append('https://context.reverso.net/translation/{}-{}/{}'.format(lg_from, i, word))
    else:
        list_of_urls.append('https://context.reverso.net/translation/{}-{}/{}'.format(lg_from, lg_to, word))
    return list_of_urls


def check_urls():
    urls = create_urls()
    for i in urls:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(i, headers=headers)
        if result:
            continue
        else:
            return result.status_code
    return True


def get_lists_of_words_and_sentences():
    the_urls = create_urls()
    multi_lists_words = []
    multi_lists_sentences = []
    for i in the_urls:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(i, headers=headers)
        soup = BeautifulSoup(result.content, 'html.parser')

        words = soup.find_all("a", {"class": "translation"}, {"lang": "fr"})
        list_of_words = []
        for j in words:
            list_of_words.append(j.text.strip())
        multi_lists_words.append(list_of_words)

        sentences = soup.find_all("div", {"class": "example"}, {"lang": "fr"})
        list_of_sentences = []
        for sentence in sentences:
            the_line = sentence.text.strip().split('\n')
            for j in the_line:
                if j != ' ' and j != '' and j != '\n':
                    list_of_sentences.append(j.strip())
        multi_lists_sentences.append(list_of_sentences)

    return multi_lists_words, multi_lists_sentences


def write_to_file():
    the_list_of_all_urls = create_urls()
    words, sentences = get_lists_of_words_and_sentences()
    languages.remove(lg_from)
    name_file = open('{}.txt'.format(word), 'w', encoding='utf-8')
    n = len(the_list_of_all_urls)
    for i in range(n):
        if n == 1:
            name_file.write("{} Translations:".format(lg_to.capitalize()) + '\n')
            for j in range(1, 6):
                name_file.write(words[i][j] + '\n')
            name_file.write("{} Examples:".format(lg_to.capitalize()) + '\n')
            for j in range(12):
                name_file.write(sentences[i][j] + '\n')
                if j % 2 != 0:
                    name_file.write('\n')
        else:
            name_file.write("{} Translations:".format(languages[i].capitalize()) + '\n')
            for k in range(1, 2):
                name_file.write(words[i][k] + '\n')

            name_file.write("{} Examples:".format(languages[i].capitalize()) + '\n')
            for k in range(2):
                name_file.write(sentences[i][k] + '\n')
                if k % 2 != 0:
                    name_file.write('\n')
    name_file.close()


if (lg_to not in languages) and (lg_to != 'all'):
    print("Sorry, the program doesn't support {}".format(lg_to))
elif lg_from not in languages:
    print("Sorry, the program doesn't support {}".format(lg_from))
else:
    response = check_urls()
    if response is True:
        write_to_file()
        f = open('{}.txt'.format(word), "r")
        for x in f:
            print(x)
        f.close()
    elif response == 404:
        print("Sorry, unable to find {}".format(word))
    else:
        print('Something wrong with your internet connection')
