import os
from flask import Flask, request
#데이터를 가독성 좋게 만들어 주는 모듈
#pprint 모듈을 가져오면서 pp로 새 이름 지정
from pprint import pprint as pp 
import requests
import random

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

api_url = 'https://api.hphk.io/telegram'
token = os.getenv('TELE_TOKEN')

@app.route(f'/{token}', methods=['POST'])
def telegram():
    #Naver api를 쓰기 위한 변수 , ~./bashrc에 환경변수로 지정해 놓음
    naver_client_id = os.getenv('NAVER_ID')
    naver_client_secret = os.getenv('NAVER_SECRET')
    
    #tele_dict 데이터 덩어리
    tele_dict = request.get_json()
    pp(request.get_json())#json 구조 출력
    
    #유저 정보 가져오기
    chat_id = tele_dict['message']['from']['id']
    # print(chat_id)
    #유저가 입력한 데이터
    #text = tele_dict()['message']['text']
    text = tele_dict.get('message').get("text")
    # print(text)
    
    
    tran = False
    img = False
    #사용자가 이미지를 넣었는지 체크
    
    #text(유저가 입력한 데이터) 제일 앞 두글자가 번역
    # if tele_dict["message"]['photo'] is not None: #tele_dict["message"]["photo"]에 파일이 있으면 실행
    if tele_dict.get('message').get('photo') is not None:
        img = True
    else:
        if  text[:2] == '번역' :
        # 번역 안녕하세요
                tran = True
                text = text.replace("번역 ","") 
        # 번역 안녕하세요 -> 안녕하세요
        
    if tran:
        papago = requests.post("https://openapi.naver.com/v1/papago/n2mt",
        headers = {
            'X-Naver-Client-Id' : naver_client_id,
            'X-Naver-Client-Secret' : naver_client_secret
                },
        data =   {
            'source':'ko',
            'target':'en',
            'text' : text
            
                }
        )
        # pp(papago)
        # pp(papago.json())
        text = papago.json()['message']['result']['translatedText']
        
    elif img:
        text = "사용자가 이미지를 넣었어요"
        #텔레그램에게 사진 정보 가져오기
        file_id = tele_dict['message']['photo'][-1]['file_id']
        file_path = requests.get(f"{api_url}/bot{token}/getFile?file_id={file_id}").json()['result']['file_path']
        file_url = f"{api_url}/file/bot{token}/{file_path}"
        #사진을 네이버 유명인 인식 api로 넘겨주기
        print(file_url)
        #가져온 데이터 중에서 필요한 정보 빼오기
        file = requests.get(file_url,stream=True)
        clova = requests.post("https://openapi.naver.com/v1/vision/celebrity",
                    headers = {
                        "X-Naver-Client-Id":naver_client_id,
                        "X-Naver-Client-Secret":naver_client_secret
                    },
                    files = {
                        "image":file.raw.read()
                    }
        )
        print(clova.json())
        #인식이 되었을때
        if clova.json().get('info').get('faceCount'):
            text = clova.json()['faces'][0]['celebrity']['value']
        #인식이 되지 않았을때
        else:
            text = "인식에 실패하였습니다."
    
    elif text == '메뉴':
        menu_list = ["한식","중식","양식","분식","일식"]
        text = random.choice(menu_list)
       
        
    elif text == '로또':
         num_list = range(1,46)
         pick = random.sample(num_list,6)
         text = sorted(pick)
         
    #유저에게 그대로 돌려주기
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    return '', 200
    
    
  
app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',8080)))

