import streamlit as st
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import os
import base64

st.title('Webスクレイピング')
button = st.button('Start')
latest_interation = st.empty()
bar = st.progress(0)
last_number = st.number_input('取得カテゴリー数を入力してください。', 1, 100, 1)
def main(c_number):
  url = 'https://imitsu.jp/'
  while True:
    try:
      sleep(2)
      r = requests.get(url, timeout=3)
      r.raise_for_status()
    except Exception as e:
      print('-----ERROR(リトライ中)-----')
    else:
      break
  soup = BeautifulSoup(r.content, 'lxml')
  jobs = soup.select('div.category-main a.ga_event')
  print(len(jobs))

  count = 0
  d_list = []
  for p, job in enumerate(jobs[:1]):
    job = jobs[c_number]
    print('*'*100)
    print(job.text)
    csv_name = f'{job.text}'
    page_url = job.get('href') + 'search/'
    print(page_url)
    retry = 0
    while retry < 10:
      try:
        sleep(2)
        page_r = requests.get(page_url, timeout=3)
        page_r.raise_for_status()
      except Exception as e:
        retry += 1
        print('-----ERROR(リトライ中)-----')
      else:
        break
    page_soup = BeautifulSoup(page_r.content, 'lxml')
    error_title = page_soup.select_one('h1.error_title')
    if error_title:
      print('404エラー')
      pass
    else:
      kensu = page_soup.select_one('div.service-count-hit').text.replace('件', '').replace(',', '')
      print('件数:', kensu)
      n = int(kensu) // 20 + 1
      if int(kensu) % 20 == 0:
        n = int(kensu) // 20

      n = 1
      for i in range(n):
        page_url = job.get('href') + 'search/' + f'?pn={i+1}#title'
        while True:
          try:
            sleep(1)
            page_r = requests.get(page_url, timeout=3)
            page_r.raise_for_status()
          except Exception as e:
            print('-----ERROR(リトライ中)-----')
          else:
            break
        page_soup = BeautifulSoup(page_r.content, 'lxml')
        companys = page_soup.select('h3.service-link')
        print('companys:', len(companys))

        for company in companys:
          count += 1
          print('='*10, f'{count}/{kensu}({i+1}/{n}ページ)', '='*10)
          latest_interation.text(f'{count}/{kensu}({i+1}/{n}ページ)')
          company_name = '?'.join(company.text.split()).replace('?', '')
          print(company_name)
          detail_url = company.select_one('a').get('href')
          print(detail_url)
          retry = 0
          while retry < 10:
            try:
              sleep(1)
              detail_r = requests.get(detail_url, timeout=3)
              detail_r.raise_for_status()
            except Exception as e:
              retry += 1
              print('-----ERROR(リトライ中)-----')
            else:
              break
          detail_soup = BeautifulSoup(detail_r.content, 'lxml')
          div = detail_soup.select_one('section#company > div.service-information-content')
          dts = div.select('dl > dt')
          dds = div.select('dl > dd')
          detail = [None] * 5
          for k, dt in enumerate(dts):
            if '会社名' == dt.text: detail[0] = '?'.join(dds[k].text.split()).replace('?', '')
            elif '設立年' == dt.text: detail[1] = '?'.join(dds[k].text.split()).replace('?', '')
            elif '従業員数' == dt.text: detail[2] = '?'.join(dds[k].text.split()).replace('?', '')
            elif '住所' == dt.text: detail[3] = '?'.join(dds[k].text.split()).replace('?', '')
            elif '会社URL' == dt.text: detail[4] = '?'.join(dds[k].text.split()).replace('?', '')

          print('会社名:', detail[0])
          print('設立年:', detail[1])
          print('従業員数:', detail[2])
          print('住所:', detail[3])
          print('会社URL:', detail[4])

          d_list.append({
            '会社名': detail[0],
            '設立年': detail[1],
            '従業員数': detail[2],
            '住所': detail[3],
            '会社URL': detail[4],
            'ソースURL': page_url,
          })

          df = pd.DataFrame(d_list)
    
  return df
#       # df.to_csv(csv_name, index=False, encoding='utf-8-sig')

if button:
  cates = ['ホームページ制作', 'アプリ開発', 'システム開発', 'ITインフラ構築', 'データセンター', '情報システム代行']
  csvs = []
  for i, cate in enumerate(cates):
    if cate == 'ホームページ制作': c_number = 0
    elif cate == 'アプリ開発': c_number = 1
    elif cate == 'システム開発': c_number = 2
    elif cate == 'ITインフラ構築': c_number = 4
    elif cate == 'データセンター': c_number = 5
    elif cate == '情報システム代行': c_number = 6
    df = main(c_number)
    st.write(f'## 結果 {i+1}/{len(cates)}', df)
    # with pd.ExcelWriter("export_data.xlsx") as EW:
    #   csv = df.to_excel(EW, index=False, sheet_name=f"{cate}")
    csv = df.to_csv(cate + '.csv', index=False, encoding='utf-8-sig')
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="result.csv">download</a>'
    st.markdown(f"ダウンロードする {href}", unsafe_allow_html=True)
    # csvs.append(csv)
  'Done'
  # for csv in csvs:
  #   b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
  #   href = f'<a href="data:application/octet-stream;base64,{b64}" download="result.csv">download</a>'
  #   st.markdown(f"ダウンロードする {href}", unsafe_allow_html=True)

