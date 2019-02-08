import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"}


def elibrary_parce(headers):
    base_url = input('Введите url ')
    session = requests.session()
    request = session.get(base_url, headers=headers)
    english_text = 'отсутствует'
    source_journal = 'отсутствует'
    issn = 'отсутствует'
    title = 'отсутствует'
    key_words_list = []
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs_title = soup.find_all('span', attrs={'class': 'bigtext'})
        for div in divs_title:
            div = str(div)
            title = str(div.split('>')[2].split('<')[0])

        divs_authors = soup.find_all('span', attrs={'style': 'white-space: nowrap'})
        authors_list = []
        for authors in divs_authors:
            author = authors.find('b')
            if author is None:
                continue
            authors_list.append(author.text)
        eng_text = soup.find_all('p', attrs={'align': 'justify'})
        for text in eng_text:
            lel = text.find('p')
            if lel is None:
                continue
            english_text = lel.text
        main_texts = soup.find_all('table', attrs={'width': '550', 'border': '0', 'cellspacing': '0'})
        main_text = []
        for source in main_texts:
            text = source.find('p', attrs={'align': 'justify'})
            if text is None:
                continue
            main_text.append(text.text)
        journals = soup.find_all('td', attrs={'width': '504', 'align': 'left'})
        journal = []
        for key in journals:
            text = key.find('a')
            if text is None:
                continue
            journal.append(text.text)
        sources_journal = soup.find_all('td', attrs={'width': '504'})
        key_list = []
        for key in sources_journal:
            key = key.text
            text = str(key)
            key_list.append(text.splitlines())

        for keys in key_list:
            for key in keys:
                first_key = key.split()
                if len(first_key) > 0:

                    if first_key[0] == 'Издательство:':
                        source_journal = first_key
                    if first_key[0] == 'ISSN:':
                        issn = first_key
        key_words = soup.find_all('a')
        for key in key_words:
            keys = str(key).split()
            del keys[0]
            key_temp = keys
            keys = keys[0].split('=')
            del keys[0]
            keys = keys[0].split('.')
            if keys[0] == '"keyword_items':
                temp = ' '.join(key_temp).split('>')
                del temp[0], temp[1]
                temp = temp[0].split('<')

                key_words_list.append(temp[0])

    print('Название статьи - "' + title + '"')
    print('Авторы : ', end='')
    for i in authors_list:
        if len(authors_list) == 1:
            print(i)
            break
        print(i, end=', ')
    else:
        print('')
    if len(journal) > 0:
        print('Журнал :', journal[0])
    if source_journal == 'отсутствует':
        print('Издательства нет')
    else:
        print(' '.join(source_journal))
    if issn == 'отсутствует':
        print('ISSN нет')
    else:
        print(' '.join(issn))
    print('Ключевые слова: ' + ', '.join(key_words_list))
    if len(main_text) > 0:
        print('Аннотация :', main_text[0], end='')
    print('Описание на английском :', english_text)


if __name__ == "__main__":
    while True:
        elibrary_parce(headers)
