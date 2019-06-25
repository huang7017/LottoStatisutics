from bs4 import BeautifulSoup
import requests
import numpy as np
class Lotto:
    def __init__(self,url):
        self.__url = url
        self.__winning_Numbers_Sort_lotto = ['Lotto649Control_history_dlQuery_No1_', 'Lotto649Control_history_dlQuery_No2_',
                                      'Lotto649Control_history_dlQuery_No3_', 'Lotto649Control_history_dlQuery_No4_',
                                      'Lotto649Control_history_dlQuery_No5_', 'Lotto649Control_history_dlQuery_No6_',
                                      'Lotto649Control_history_dlQuery_SNo_']
        self.__res = requests.get(self.__url, timeout=30)
        self.soup = BeautifulSoup(self.__res.text, 'lxml')
    def getVIEWSTATE(self):
        viewstate = self.soup.find(id="__VIEWSTATE")
        viewstate = viewstate.get('value')
        return viewstate
    def getVIEWSTATEGENERATOR(self):
        VIEWSTATEGENERATOR = self.soup.find(id="__VIEWSTATEGENERATOR")
        VIEWSTATEGENERATOR = VIEWSTATEGENERATOR.get('value')
        return VIEWSTATEGENERATOR
    def getEVENTVALIDATION(self):
        EVENTVALIDATION = self.soup.find(id="__EVENTVALIDATION")
        EVENTVALIDATION = EVENTVALIDATION.get('value')
        return EVENTVALIDATION
    def setYM(self,year,month):
        session = requests.Session()
        headers = {
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6,ja;q=0.5',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'9796',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.taiwanlottery.com.tw',
            'Origin': 'http://www.taiwanlottery.com.tw',
            'Referer': 'http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Cookie':'ASPSESSIONIDCAQRDBDB=AENKKMJAHEFAPIDMFCIPLFML; ASPSESSIONIDCASRBBDA=FMACMPKANGBOAGOFLEHNPFMJ; ASPSESSIONIDCATRDBCB=AHNCJAMAOFOAFPONEKOJGFBM; ASPSESSIONIDCCSRCACA=AFKOMFMAABLHHIGCMIFPNHLC; ASPSESSIONIDACQQBBCA=DAJLMPLANPKDBKBPKGNLNMKK; ASPSESSIONIDAATRCADA=LCOEMAMAGGJBBOIPMJPCHLHH; ASPSESSIONIDCCRSCCAA=PONGLDMAIDFPMDMILICLLAEM; ASPSESSIONIDAARSCCAA=FFIMBDCAGIPGPDOMPIIHFMJB; ASPSESSIONIDCATQCADA=DJDEGKNACIPJKAJMKGJBGPEA'
        }
        formdate = {
            '__EVENTTARGET':'',
            '_EVENTARGUMENT':'',
            '__LASTFOCUS':'',
            '__VIEWSTATE': self.getVIEWSTATE(),
            '__VIEWSTATEGENERATOR':self.getVIEWSTATEGENERATOR(),
            '__EVENTVALIDATION':self.getEVENTVALIDATION(),
            'Lotto649Control_history$DropDownList1':'2',
            'Lotto649Control_history$chk':'radYM',
            'Lotto649Control_history$dropYear': year,
            'Lotto649Control_history$dropMonth':month,
            'Lotto649Control_history$btnSubmit':'查詢'
        }
        self.__res = session.post(url=self.__url,data =formdate, headers=headers)
        self.soup = BeautifulSoup(self.__res.text, 'lxml')
    def search_winning_numbers(self,css_class):
        if (css_class != None):
            for i in range(len(self.__winning_Numbers_Sort_lotto)):
                if self.__winning_Numbers_Sort_lotto[i] in css_class:
                    return css_class
    def parse_tw_lotto_html(self,data_Info, number_count):
        data_Info_List = []
        data_Info_Dict = {}
        tmp_index = 0
        for index in range(len(data_Info)):
            if (index == 0):
                data_Info_List.append(data_Info[index].text)
            else:
                if (index % number_count != 0):
                    data_Info_List.append(data_Info[index].text)
                else:
                    data_Info_Dict[str(tmp_index)] = list(data_Info_List)
                    data_Info_List = []
                    data_Info_List.append(data_Info[index].text)
                    tmp_index = tmp_index + 1
            data_Info_Dict[str(tmp_index)] = list(data_Info_List)
        return data_Info_List, data_Info_Dict
    def getLottoNumber(self):
        header_Info = self.soup.find_all(id=self.search_winning_numbers)
        data_Info_List, data_Info_Dict = self.parse_tw_lotto_html(header_Info, 7)
        return data_Info_Dict
    def getStatistics(self):
        dict = self.getLottoNumber()
        list = []
        Statistics = np.zeros(49)
        for i in range(len(dict)):
            list.append(dict.get(str(i)))
        for i in range(len(list)):
            for j in range(7):
                Statistics[int(list[i][j])]+=1
        for i in range(np.size(Statistics)):
            print(str(i+1)+':',end = '')
            print(int(Statistics[i]),end = ' ')
        print()

if __name__ == '__main__':
    obj = Lotto('http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx')
    obj.getStatistics()
    obj.setYM(108,5)
    obj.getStatistics()
