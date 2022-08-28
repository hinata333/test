from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep

#####################################変更欄（右辺のみ変更して下さい。）#####################################

#読み込みページ数 (例：strat_number = 1,last_number = 50  →  1～50ページを取得します。)
strat_number = 1
last_number = 1

#URL (例：items_url = 'https://www.2ndstreet.jp/search?category=700053') ※「''」で囲ってください。
items_url = 'https://www.2ndstreet.jp/search?category=700053'

#保存するcsvファイルの名前 (例：csv_name = '2nd_street.csv') ※「''」で囲ってください。
csv_name = '2nd_street_test_st.csv'

############################################################################################################

def main():
  d_list=[]
  count = 0
  for i in range(int(strat_number), int(last_number)+1):
    url = items_url + f'&page={i}'
    sleep(3)
    r = requests.get(url, timeout=3)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'lxml')
    jobs = soup.select('li.js-favorite')
    print('ページ内のアイテム数', len(jobs))
    page_number = soup.select_one('p.pager')

    for job in jobs:
      count += 1
      print('='*30, count, f'({page_number.text})', '='*30)
      page_url = 'https://www.2ndstreet.jp' + job.select_one('a').get('href')
      print('商品URL:', page_url)
      try:
        sleep(3)
        page_r = requests.get(page_url, timeout=5)
        page_r.raise_for_status()
        page_soup = BeautifulSoup(page_r.content, 'lxml')
      except Exception as e:
        try:
          print('-----ERROR(リトライ中)-----')
          sleep(5)
          page_r = requests.get(page_url, timeout=5)
          page_r.raise_for_status()
          page_soup = BeautifulSoup(page_r.content, 'lxml')
        except Exception as e:
          print('-----ERROR(リトライ中)-----')
          sleep(5)
          page_r = requests.get(page_url, timeout=5)
          page_r.raise_for_status()
          page_soup = BeautifulSoup(page_r.content, 'lxml')
          pass
        pass

      #商品名
      item_name = page_soup.select_one('div.blandName')
      if item_name:
        item_name = item_name.text
      else:
        item_name = '記載なし'
      productName = page_soup.select_one('div.productName')
      if productName:
        item_name = item_name + ' ' + productName.text
      print('商品名:', item_name)

      #価格
      price = page_soup.select_one('span.priceNum')
      if price:
        price = price.text
      else:
        price = '記載なし'
      print('価格:', price)
      
      #状態
      condition = page_soup.select_one('div.conditionStatus')
      if condition:
        condition = condition.text.split()[1]
        condition = ','.join(condition).replace(',', ' ')
      else:
        condition = '記載なし'
      print('状態:', condition)

      #画像URL
      images = page_soup.select('li.thumbnail-item')
      print('画像数:', len(images))
      image_urls = [None] * 15
      for j, image in enumerate(images):
        image_url = image.select_one('img').get('data-src')
        print(image_url)
        image_urls[j] = image_url
      print(image_urls)
      image_url_1 = image_urls[0]
      image_url_2 = image_urls[1]
      image_url_3 = image_urls[2]
      image_url_4 = image_urls[3]
      image_url_5 = image_urls[4]
      image_url_6 = image_urls[5]
      image_url_7 = image_urls[6]
      image_url_8 = image_urls[7]
      image_url_9 = image_urls[8]
      image_url_10 = image_urls[9]
      image_url_11 = image_urls[10]
      image_url_12 = image_urls[11]
      image_url_13 = image_urls[12]
      image_url_14 = image_urls[13]
      image_url_15 = image_urls[14]


      #コメント
      shopComment = page_soup.select_one('div#shopComment')
      if shopComment:
        shopComment = shopComment.text
      else:
        shopComment = '商品説明記載なし'
      print(shopComment)

      #表
      itemDetail = page_soup.select('section#itemDetail dd')
      detail = [None]*6
      for k, dt in enumerate(itemDetail):
        d = dt.text.split()
        # print(d)
        detail[k] = d
      # print(detail)
      model = ','.join(detail[0]) if detail[0] else ' '
      color = ','.join(detail[1]) if detail[1] else ' '
      pattern = ','.join(detail[2]) if detail[2] else ' '
      material = ','.join(detail[3])  if detail[3] else ' '
      size = ','.join(detail[4]) if detail[4] else ' '
      actual_size = ','.join(detail[5]).replace(',', ' ') if detail[5]  else ' '
      print('型番:', model)
      print('色:', color)
      print('柄:', pattern)
      print('素材・生地:', material)
      print('サイズ:', size)
      print('実寸サイズ:', actual_size)


      d_list.append({
          '商品名': item_name,
          '商品URL': page_url,
          '価格': price,
          '商品状態': condition,
          '型番': model,
          '色': color,
          '柄': pattern,
          '素材・生地': material,
          'サイズ': size,
          '実寸サイズ': actual_size,
          '商品説明': shopComment,
          '画像URL_1': image_url_1,
          '画像URL_2': image_url_2,
          '画像URL_3': image_url_3,
          '画像URL_4': image_url_4,
          '画像URL_5': image_url_5,
          '画像URL_6': image_url_6,
          '画像URL_7': image_url_7,
          '画像URL_8': image_url_8,
          '画像URL_9': image_url_9,
          '画像URL_10': image_url_10,
          '画像URL_11': image_url_11,
          '画像URL_12': image_url_12,
          '画像URL_13': image_url_13,
          '画像URL_14': image_url_14,
          '画像URL_15': image_url_15,
      })
    
      df = pd.DataFrame(d_list)
      # df.to_csv(csv_name, index=False, encoding='utf-8-sig')

if __name__ == '__main__':
  main()