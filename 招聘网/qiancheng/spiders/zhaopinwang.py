# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qiancheng.items import QianchengItem
import datetime
from datetime import timedelta
import random
from qiancheng.agent import agent

class ZhaopinwangSpider(CrawlSpider):
    name = 'zhaopinwang'
    allowed_domains = ['lagou.com']
    start_urls = ['http://lagou.com/']
    rules = (
        Rule(LinkExtractor(allow=r'https://www\.lagou\.com/zhaopin/\w+/'),follow=True),
        Rule(LinkExtractor(allow=r'https://www\.lagou\.com/jobs/\d+.html'), callback='parse_detail', follow=False)
    )
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS" : {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_ga=GA1.2.228625670.1531838233; user_trace_token=20180717223713-e5162ace-89ce-11e8-9c70-525400f775ce; LGUID=20180717223713-e5162da4-89ce-11e8-9c70-525400f775ce; _qddaz=QD.lejbop.dpoqhn.jlggn4hk; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAAAFCAAEGA5288FEBE02B3233098A29290217BCC9; TG-TRACK-CODE=index_navigation; X_HTTP_TOKEN=5a85b0a8d7bde1ec8017fc826e18e25f; LGSID=20180902210248-7db6d8a4-aeb0-11e8-b45e-5254005c3644; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D1FF6mHlNPHG5PyDUhlQcPGvc9m82HpNWs4GtTSIfY4RevBgif1mFo_KNOsS_egR-%26wd%3D%26eqid%3Dd4c0e88d00072e14000000035b8bdf71; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fmsg%3Dvalidation%26uStatus%3D2%26clientIp%3D223.104.3.162; _gid=GA1.2.623186379.1535893368; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535710470,1535795243,1535893367,1535893376; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535893376; LGRID=20180902210257-831c7108-aeb0-11e8-b45e-5254005c3644",
            "Host": "www.lagou.com",
            "Referer": "https://www.baidu.com/link?url=CoTraSswAN8sEGFGFNr-Yv0vOAH1mbkPOk8sDBPVFim&wd=&eqid=d4c0e88d00072e14000000035b8bdf71",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",     }
     }

    def parse_detail(self, response):
        title = response.xpath('//div[@class="position-content-l"]//span[@class="name"]/text()').extract_first()
        company = response.xpath('//div[@class="company"]/text()').extract_first()
        money = response.xpath('//span[@class="salary"]/text()').extract_first()
        data_ing = response.xpath('//div[@class="work_addr"]/text()').extract()
        print(data_ing)
        data_ing = ''.join(data_ing).replace('\n', '').strip().replace(' ', '').replace('-', '')
        hangwei = response.xpath('//dd[@class="job_bt"]//text()').extract()
        print(hangwei)
        hangwei = ''.join(hangwei).replace('\n', '').strip().replace(' ', '')
        xueli = response.xpath('//div[@class="position-content-l"]/dd//span[4]/text()').extract()[0]
        tiem_now = response.xpath('//p[@class="publish_time"]/text()').extract()[0]
        if '天前' in tiem_now:  # 判断几天前  把天数出去 减去当前的时间
            num = tiem_now.split('天')
            a = num[0]
            tiem_now = self.day(a)
        else:
            tiem_now_list = tiem_now.split('发')
            tiem_now = tiem_now_list[0]
        # print(title, company, salary, job_adv, job_bt)
        item = QianchengItem()
        item['title'] = title
        item['company'] = company
        item['money'] = money  # 薪资
        item['data_ing'] = data_ing #
        item['hangwei'] = hangwei  # 详情
        item['tiem_now'] = tiem_now  # 时间
        item['xueli'] = xueli  # 时间
        item['http_'] = '拉钩网'  # 时间
        yield item

    def day(self,num):
        '''
        :param num: 要减去时间的天数
        :return:
        : a  当前的日期
        '''
        c = int(num)
        b = timedelta(c)
        a = datetime.datetime.now()
        return (a - b).strftime('%Y-%m-%d')