import requests

from bs4 import BeautifulSoup

languages = {1: 'arabic', 2: 'german', 3: 'english', 4: 'spanish', 5: 'french', 6: 'hebrew', 7: 'japanese', 8: 'dutch', 9: 'polish', 10: 'portuguese', 11: 'romanian', 12: 'russian', 13: 'turkish'}

lg_from = int(input("Hello, you're welcome to the translator. Translator supports:\n1. Arabic\n2. German\n3. English\n4. Spanish\n5. French\n6. Hebrew\n7. Japanese\n8. Dutch\n9. Polish\n10. Portuguese\n11. Romanian\n12. Russian\n13. Turkish\nType the number of your language:\n"))
lg_to = int(input("Type the number of a language you want to translate to or '0' to translate to all languages:\n"))
word = input('Type the word you want to translate: \n')


def create_address(fr, t):
    left = languages.get(fr)
    right = languages.get(t)
    address = 'https://context.reverso.net/translation/{}-{}/{}'.format(left, right, word)
    return address


def get_urls():
    list_of_urls = []
    if lg_to == 0:
        for i in range(1, 14):
            if lg_from != i:
                url = create_address(lg_from, i)
                list_of_urls.append(url)
    else:
        url = create_address(lg_from, lg_to)
        list_of_urls.append(url)
    return list_of_urls


def get_lists_of_words_and_sentences():
    the_urls = get_urls()
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
        for i in sentences:
            list_of_sentences.append(i.text.strip())
        clean_sentences = []
        for i in range(len(list_of_sentences)):
            pair = []
            the_line = list_of_sentences[i].split('\n')
            for j in range(len(the_line)):
                pair.append(the_line[j].strip())
            clean_sentences.append(pair)
        f = []
        for i in range(len(list_of_sentences)):
            p = []
            for j in clean_sentences[i]:
                if j != ' ' and j != '' and j != '\n':
                    p.append(j.strip())
            f.append(p)
        multi_lists_sentences.append(f)
    return multi_lists_words, multi_lists_sentences


the_list_of_all_urls = get_urls()
the_lists_of_all_words_and_sentences = get_lists_of_words_and_sentences()
name_file = open('{}.txt'.format(word), 'w', encoding='utf-8')

n = len(the_list_of_all_urls)
for i in range(n):
    if n == 1:
        print("{} Translations:".format(languages.get(lg_to).capitalize()))
        name_file.write("{} Translations:".format(languages.get(lg_to).capitalize()) + '\n')
    else:
        if i+1 < lg_from:
            print("{} Translations:".format(languages.get(i+1).capitalize()))
            name_file.write("{} Translations:".format(languages.get(i+1).capitalize()) + '\n')
        elif i+1 >= lg_from:
            print("{} Translations:".format(languages.get(i+2).capitalize()))
            name_file.write("{} Translations:".format(languages.get(i+2).capitalize()) + '\n')
    for j in range(1, 2):
        print(the_lists_of_all_words_and_sentences[0][i][j])
        name_file.write(the_lists_of_all_words_and_sentences[0][i][j] + '\n')
    name_file.write('\n')
    print()

    if n == 1:
        print("{} Example:".format(languages.get(lg_to).capitalize()))
        name_file.write("{} Example:".format(languages.get(lg_to).capitalize()) + '\n')
    else:
        if i+1 < lg_from:
            print("{} Example:".format(languages.get(i+1).capitalize()))
            name_file.write("{} Example:".format(languages.get(i+1).capitalize()) + '\n')
        elif i+1 >= lg_from:
            print("{} Example:".format(languages.get(i+2).capitalize()))
            name_file.write("{} Example:".format(languages.get(i+2).capitalize()) + '\n')
    for j in range(1, 2):
        for k in the_lists_of_all_words_and_sentences[1][i][j]:
            print(k)
            name_file.write(k + '\n')
        name_file.write('\n')
        print()
    name_file.write('\n')
    print()
name_file.close()
