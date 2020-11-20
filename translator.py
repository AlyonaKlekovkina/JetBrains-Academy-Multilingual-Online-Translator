import requests

from bs4 import BeautifulSoup

languages = {1: 'arabic', 2: 'german', 3: 'english', 4: 'spanish', 5: 'french', 6: 'hebrew', 7: 'japanese', 8: 'dutch', 9: 'polish', 10: 'portuguese', 11: 'romanian', 12: 'russian', 13: 'turkish'}

lg_from = int(input("Hello, you're welcome to the translator. Translator supports:\n1. Arabic\n2. German\n3. English\n4. Spanish\n5. French\n6. Hebrew\n7. Japanese\n8. Dutch\n9. Polish\n10. Portuguese\n11. Romanian\n12. Russian\n13. Turkish\nType the number of your language:\n"))
lg_to = int(input("Type the number of your language:\n"))

word = input('Type the word you want to translate: \n')


def create_address(fr, t):
    left = languages.get(fr)
    right = languages.get(t)
    address = 'https://context.reverso.net/translation/{}-{}/{}'.format(left, right, word)
    return address


url = create_address(lg_from, lg_to)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
result = requests.get(url, headers=headers)


soup = BeautifulSoup(result.content, 'html.parser')
words = soup.find_all("a", {"class": "translation"}, {"lang": "fr"})
list_of_words = []
for i in words:
    list_of_words.append(i.text.strip())


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


print("{} Translations:".format(languages.get(lg_to).capitalize()))
for i in range(1, 6):
    print(list_of_words[i])

print("\n{} Examples:".format(languages.get(lg_to).capitalize()))
for i in range(6):
    for j in f[i]:
        print(j)
    print()
