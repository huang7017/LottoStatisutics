from Moduls import Lotto

if __name__ == '__main__':
    obj = Lotto.Lotto('http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx')
    print('6月')
    obj.getStatistics()
    print('5月')
    obj.setYM(108,5)
    obj.getStatistics()
    print('4月')
    obj.setYM(108,4)
    obj.getStatistics()