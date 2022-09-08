# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2022/04/09 21:27
# @author  : xiaomi
import time
from git import Repo
from turtle import update
import os
import requests
import flask, json
from urllib.parse import quote, unquote, urlencode

botToken="5528541550:AAHMN2eOC-6W1PkreoQcHfnIwhEzjXmecg4"
updateId = None
listem_id=-1001714808788
def getUpdates(offset):
    if (offset):
        url = "https://api.telegram.org/bot"+botToken+"/getUpdates?offset="+str(offset)
    else:
        url = "https://api.telegram.org/bot"+botToken+"/getUpdates"
    response = requests.request("GET", url, data=None, headers=None)
    resultStr = response.text
    result = json.loads(resultStr)
    if (result["ok"]==True):
        messages = result["result"]
        for message in messages:
            if (message["message"]["chat"]["id"]==listem_id):
                if("document" in message["message"]):
                    downFile(message["message"]["document"]["file_id"],message["message"]["document"]["file_name"],message["message"]["chat"]["id"])
                else:
                    print(message["message"]["chat"]["title"]+"("+str(message["message"]["chat"]["id"])+")消息："+message["message"]["text"])
                global updateId
                updateId = message["update_id"]+1


def downFile(fileId,file_name,chat_id):
    sendMsg(chat_id,"开始上传>>>>>>>>")
    fileIdUrl = "https://api.telegram.org/bot"+botToken+"/getFile?file_id="+fileId
    response = requests.request("GET", fileIdUrl, data=None, headers=None)
    resultStr = response.text
    result = json.loads(resultStr)
    print(result)
    if (result["ok"]==True):
        filePath = result["result"]["file_path"]
        filePathUrl = "https://api.telegram.org/file/bot"+botToken+"/"+filePath
        print(filePathUrl)
        down_res = requests.request("GET", filePathUrl, data=None, headers=None)
        with open(file_name,"wb") as code:
            code.write(down_res.content)
            print("文件下载成功:"+file_name)
            pushFile()
            sendMsg(chat_id,file_name+"上传成功")


def pushFile():
    dirfile = os.path.abspath('') # code的文件位置，我默认将其存放在根目录下
    repo = Repo(dirfile)
    g = repo.git
    g.add("--all")
    g.commit("-m auto update")
    g.push()
    print("Successful push!")

def sendMsg(chat_id,text):
    url = "https://api.telegram.org/bot"+botToken+"/sendMessage?chat_id="+str(chat_id)+"&text="+text
    response = requests.request("GET", url, data=None, headers=None)
    resultStr = response.text
if __name__ == '__main__':
    # api.run(port=9001, debug=True, host='0.0.0.0')
    while True:
        getUpdates(updateId)
        time.sleep(3)
