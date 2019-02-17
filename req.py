#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import os, sys
from pathlib import Path

# 封装下载图片方法
def downloadPic(src, id, targetFolder):
	dir = './' + targetFolder + '/' + str(id) + '.jpg'
	try:
		pic = requests.get(src, timeout = 10)
		fp = open(dir, 'wb')
		fp.write(pic.content)
		fp.close()
	except requests.exceptions.ConnectionError:
		print("图片无法下载")

doubanPicUrl = 'https://www.douban.com/j/search_photo'
queryName = input("请输入你的女神？")

# 如果目录不存在则创建一个目录，来存放即将要下载的照片
folder = Path('./' + queryName)
if Path(folder).exists():
    print(queryName + '目录已经存在')
else:
	os.mkdir('./' + queryName)

# 请求查看名人的图片库信息
resText = requests.get(doubanPicUrl + '?q=' + queryName + '&limit=1&start=0').text

# 将返回的 Json 内容转换为 python 对象
resJson = json.loads(resText, encoding='utf-8')
total = resJson['total']
print("总共发现女神照片" + str(total) + '张')
print("开始下载女神照片")

# 开始循环请求女神照片，并且下载
for i in range(0, total, 20):
    queryUrl = doubanPicUrl + '?q=' + queryName + '&limit=20&start=' + str(i)
    resText = requests.get(queryUrl).text
    resJson = json.loads(resText, encoding='utf-8')
    for image in resJson['images']:
    	print('下载图片：' + image['src'])
    	downloadPic(image['src'], image['id'], queryName)
