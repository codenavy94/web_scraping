import requests
from bs4 import BeautifulSoup

### Best Seller 책 40권에 대한 url 추출

url = 'http://www.yes24.com/24/Category/BestSeller'
bsinfo = requests.get(url).text
soup = BeautifulSoup(bsinfo, 'lxml')

book_url_lst = []
for i in range(1, 41):
    search_index = 'num' + str(i) # num1, num2, ...
    
    try:
        book_url = soup.find('li', attrs={'class':search_index}).find('a').get('href')
    except:
        search_index = 'num' + str(i) + '_line' # num19_line, num20_line, ...
        book_url = soup.find('li', attrs={'class':search_index}).find('a').get('href')

    book_url = 'http://www.yes24.com' + book_url
    book_url_lst.append(book_url)


### 각 책에 대해 제목, 평점, 저자(들), 발간일, 판매가, 할인율 정보를 출력

with open('YES24_bestseller_info.txt', 'w', encoding='utf-8') as f:
    f.write('\t'.join(['title', 'rating', 'authors', 'pubdate', 'price', 'discount']) + '\n')

    for book_url in book_url_lst:
        book_info = requests.get(book_url).text
        soup = BeautifulSoup(book_info, 'lxml')
        
        title = soup.find('meta', attrs={'name':'title'}).get('content').split('-')[0].strip()
        try:
            rating = soup.find('span', attrs={'id':'spanGdRating'}).find('em', attrs={'class':'yes_b'}).text
        except:
            rating = "NA" # rating 정보가 없는 도서의 경우, rating 정보를 'NA'로 저장
        authors = soup.find('meta', attrs={'name':'author'}).get('content')
        pubdate = soup.find('span', attrs={'class':'gd_date'}).text
        price = soup.find('span', attrs={'class':'nor_price'}).text.replace("원", "")
        discount = soup.find('tr', attrs={'class':'accentRow'}).text.strip().split('%')[0].split('(')[-1]

        f.write('\t'.join([title, rating, authors, pubdate, price, discount]) + '\n')

print('---BOOK INFO SAVE COMPLETE---')