from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm
from datetime import datetime

session = HTMLSession()
today = datetime.now()

keyword = input("Enter ny one keyword: ")
# keyword = 'laptop'
urls = ["https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=0&_pgn={}".format(
    keyword, x) for x in range(0, 9)]

data = []

for url in tqdm(urls):
    r = session.get(url.strip())
    content = r.html.find('div.s-item__wrapper.clearfix')

    for items in content:
        img = items.find('div.s-item__image a img', first=True).attrs['src']
        title = items.find('div.s-item__title', first=True).text
        subtitle = items.find('div.s-item__subtitle span', first=True).text
        price = items.find('span.s-item__price', first=True).text
        try:
            sallercategory = items.find(
                'span.s-item__etrs-text', first=True).text
        except:
            sallercategory = ''
        try:
            discountprice = items.find(
                'span.s-item__discount.s-item__discount', first=True).text
        except:
            discountprice = ''
        try:
            shippingprice = items.find(
                'span.s-item__shipping.s-item__logisticsCost', first=True).text.replace('shipping', '')
        except:
            shippingprice = ''
        try:
            shippingfrom = items.find(
                'span.s-item__location.s-item__itemLocation', first=True).text.replace('from', '')
        except:
            shippingfrom = ''

        link = items.find('a.s-item__link', first=True).attrs['href']

        data.append([title, subtitle, price, discountprice,
                    shippingprice, shippingfrom, sallercategory, img, link])

df = pd.DataFrame(data, columns=['Title', 'Subtitle', 'Price', 'Discount Price',
                  'Shipping Price', 'Shipping From', 'Saller Category', 'Image Url', 'Item Url'])

df.to_csv(f'{today.strftime("%Y%m%d%H%M%S")}.csv', index=False, mode='a')
