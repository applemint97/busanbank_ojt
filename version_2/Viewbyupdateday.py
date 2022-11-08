import json
import requests
import pprint
import set_logging
import config_api
import pandas as pd
import numpy as np

start_date = pd.to_datetime('2021-12-10') # 시작 날짜
end_date = pd.to_datetime('2021-12-11') # 마지막 날짜

dates = pd.date_range(start_date,end_date,freq='D')
dates = dates.strftime('%Y%m%d')

# 최종 dataframe을 위한 할당
df = pd.DataFrame()

# encoding key 입력
config_api.config_generator()
key = config_api.config_read_key()

try:
    for i in dates:
        #url = f'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListByDate?serviceKey={key}&pageNo=1&numOfRows=10&key={i}&type=json'
        url = f'http://apis.data.go.kr/B553'
        # url 불러오기
        response = requests.get(url)

        # 정상 출력, 에러 구분
        if response.status_code == 200:
            set_logging.log.debug(f'정상 출력상태 : {response.status_code}')
        else:
            set_logging.log.warning(f'에러 발생 : {response.status_code} Error')

        # 데이터 값 출력해보기
        contents = response.text

        # 데이터 결과값 온전하게 출력해주는 코드
        pp = pprint.PrettyPrinter(indent=4)

        #문자열을 변경
        json_ob = json.loads(contents)

        # 필요한 내용만 추출
        body = json_ob['body']['items']

        # pandas import
        from pandas.io.json import json_normalize
        # Dataframe으로 만들기
        dataframe = json_normalize(body)

        df_for = pd.DataFrame(dataframe)

        chgDt = []

        for k in range(len(df_for)):
            chgDt.append(i)

        df_for['chgDt'] = chgDt
        df = pd.concat([df, df_for], axis=0)
        set_logging.log.debug(f'{i}일자 데이터 추출 성공')

except JSONDecodeError:
    set_logging.log.warning('JSONDecodeError 발생')
except SSLError:
    set_logging.log.warning('SSLError 발생')
except:
    set_logging.log.warning('에러 발생')

df.to_csv('2021Y12Mtest.csv', encoding = 'utf-8-sig', index=False)    
print(df)