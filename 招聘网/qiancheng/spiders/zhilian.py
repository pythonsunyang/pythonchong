# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import request
from w3lib.html import remove_tags
from qiancheng.items import QianchengItem
class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://jobs.zhaopin.com/']

    def parse(self, response):
        html = response.text
        a_s = re.findall(r'a href="(sj.*?)" ',html)
        for a in a_s:   # 获取所有类别
            url = 'https://jobs.zhaopin.com/' + a
            yield  scrapy.Request(url=url,callback=self.page_data)
    def page_data(self,response):
        html = response.text
        href_s = re.findall(r'<span class="post"><a href="(.*?)"',html)
        for href in href_s:
            yield scrapy.Request(href,callback=self.page_info)
        try:
            next_href = re.findall(r'<a href="(.*?)" rel=\'nofollow\'>下一页', html)[0]
            next_href1 = request.urljoin(response.url,next_href)
            yield scrapy.Request(next_href1,callback=self.page_data)
        except Exception as e:
            print(e)

    def page_info(self,response):
        # 里面有校园招聘  过滤
        if  'jobs.zhaopin.com' in response.url:
            item = QianchengItem()
            # with open('123.html','wb') as f:
            #     f.write(response.body)
            html = response.text
            pattern = re.compile(r'<h1>(.*?)</h1>',re.S)
            put = pattern.search(html)
            title = put.group(1)  # 标题
            money = re.findall(r'职位月薪：</span><strong>(.*?)<a',html,re.S)[0].replace('&nbsp;','')
            tiem_now = re.findall(r'<span id="span4freshdate">(.*?)</span>',html,re.S)[0]
            data_ing = re.findall(r'<h2>(.*?)<a',html,re.S)[1].strip()  # 公司地址
            if '</h2>' in data_ing:
                data_ing = data_ing.split('</h2>')
                data_ing = data_ing[0].strip()   # 公司地址  里面右 h2 标签的 取出
            data = re.findall(r'<span>工作地点：</span><strong><a target="_blank" href=".*?">(.*?)</a>', html, re.S)[0]
            xueli = re.findall(r'<li><span>最低学历：</span><strong>(.*?)</strong></li>', html, re.S)[0]
            company = re.findall(r'<li><span>最低学历：</span><strong>(.*?)</strong>', html, re.S)[0] # 公司
            hangwei = re.findall(r'<div class="tab-inner-cont">(.*?)<b>工作地址：</b>', html, re.S)[0].strip()  # 详情
            hangwei = remove_tags(hangwei)
            item['title'] = title
            item['company'] = company
            item['data_ing'] = data_ing
            item['xueli'] = xueli
            item['hangwei'] = hangwei
            item['money'] = money
            item['tiem_now'] = tiem_now
            item['http_'] ='智联招聘'
            yield item











                # req = re.findall(r'<h1>(.*?)</h1>',html)[0]
            # print(req)
            # res = req.findall(html)
            # print(res)


