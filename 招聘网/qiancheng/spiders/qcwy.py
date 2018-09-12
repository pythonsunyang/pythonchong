# -*- coding: utf-8 -*-
import scrapy
from qiancheng.items import QianchengItem
class QcwySpider(scrapy.Spider):
    name = 'qcwy'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,32,9,99,%2520,2,1.html']
    def parse(self, response):
        divs = response.xpath('//div[@class="el"]')[4:] # 得到全部
        for div in divs:  # 获取每一个工作的详情信息
            href_url = div.xpath('./p/span/a/@href').extract()[0]
            html = scrapy.Request(url=href_url, callback=self.page_info,meta={'url':href_url})
            yield html
        # 获取下一页回调他本身
        next_page = response.xpath('//div[@class="p_in"]/ul/li/a/@href')[-1].extract()
        yield scrapy.Request(url=next_page,callback=self.parse,meta={'download_timeout': 10},dont_filter=False)

    def page_info(self,response): #class="cn" //div[@class="cn"]/p[2]/text()[5]
        item = QianchengItem()
        url = response.meta['url']
        if 'jobs.51job.com' in url:
            title = response.xpath('//h1/text()').extract()[0].strip()
            company = response.xpath('//div[@class="cn"]/p/a/@title').extract()[0].strip()  # 公司名称
            data_ing = response.xpath('//div[@class="cn"]/p[2]/text()[1]').extract()[0].strip()  # 工作地址
            xueli = response.xpath('//div[@class="cn"]/p[2]/text()[3]').extract()[0].strip()  # 学历
            if '人' in xueli:
                xueli = '不需要学历'
            hangwei = response.xpath('//div[@class="bmsg job_msg inbox"]//text()').extract()   #岗位职责 #任职资格
            hangwei = "".join(hangwei).split()  # 转化字符串   在取空格变成列表
            hangwei = "".join(hangwei)  # 在转化为字符串拼接
            tiem_now = ''
            money ='不给钱'
            try:
                if response.xpath('//div[@class="cn"]/strong/text()'):
                    money = response.xpath('//div[@class="cn"]/strong/text()').extract()[0].strip()  # 金额
                if response.xpath('//div[@class="cn"]/p[2]/text()[5]'):
                    tiem_now = response.xpath('//div[@class="cn"]/p[2]/text()[5]').extract()[0].strip()  # 发布时间
            except Exception as e:
                print(e)
            item['title'] = title
            item['company'] = company
            item['data_ing'] = data_ing
            item['xueli'] = xueli
            item['hangwei'] = hangwei
            item['money'] = money
            item['tiem_now'] = tiem_now
            item['http_'] = '51job'
            yield item
        else:
            pass






