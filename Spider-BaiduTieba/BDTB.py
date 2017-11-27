#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2017-10 - aumujun <aumujun@gmail.com> 
__author__ = 'Aumujun'

import re
import urllib.request
import urllib.parse
import urllib.error


class Tool:
    #删除img标签
    filter_img = re.compile(r'<img class="BDE_Image" .*?>| {12}|<img pic_type=".*?>|<img class="BDE_Smiley".*?>')
    #替换br为\n加空格
    filter_br = re.compile(r'<br><br>|<br>')
    #删除a超链接标签
    filter_a = re.compile(r'<a.*?>|</a>|<div class="post_bubble_top".*?>')
    #替换td标签为t
    filter_td = re.compile(r'<td>')



    def replace(self,x):
        x = re.sub(self.filter_img,'',x)
        x = re.sub(self.filter_br,'\n',x)
        x = re.sub(self.filter_a,'',x)
        x = re.sub(self.filter_td,'\t',x)

        return x.strip()


class BDTB:

    def __init__(self,baseUrl,seeLZ):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()

    def getPage(self,pageNum):
        try:
            #将要爬取的帖子链接拼接
            #https://tieba.baidu.com/p/5454958799?fid=46&see_lz=1
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
            #https://tieba.baidu.com/p/5454414515
            request = urllib.request.Request(url)
            request.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
            rsp = urllib.request.urlopen(request)
            rsp = rsp.read().decode('utf8')
            return rsp
        except urllib.error.URLError as e:
            if hasattr(e,'reason'):
                print('连接百度贴吧失败，错误原因：',e.reason)
                return None
    #提取帖子的标题
    def getTitle(self,page):
        # page = self.getPage(1)
        pattern = re.compile(r'<h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>')
        result = pattern.search(page)
        if result:
            return result.group(1)
        else:
            return None
    #获取帖子的总页数
    def getPageNum(self,page):
        # page = self.getPage(1)
        pattern = re.compile(r'<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = pattern.search(page)
        #strip()用于移除字符串首位的字符 默认为空格
        return result.group(1).strip()

    def getContent(self,page):
        pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>',re.S)
        contents = pattern.findall(page)
        louc = 1
        for content in contents:
            print(louc,'Floor:',"="*35+'\n')
            print(self.tool.replace(content)+'\n')
            louc += 1
    #开始部署
    def start(self):
        indexpage = self.getPage(1)
        pageNum = self.getPageNum(indexpage)
        title = self.getTitle(indexpage)
        print('这条帖子一共有',pageNum,'页......')
        for i in range(1,int(pageNum)+1):
            print('===============第 【',i,'】 页===============')
            hqfy = self.getPage(i)
            print(self.getContent(hqfy))
            ...
baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL,0)
bdtb.start()






