import sys
import json
import requests
import pprint
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import logging
import logging.handlers
import configparser

# log설정

# logging 모듈에서 로거 가져오기
log = logging.getLogger(__name__)
logging.basicConfig(filename="logmessage.txt", filemode="w")
log.setLevel(logging.INFO)

# 출력 형식(포매터) 지정
formatter = logging.Formatter('[Leehwajung][%(levelname)s] - %(asctime)s - (%(filename)s) %(message)s')

# 파일과 콘솔 출력을 지정
fileHandler = logging.FileHandler('logmessage.txt')
streamHandler = logging.StreamHandler()

# 파일과 콘솔에 포매터 지정
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

# log에 파일과 콘솔 지정
log.addHandler(fileHandler)
log.addHandler(streamHandler)

# 최종 dataframe을 위한 할당
df = pd.DataFrame()

# config.ini파일에서 api key 값 가져오기
def config_read_key():
    # 설정파일 읽기
    config = configparser.ConfigParser()    
    config.read('config.ini', encoding='utf-8') 

    # 설장파일 색션 확인
    return(key_read(config))

def key_read(config):
    
    # 섹션값 읽기
    key = config['system']['api_key']
    return(key)

# encoding key 입력
key = config_read_key()

if len(sys.argv) != 2:
    date = '20210602'
    ex = '_example'
    log.info('날짜를 입력하지 않거나 잘못입력하여 샘플데이터를 출력하겠습니다.')
elif len(sys.argv[1]) == 8:
    date = sys.argv[1]
    ex = ''
else:
    date = '20210602'
    ex = 'example'
    log.info('날짜입력 형식이 잘못되어 샘플데이터를 출력하겠습니다.')

try:
    url = f'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListByDate?serviceKey={key}&pageNo=1&numOfRows=10&key={date}&type=json'
    log.info(f'데이터 요청한 URL 주소 : {url}')

    # url 불러오기
    response = requests.get(url)

    # 정상 출력, 에러 구분
    if response.status_code == 200:
        log.info(f'정상 출력상태 : {response.status_code} | {response.reason}')
    else:
        log.error(f'에러 발생 : {response.status_code} | {response.reason}')

    # 데이터 값 contents에 담기
    contents = response.text

    #문자열을 변경
    json_ob = json.loads(contents)

    # 필요한 내용만 추출
    body = json_ob['body']['items']
    
    # Dataframe으로 만들기
    dataframe = json_normalize(body)
    df_for = pd.DataFrame(dataframe)
    
    # 추출한 데이터 프레임에 아무 데이터가 없을 경우 데이터 없다고 출력
    if df_for.empty == True:
        log.info(f'{date}일자 데이터가 존재하지 않습니다.')
    
    # 수정일자 변수 추가
    chgDt = []
    for k in range(len(df_for)):
        chgDt.append(date)
    
    # 수정일자 변수 데이터프레임에 추가
    df_for['chgDt'] = chgDt
    df = pd.concat([df, df_for], axis=0)
    
    log.info(f'{date}일자 데이터 추출 성공')
    
    # 추출한 데이터프레임 csv파일로 저장
    df.to_csv(f'show_updateday_{date}{ex}.csv', encoding = 'utf-8-sig', index=False)

# 모든 예외처리 및 예외 메세지 출력        
except Exception as e:
    log.info(f'{e}')


print(df)