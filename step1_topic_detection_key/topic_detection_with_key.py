# -*- encoding: utf-8 -*-

from unidecode import unidecode
import re


class KeyWordDetection:
    def __init__(self):
        self.keywords = {}
        self.hotkeywords = {}
        self.keywords['0'] = ['CHUNG MINH NHAN', 'THU',
                              'THE CAN CUOC CONG DAN']

        self.hotkeywords['0'] = ['CMT', 'CMND', 'TCC', 'CCCD', 'CMTND']

        self.keywords['9'] = ['VU KHI', 'VAT LIEU NO', 'TRAI PHEP', 'TANG TRU', 'SUNG', 'DAN', 'PHAO', 'BOM', 'MIN',
                              'THUOC NO']

        self.hotkeywords['9'] = ['VK', 'VLN']

    def intent_detection(self, question):
        # bo dau
        question = unidecode(question.decode('utf8'))
        # dua ve in hoa, xoa dau thua, cat phan du o cuoi cau
        upper_question = re.sub('[^A-Za-z0-9]+', ' ', question).upper().strip()
        print (upper_question)
        list_token_upper_question = upper_question.split(" ")

        # check hotkeys 0
        for _ in self.hotkeywords['0']:
            if _ in list_token_upper_question:
                return 0

        # check hotkeys for topic 9
        for _ in self.hotkeywords['9']:
            if _ in list_token_upper_question:
                return 9

        keys = self.keywords.keys()
        statistic = {}
        for key in keys:  # trong cac danh sach keywords voi moi chu de
            count = 0
            # danh sach cac key doi voi moi chu de
            list_keywords = self.keywords[key]

            for item in list_keywords:
                print "Item checked :", item

                list_item = item.split(' ')
                for _ in list_item:  # moi tu trong key
                    if _ in upper_question.split(" "):
                        count = count + 1

            statistic[key] = count
        print statistic
        topic = 'unknown'
        max = 0
        for _ in statistic.keys():
            if statistic[_] > 0 and statistic[_] > max:
                max = statistic[_]
                topic = _
        return topic

    # u"1.CHỨNG MINH THƯ (CMT/CMND)":0,
    # u"1.NƠI TẠM TRÚ":1,
    # u"1.DANH TÍNH TÔI PHẠM":2,
    # u"1.THỜI HẠN TẠM TRÚ":3,
    # u"1.HÀNH VI TỘI PHẠM":4,
    # u"1.CĂN CƯỚC CÔNG DÂN (CCCD)":5,
    # u"1.GIẤY CHỨNG NHẬN/ XÁC NHẬN ĐỦ ĐIỀU KIỆN AN NINH TRẬT TỰ":6,
    # u"1.NƠI THƯỜNG TRÚ":7,
    # u"1.SỔ HỘ KHẨU (THƯỜNG TRÚ) / KT1":8,
    # u"1.TÀNG TRỮ VŨ KHÍ, VẬT LIỆU NỔ":9,
    # u"1.SỔ TẠM TRÚ / KT2 / KT3 / KT4":10,
    # u'other':11

    # keywords = {}

    # keywords['0'] = ['CMT', 'CMND', 'TCC', 'CCCD', 'CMTND', 'CHUNG MINH THU', 'CHUNG MINH THU NHAN DAN',
    #                  'THE CAN CUOC CONG DAN',
    #                  'THE CAN CUOC', 'THE CC', 'THE CC CONG DAN']
    # keywords['1'] = ['NOI TAM TRU', 'NOI TT', 'NTT', 'TAM TRU', 'TT']
    # keywords['2'] = ['LAY CAP', 'MAT CAP', 'TOI PHAM', 'TO CAO', 'CHUNG CU', 'TROM CAP', 'HANG GIA', 'TRAI PHEP',
    #                  'LAM GIA',
    #                  'GIA MAO', 'VU KHONG', 'LUA DAO', 'KICH DONG', 'BAO LUC', 'DANH DAP']
    # keywords['3'] = []
    # keywords['4'] = []
    # keywords['5'] = []
    # keywords['6'] = []
    # keywords['7'] = []
    # keywords['8'] = []
    # keywords['9'] = ['VU KHI', 'VAT LIEU NO', 'TRAI PHEP', 'TANG TRU', 'SUNG', 'DAN', 'PHAO', 'BOM', 'MIN',
    #                  'THUOC NO']
    # keywords['10'] = []
    # keywords['11'] = []


if __name__ == '__main__':
    d = KeyWordDetection()

    st = 'Đối tượng nào thì được chứng minh thư nhân dân?'
    x = d.intent_detection(st)

    print x

# DOI TUONG NAO THI DUOC CAP VU KHI BOM DAN
