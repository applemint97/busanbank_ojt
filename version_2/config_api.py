import configparser

def config_generator():
    # 설정파일 생성
    config = configparser.ConfigParser()
    
    key = '4bJGyc3PnSj%%2B30WUZQFtrkavccxBNxczoVIos5vMZz9%%2Fh2Hxfw7JtflieuWlgta4CMOBuUfhbWdDjw6eX%%2BoWHg%%3D%%3D'
    # 설정파일 오브젝트 만들기
    config['system'] = {}
    config['system']['api_key'] = key

    # 설정파일 저장
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def config_read_key():
    # 설정파일 읽기
    config = configparser.ConfigParser()    
    config.read('config.ini', encoding='utf-8') 

    # 설장파일 색션 확인
    # config.sections()
    return(key_read(config))

def key_read(config):
    
    # 섹션값 읽기
    key = config['system']['api_key']
    return(key)