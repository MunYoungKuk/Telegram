import os
import requests
import json

token = os.getenv('tele_token')
method = 'getUpdates'

# c9에서 telegram api 막음 ㅠㅠㅠ
# url = "https://api.telegram.org/bot{}/{}".format(token,method)
url = "https://api.hphk.io/telegram/bot{}/{}".format(token,method)

res = requests.get(url).json()
#딕셔너리에서 추출할때 괄호 확인 잘하기 []:리스트 {}:딕셔너리 리스트에 딕셔너리가 있을수도 있고 반대일수도 있으므로 주의해서
user_id = res["result"][0]["message"]["from"]["id"]#id값 찾아서 넣기

msg = "야"

method='sendMessage'
msg_url = "https://api.hphk.io/telegram/bot{}/{}?chat_id={}&text={}".format(token,method,user_id,msg)
#인자와 인자 구분할때 : & ,

print(msg_url)
requests.get(msg_url)
