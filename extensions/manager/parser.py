
import re

from bs4 import BeautifulSoup

from bases.exceptions import NotFoundError


class ManagementParser:

    @staticmethod
    def parse_manager(response):
        if response.status_code == 404:
            raise NotFoundError('管理人页面404！')

        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}

        span = soup.find('span', text='机构信息')
        tds = span.parent.parent.find_all('td', attrs={'class': 'title', 'style': None})
        for td in tds:
            value = td.find_next('td').string
            data[td.string or td.div.string] = value and value.strip()

        span = soup.find('span', text='会员信息')
        tds = span.parent.parent.find_all('td', attrs={'class': 'title'})
        for td in tds:
            value = td.find_next('td').string
            data[td.string] = value and value.strip()

        span = soup.find('span', text='法律意见书信息')
        tds = span.parent.parent.find_all('td', attrs={'class': 'title'})
        for td in tds:
            value = td.find_next('td').string
            data[td.string] = value and value.strip()

        td = soup.find('td', text='实际控制人姓名 / 名称')
        data['实际控制人姓名 / 名称'] = td.find_next('td').string.strip()

        td = soup.find('td', text='机构信息最后更新时间')
        data['机构信息最后更新时间'] = td.find_next('td').string

        data['高管信息'] = []
        span = soup.find('span', text='高管信息')
        tds = span.parent.parent.find_all('td', attrs={'class': 'title'})
        for td in tds:
            key = td.string
            if key == '职务':
                data['高管信息'].append({})

            if key == '工作履历':
                value = [
                    [td.string and td.string.strip() for td in tr.find_all('td')]
                    for tr in td.find_next('tbody').find_all('tr')
                ]
            else:
                value = td.find_next('td').string.strip()

            data['高管信息'][-1][key] = value

        data['关联方信息'] = []
        td = soup.find('td', attrs={'class': 'title'}, text='关联方')
        for tr in td.find_next('tbody').find_all('tr'):
            data['关联方信息'].append([tr.a['href'][:-5], *(td.string.strip() for td in tr.find_all('td'))])

        data['出资人信息'] = []
        td = soup.find('td', attrs={'class': 'title'}, text='出资人')
        for tr in td.find_next('tbody').find_all('tr'):
            data['出资人信息'].append([td.string.strip() for td in tr.find_all('td')])

        links = soup.find_all('a', attrs={'href': re.compile(r'../fund/.*.html')})
        data['fund_ids'] = [link['href'].split('/')[-1].split('.')[0] for link in links]
        return data

    @staticmethod
    def parse_fund(response):
        if response.status_code == 404:
            raise NotFoundError('基金页面404！')

        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}

        tds = soup.find_all('td', attrs={'class': 'title'})
        for td in tds:
            value = td.find_next('td').string
            data[td.string] = value and value.strip()

        links = soup.find_all('a', attrs={'href': re.compile(r'../manager/.*.html')})
        data['manager_ids'] = [link['href'].split('/')[-1].split('.')[0] for link in links]
        return data

