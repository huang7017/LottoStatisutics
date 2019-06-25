from Moduls import Lotto

if __name__ == '__main__':
    obj = Lotto.Lotto('http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx')
    obj.getStatistics()
    obj.setYM(108,5)#設定年月份
    obj.getStatistics()#取得統計