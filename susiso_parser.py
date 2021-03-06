from bs4 import BeautifulSoup as bs
import requests
import re

class susiso_parser(object):
    def __init__(self):
        self.susiso_url = 'http://smartsw.ssu.ac.kr'
        self.url_base = 'http://smartsw.ssu.ac.kr/rb/?c=2/38'

    def refresh_notification(self):
        self.r = requests.get(self.url_base)
        self.soup = bs(self.r.text, 'html.parser')
        self.bbs = self.soup.find('div', {'id':'bbslist'})
        date = re.compile(r"\d{4}.\d{2}.\d{2}")#date pattern YYYY.MM.DD

        self.notis =[noti.text for noti in self.bbs.find_all('span', {'class':'subject'})]
        self.dates =[re.search(date,tr.text).group() for tr in self.bbs.find_all('div',{'class':'info'})]
        self.links =[re.search(r'/rb.*\d{4}', tr.get('onclick')).group()\
                     for tr in self.bbs.find_all('div', {'class':'list'})]

        self.my_tb = zip(self.notis, self.dates, self.links)

    def get_notification_with_link(self):
        ret = ''
        self.refresh_notification()
        
        for noti, date, link in self.my_tb:
            ret += '<a href={link}>{notification}</a> \n{date}\n'.format(
                    link=
                    '{head_url}{tail_url}'.format(head_url=self.susiso_url,tail_url=link),
                    notification=noti,
                    date=date)
            ret.replace('\t', '')
        return ret
    
    def get_notification(self):
        ret = ''
        self.refresh_notification()
        
        for noti, date, link in self.my_tb:
            ret += '{notification} {date}\n'.format(
                    notification=noti,
                    date=date)
            ret.replace('\t', '')
        return ret

