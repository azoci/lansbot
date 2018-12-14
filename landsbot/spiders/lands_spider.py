import scrapy
import datetime
from landsbot.items import LandsbotItem

class LandsSpider(scrapy.Spider):
  name = 'land'
  land_url = 'https://land.naver.com/article/articleList.nhn?page=1'
  rlet_type_cd = '&rletTypeCd=A01'
  cortar_no = '&cortarNo=1168011500'
  start_urls = [
    land_url + cortar_no + rlet_type_cd
  ]

  def parse(self, response):
    #call page number
    lst = response.url.split('&')
    matched = [x for x in lst if 'page=' in x]
    if len(matched) > 0:
      call_page = int(matched[0].split('=')[1])
    else:
      call_page = 1
    #current page number
    current_page = response.xpath('//div[contains(@class, "paginate")]/strong/text()').extract_first()
    if current_page:
      current_page = int(current_page)
      if call_page <= current_page:
        next_page = current_page + 1
        trlist = response.xpath('//tbody//tr')
        rent_fee = 0
        max_floor = ''
        exclusive_area = ''
        for tr in trlist:
          if tr.xpath('.//td[contains(@class, "sale_type  bottom")]/div/text()').extract_first() is None:
            pass
          else:
            item = LandsbotItem()
            item['ts'] = datetime.datetime.now().isoformat()
            sale_type = tr.xpath('.//td[contains(@class, "sale_type  bottom")]/div/text()').extract_first()
            item['sale_type'] = tr.xpath('.//td[contains(@class, "sale_type  bottom")]/div/text()').extract_first()
            item['building_type'] = tr.xpath('.//td[contains(@class, "sale_type2  bottomline")]/div/text()').extract_first()
            item['building_name'] = tr.xpath('.//td[contains(@class, "align_l name")]/div/a/text()').extract_first()
            #area
            area = tr.xpath('.//td[contains(@class, "num")]/div/text()').extract_first()
            if area:
              area = area.strip()
              item['area'] = area
              a_split = area.split('/')
              item['supply_area'] = a_split[0]
              if len(area) > 1:
                item['exclusive_area'] = a_split[1]
            #floor
            floor = tr.xpath('.//td[contains(@class, "num2")]/div/span/text()').extract_first()
            if floor:
              floor = floor.strip()
              item['floor'] = floor
              f_split = floor.split('/')
              item['sale_floor'] = f_split[0]
              if len(f_split) > 1:
                item['max_floor'] = f_split[1]
            #rent fee
            sale_price = tr.xpath('.//td[contains(@class, "num align_r")]/div/strong/text()').extract_first()
            if sale_price:
              sale_price = sale_price.strip()
              item['sale_price'] = sale_price
              p_split = sale_price.split('/')
              item['deposit'] = int(p_split[0].replace(',', ''))
              if len(p_split) > 1:
                item['rent_fee'] = int(p_split[1].replace(',', ''))
            yield item
        #next page url
        next_page_url = response.url.replace('page=' + str(current_page), 'page=' + str(next_page))
        yield response.follow(next_page_url, self.parse)


