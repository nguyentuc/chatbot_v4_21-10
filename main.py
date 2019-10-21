# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import os
from unidecode import unidecode
import aiml
import json

from logger import logger
from vietnamese_accentizer.accentizer import accentizer
from vietnamese_accentizer.verify_RF_result import verify_RF

app = Flask(__name__)
from gtel_chatbot.bot_brain import brain_bot

brain_bot = brain_bot()
brain_bot.run()

accent = accentizer('vietnamese_accentizer')

accent.run(None, None)

verify = verify_RF('vietnamese_accentizer')
verify.run(None)

x = u'xin chao viet nam'
xx = accent.predict(x)

print verify.verify_result(xx)


@app.route("/")
def hello():
    return render_template('chat.html')


@app.route("/ask", methods=['POST'])
def ask():
    message = request.form['messageText'].encode('utf-8').strip()
    # nhan input va khu dau tieng viet
    string_input = unidecode(message.decode('utf8'))

    kernel = aiml.Kernel()

    # check chu de cho cau hoi roi load cac chu de tuong tung
    from step1_topic_detection_key.topic_detection_with_key import KeyWordDetection
    detection_topic = KeyWordDetection()

    # kiem tra va check chu de cho du lieu nhap vao.
    # question = []
    # question.append(message.decode('unicode-escape'))
    x = detection_topic.intent_detection(message)  # x: topic_ id nhan gia tri tu 0 den 12
    topic = x
    print "Type topic: ", topic

    # check topic, if it unknown we can get it from last topic_id in log db

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

    if topic != 'unknown' and int(topic) in range(11):
        if os.path.isfile("bot_brain/bot_brain_" + str(topic) + ".brn"):
            kernel.bootstrap(brainFile="bot_brain/bot_brain_" + str(topic) + ".brn")
        else:
            kernel.bootstrap(learnFiles=os.path.abspath("learningFileList/learningFileList_" + str(topic) + ".aiml"),
                             commands="LEARN AIML")
            kernel.saveBrain("bot_brain/bot_brain_" + str(topic) + ".brn")
            # bot_brain_x : du lieu load aiml cua cau hoi lien quan chu de co id la x

    # kernel now ready for use
    while True:
        reply = kernel.respond(string_input)
        print "reply: ", reply

        if reply:  # check cau tra loi dua tren he thong build file aiml.
            with open('rules/rule_' + str(topic) + '.json', 'r') as myfile:
                data = myfile.read()

            rules = json.loads(data)['rules']
            answer = ""
            link = ""
            for r in rules:
                if r['key'] == reply:
                    answer = r['value']
                    link = r['link']
                    break
            logger.info('question_aiml: %s, answer_aiml: %s' % (string_input, answer))
            if link == "":
                return jsonify({'status': 'OK',
                                'answer': answer,
                                'flag': 0})
            return jsonify({'status': 'OK',
                            'answer': answer,
                            'link': link,
                            'flag': 1})


        # check cau tra loi tren he thong tim cau hoi tuong dong
        elif brain_bot.thinking(unicode(message, "utf-8")):
            logger.info(
                'question_sys2tuongdong: %s, answer_sys2tuongdong: %s' % (
                    string_input, brain_bot.thinking(unicode(message, "utf-8"))))
            return jsonify({'status': 'OK',
                            'answer': brain_bot.thinking(unicode(message, "utf-8")),
                            'flag': 2})
        else:
            return jsonify({'status': 'OK',
                            'answer': "Tôi đang không hiểu ý bạn là gì, bạn hãy đưa câu hỏi cụ thể hơn được không ?"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
