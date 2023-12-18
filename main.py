import requests,json, os, urllib
from flask import Flask
from flask import render_template
from flask import request
import hashlib
import time 
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()

api = os.getenv('KEY')

DEFAULTS={'hashValue':'5767653494d05b3f3f38f1662a63335d09ae6489'}

api_url = 'https://www.virustotal.com/vtapi/v2/file/report'

UPLOAD_FOLDER = './uploads'

headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,  My Python requests library example client or username"}

proxy_list = {
    'http': 'http://username:password@proxyserver:proxyport',
    'https': 'https://username:password@proxyserver:proxyport'
}


@app.route('/', methods=['GET', 'POST'])
def home():
    f = ""
    img_key=""
    if request.method == 'POST':
        f = request.files['inputFile']
        img_key = hashlib.md5(f.read()).hexdigest()
    
    textAreaHash = request.args.get('textArea')
    allhash=[img_key,textAreaHash]
    if allhash==['',None]:
        allhash=[DEFAULTS['hashValue']]
        
    resultVT=[]
    for i in allhash:
        time.sleep(5)
        response = findHashatVT(i)
        resultVT.append(response)
    resultVTjson=json.dumps(resultVT)
    print(resultVT)

        
    return render_template('home.html', size=len(allhash), resultVT=resultVT,resultVTjson=resultVTjson)


def findHashatVT(hashValue):
    print(hashValue)
    params = {'apikey': f'{api}', 'resource': hashValue}
    try:
        response = requests.post(api_url, params=params, headers=headers, verify=False)
    except ConnectionError as e:
        return e


    try:
        positives = response.json()['positives']
        total = response.json()['total']
        permalink=response.json()['permalink']
    except:
        positives = 'n'
        total = 'a'
        permalink=''

    try:
        Symantec_response = response.json()['scans']['Symantec']['detected']
        Symantec_result = response.json()['scans']['Symantec']['result']
        Symantec_update = response.json()['scans']['Symantec']['update']
    except:

        Symantec_response = '-'
        Symantec_result = '-'
        Symantec_update ='-'

    try:
        Trendmicro_response = response.json()['scans']['TrendMicro']['detected']
    except:
        Trendmicro_response = '-'

    try:
        Sophos_response = response.json()['scans']['Sophos']['detected']
    except:
        Sophos_response = '-'

    try:
        McAfee_response = response.json()['scans']['McAfee']['detected']
    except:
        McAfee_response='-'


    return hashValue,positives,total,Symantec_response, Symantec_result,Symantec_update, Trendmicro_response, Sophos_response,McAfee_response,permalink

if __name__ == '__main__':
    app.run(port=5001,debug=True)
