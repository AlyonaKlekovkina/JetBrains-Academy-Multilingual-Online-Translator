import requests

from bs4 import BeautifulSoup

inp = input('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French: \n')
word = input('Type the word you want to translate: \n')

print('You chose "{}" as the language to translate "{}" to.'.format(inp, word))

address = ''
if inp == 'fr':
    address = 'https://context.reverso.net/translation/english-french/{}'.format(word)
elif inp =='en':
    address = 'https://context.reverso.net/translation/french-english/{}'.format(word)

url = address
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
result = requests.get(url, headers=headers)

if result:
    print('200 OK')
    print('\nContext examples:\n')

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


print("French Translations:")
for i in range(1, 6):
    print(list_of_words[i])

print("\nFrench Examples:")
for i in range(6):
    for j in f[i]:
        print(j)
    print()
