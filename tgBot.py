# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2022/04/09 21:27
# @author  : xiaomi
from git import Repo
from turtle import update
import requests
import time,os, json

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
            chat_id = message["message"]["chat"]["id"]
            if (message["message"]["chat"]["id"]==listem_id):
                if("document" in message["message"]):
                    file_name = message["message"]["document"]["file_name"]
                    downFile(message["message"]["document"]["file_id"],file_name,chat_id)
                else:
                    text = message["message"]["text"]
                    print(message["message"]["chat"]["title"]+"("+str(message["message"]["chat"]["id"])+")消息："+text)
                    if("删除 " in text):
                        fileName = text.split( )[1]
                        sendMsg(chat_id,"开始删除: "+fileName)
                        try:
                            os.unlink(fileName)
                        except:
                            sendMsg(chat_id,"本地文件不存在")
                        if(pushFile()):
                            sendMsg(chat_id,fileName+"删除成功")
                        else:
                            sendMsg(chat_id,fileName+"删除失败,网络异常")
                global updateId
                updateId = message["update_id"]+1


def downFile(fileId,file_name,chat_id):
    sendMsg(chat_id,"开始上传:"+file_name)
    fileIdUrl = "https://api.telegram.org/bot"+botToken+"/getFile?file_id="+fileId
    response = requests.request("GET", fileIdUrl, data=None, headers=None)
    resultStr = response.text
    result = json.loads(resultStr)
    print(result)
    if (result["ok"]==True):
        filePath = result["result"]["file_path"]
        filePathUrl = "https://api.telegram.org/file/bot"+botToken+"/"+filePath
        down_res = requests.request("GET", filePathUrl, data=None, headers=None)
        with open(file_name,"wb") as code:
            code.write(down_res.content)
            print("文件下载成功:"+file_name)
            pushResult = pushFile()
            if(pushFile):
                sendMsg(chat_id,file_name+"上传成功")
                return
            sendMsg(chat_id,file_name+"上传失败,网络异常")

def pushFile():
    dirfile = os.path.abspath('') # code的文件位置，我默认将其存放在根目录下
    repo = Repo(dirfile)
    g = repo.git
    g.add("--all")
    try:
        g.commit("-m auto update")
    except:
        print("没有任何改变,无须更新")
        return True
    try:
        g.push()
        return True
    except:
        print("上传失败")
        return False

def sendMsg(chat_id,text):
    url = "https://api.telegram.org/bot"+botToken+"/sendMessage?chat_id="+str(chat_id)+"&text="+text
    response = requests.request("GET", url, data=None, headers=None)
    resultStr = response.text
if __name__ == '__main__':
    # api.run(port=9001, debug=True, host='0.0.0.0')
    while True:
        getUpdates(updateId)
        time.sleep(3)
