import json
import requests
import pprint
import set_logging
import pandas as pd
import numpy as np


start_date = pd.to_datetime('2021-06-21') ## 시작 날짜
end_date = pd.to_datetime('2021-06-23') ## 마지막 날짜
 
# print(start_date)
# print(end_date)

dates = pd.date_range(start_date,end_date,freq='D')
dates = dates.strftime('%Y%m%d')

# 최종 dataframe을 위한 할당
df = pd.DataFrame()

for i in dates:

    # encoding key 입력
    key = '4bJGyc3PnSj%2B30WUZQFtrkavccxBNxczoVIos5vMZz9%2Fh2Hxfw7JtflieuWlgta4CMOBuUfhbWdDjw6eX%2BoWHg%3D%3D' # 각자 encoding key 입력
    url = f'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListByDate?serviceKey={key}&pageNo=1&numOfRows=1000&key={i}&type=json'
    
    #  url 불러오기
    response = requests.get(url)

    # 데이터 값 출력해보기
    contents = response.text

    # print(contents)

    # 데이터 결과값 온전하게 출력해주는 코드
    pp = pprint.PrettyPrinter(indent=4)
    #print(pp.pprint(contents))

    #문자열을 변경
    json_ob = json.loads(contents)
    #print(json_ob)
    #print(type(json_ob)) #json확인

    # 필요한 내용만 추출
    #body = json_ob['header']['items']['item']
    body = json_ob['body']['items']

    #print(body)

    # pandas import
    import pandas as pd
    from pandas.io.json import json_normalize
    # Dataframe으로 만들기
    dataframe = json_normalize(body)
    
    df_for = pd.DataFrame(dataframe)
    
    chgDt = []
    
    for j in range(len(df_for)):
        chgDt.append(i)
        
    df_for['chgDt'] = chgDt
    df = pd.concat([df, df_for], axis=0)
    set_logging.log.debug(f'{i}일자 데이터 추출 성공')

print(df)