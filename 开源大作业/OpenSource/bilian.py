import re
import requests
from lxml import etree
import csv

# 存储总共爬取的条数
climbnum = 0
# 存储的数据格式
sql_data = dict(
    web = '',   #信息来源网站
    keyword = '',   #关键字
    detail_url = '',    #招标详细页网址
    title = '', #第三方网站发布标题
    toptype = '',   #信息类型
    province = '',  #归属省份
    prodect = '',   #产品范畴
    tendering_manner = '',  #招标方式
    publicity_date = '',    #招标公示日期
    expiry_date = '',   #招标截止时间
)

#csv文件的表头
CSVHEADER = ['web','keyword','detail_url','title','toptype','province','prodect','tendering_manner','publicity_date','expiry_date']

#请求时带的数据
params = dict(
    infoClassCodes='',
    rangeType='',
    projectType='bid',
    fundSourceCodes='',
    dateType='',
    startDateCode='',
    endDateCode='',
    normIndustry='',
    normIndustryName='',
    zone='',
    zoneName='',
    zoneText='',
    key='',  # keyword
    pubDateType='',
    pubDateBegin='',
    pubDateEnd='',
    sortMethod='timeDesc',
    orgName='',
    currentPage='1',  # page
)
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Host':'ss.ebnew.com',
    'cookie':'loginUser=; __cfduid=daa1311ae7cd31fd395f7e3251e7770671608880455; Hm_lvt_ce4aeec804d7f7ce44e7dd43acce88db=1608880460; JSESSIONID=5644896A631BE3652EA3853BEE69DF00; Hm_lpvt_ce4aeec804d7f7ce44e7dd43acce88db=1608881105'
}

COOKIES = 'loginUser=; __cfduid=daa1311ae7cd31fd395f7e3251e7770671608880455; Hm_lvt_ce4aeec804d7f7ce44e7dd43acce88db=1608880460; JSESSIONID=5644896A631BE3652EA3853BEE69DF00; Hm_lpvt_ce4aeec804d7f7ce44e7dd43acce88db=1608881105'

def write_csv(datas):
    global CSVHEADER
    with open('result.csv','a',newline='',encoding='utf-8') as f1:
        writer = csv.DictWriter(f1,fieldnames=CSVHEADER)
        with open("result.csv", "r", newline="",encoding='utf-8') as f2:
            reader = csv.reader(f2)
            # 判断是否存在标题，不存在则写入标题
            if not [row for row in reader]:
                writer.writeheader()
                writer.writerow(datas)
            else:
                writer.writerow(datas)

def start_requests(keyword,page):
    '''
    开始请求，并返回html对象
    :param self:
    :return:
    '''
    global DEFAULT_REQUEST_HEADERS
    global params
    params['key'] = keyword
    params['currentPage'] = page
    try:
        response = requests.get(
            url='https://ss.ebnew.com/tradingSearch/index.htm',
            params=params,
            headers=DEFAULT_REQUEST_HEADERS
        )
        html = etree.HTML(response.text)
        return html
    except:
        print('未知错误')
        return None

def pagenum_get(html):
    '''
    用于提取总页数
    :param html:
    :return:
    '''
    page_num = html.xpath('//form[@id="pagerSubmitForm"]/a/text()')
    if page_num:
        return page_num

def pagedata_get(html):
    global sql_data
    global params
    global climbnum
    content_list_x_s = html.xpath('//div[@class="ebnew-content-list"]/div')
    for content_list_x in content_list_x_s:
        toptype = content_list_x.xpath('./div/i[1]/text()')
        title = content_list_x.xpath('./div/a/text()')
        publicity_date = content_list_x.xpath('./div/i[2]/text()')
        tendering_manner = content_list_x.xpath('./div[2]/div[1]/p[1]/span[2]/text()')
        prodect = content_list_x.xpath('./div[2]/div[1]/p[2]/span[2]/text()')
        expiry_date = content_list_x.xpath('./div[2]/div[2]/p[1]/span[2]/text()')
        province = content_list_x.xpath('./div[2]/div[2]/p[2]/span[2]/text()')

        sql_data['toptype'] = toptype[0] if toptype else None
        sql_data['title'] = title[0] if title else None
        sql_data['publicity_date'] = publicity_date[0] if publicity_date else None
        if sql_data['publicity_date']:
            sql_data['publicity_date'] = re.sub('[^0-9\-]', '', sql_data['publicity_date'])
        sql_data['tendering_manner'] = tendering_manner[0] if tendering_manner else None
        sql_data['prodect'] = prodect[0] if prodect else None
        sql_data['expiry_date'] = expiry_date[0] if expiry_date else None
        sql_data['province'] = province[0] if province else None
        sql_data['keyword'] = params['key']
        sql_data['web'] = '必联网'
        sql_data['detail_url'] = content_list_x.xpath('./div/a/@href')[0] if content_list_x.xpath('./div/a/@href') else None
        write_csv(sql_data)
        climbnum += 1

def start_climb(key,pages):
    '''
    图形界面的开始爬取集合方法
    :param key:
    :param page:
    :return:
    '''
    for page in range(1,pages+1):
        print(page)
        pagedata_get(start_requests(keyword=key,page=page))
        print('已经完成第'+str(page)+'页爬取！')

