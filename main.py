__author__ = 'Acheron'

import sys
import socket
from PyQt4 import QtGui, QtCore, Qt
from design import Ui_MainWindow
from prefs import Ui_PrefWindow
import random
import re
import os
import datetime

import asyncio
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair

class GSMGateway(QtCore.QThread):

    def __init__(self, loop, auth, ip, port=5038, SIMSlot=2, numbers_list=[], text=''):
        super().__init__()
        self.loop = loop
        self.ip = ip
        self.port = port
        assert len(auth) == 2, 'Login or password missed! Should be (login, password)'
        self.user, self.password = auth
        self.SIM = SIMSlot
        self.numbers = numbers_list
        self.text = text
        self.num_id = str(random.randint(10,10000))

    def run(self):
        reader, writer = self.loop.run_until_complete(self.login(self.loop))
        self.loop.run_until_complete(self.sendSMS(reader, writer))

    @asyncio.coroutine
    def login(self, loop):

        action = b'action: Login\r\n'
        username = ('username: {0}\r\n'.format(self.user)).encode()
        secret = ('secret: {0}\r\n\r\n'.format(self.password)).encode()
        data_auth = action + username + secret


        reader, writer = yield from asyncio.open_connection(self.ip, self.port, loop=loop)
        stage = 0
        self.emit(QtCore.SIGNAL("response(PyQt_PyObject)"), (stage,'Connection established'))

        writer.write(data_auth)

        response = ''
        while True:
            data = yield from reader.readline()
            if data == b'\r\n':
                break
            response += data.decode()
        stage = 1
        self.emit(QtCore.SIGNAL("response(PyQt_PyObject)"), (stage,response))
        return reader, writer

    @asyncio.coroutine
    def sendSMS(self, reader, writer):
        for number in self.numbers:
            action = b'Action: SMSCommand\r\n'
            command = b'command: gsm send sms ' + self.SIM.encode() + b' ' + number.encode() \
                       + b' "' + self.text.encode() + b'" ' + self.num_id.encode() + b'identifier\r\n\r\n'
            cmd = action + command
            writer.write(cmd)
            response = ''
            while True:
                data = yield from reader.readline()
                if data == b'\r\n':
                    break
                response += data.decode()
            self.num_id = str(int(self.num_id)+1)
            stage = 2
            response += 'Number: %s' % number
            print(response)
            self.emit(QtCore.SIGNAL("response(PyQt_PyObject)"), (stage,response))

    def readResponse(self, reader):
        print('Read response')
        print(reader)
        while True:
            data = yield from reader.readline()
            if data == b'\r\n':
                break
            # print(data.decode())
        return data.decode()

class Preferences(QtGui.QMainWindow, Ui_PrefWindow):

    def __init__(self, config):
        super().__init__()
        self.ui = Ui_PrefWindow()
        self.ui.setupUi(self)
        self.config = config

        self.ui.btn_cancel.clicked.connect(self._exit)
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_def.clicked.connect(self.default)

        self.initilize()

    def initilize(self):
        self.ip = self.config['gateway']
        self.port = self.config['port']
        self.sim_slot = self.config['simslot']
        self.usr = self.config['username']
        self.psw = self.config['password']
        self.sanitarize = self.config['sanitarize']

        self.ui.txt_addr.clear()
        self.ui.txt_addr.insertPlainText(self.config['gateway'] + ':' + self.config['port'])

        if self.sanitarize == 'true':
            self.ui.chk_num_auto.setChecked(True)
        else: self.ui.chk_num_auto.setChecked(False)

        for i in range(1,5):
            self.ui.cmb_slot.addItem(str(i))
        self.ui.cmb_slot.setCurrentIndex(int(self.sim_slot)-1)

    def _exit(self):
        self.close()

    def save(self):
        cat = os.path.split(os.path.abspath(__file__))[0]
        filename = os.path.join(cat,'config.txt')
        config = dict()

        with open(filename, 'w') as f:
            ip, port = self.ui.txt_addr.toPlainText().split(':')
            f.write('gateway=' + ip +'\n')
            f.write('port=' + port + '\n')
            f.write('username=' + self.usr + '\n')
            f.write('password=' + self.psw + '\n')
            self.sim_slot = str(self.ui.cmb_slot.currentIndex()+1)
            f.write('simslot=' + self.sim_slot + '\n')
            if self.ui.chk_num_auto.isChecked:
                f.write('sanitarize=true' + '\n')
                self.config['sanitarize'] = 'true'
            else:
                f.write('sanitarize=false' + '\n')
                self.config['sanitarize'] = 'false'

            self.config['gateway'] = ip.replace('\n','')
            self.config['port'] = port.replace('\n','')
            self.config['simslot'] = str(self.ui.cmb_slot.currentIndex() +1 )


            self.emit(QtCore.SIGNAL("config(PyQt_PyObject)"), (self.config))
            self.emit(QtCore.SIGNAL("response(PyQt_PyObject)"), (7, filename))
            self.close()

    def default(self):
        self.config = {
            'gateway':'192.168.1.150',
            'port':'5038',
            'username':'apiuser',
            'password':'apipass',
            'simslot':'2',
            'sanitarize':'true'
        }
        self.initilize()

class MainFrame(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, loop, config):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.config = config
        self.ui.txt_log.insertPlainText('Файл настроек загружен.')

        self.prefs_window = None

        self.ui.menu_exit.triggered.connect(self._exit)
        self.ui.menu_preferences.triggered.connect(self.prefs_open)
        self.ui.menu_open.triggered.connect(self.open_dialog)
        self.ui.menu_save.triggered.connect(self.save)
        self.ui.menu_save_as.triggered.connect(self.save_as)
        self.ui.menu_create.triggered.connect(self.clear_numbers)

        self.ui.btn_exit.clicked.connect(self._exit)
        self.ui.btn_send.clicked.connect(self.send)

        self.loop = loop

    def _exit(self):
        sys.exit()

    def open_dialog(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Открыть файл списка номеров", "", "text file (*.txt)")
        if os.path.exists(file_name):
            self.ui.txt_sms_num.clear()
            with open(file_name, 'r') as f:
                self.ui.txt_sms_num.insertPlainText(f.read())
            self.response_decode((5, file_name))

    def save(self):
        file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
        cat = os.path.split(os.path.abspath(__file__))[0]
        full_path = os.path.join(cat, file_name)
        with open(full_path, 'w') as f:
            f.write(self.ui.txt_sms_num.toPlainText())
        self.response_decode((6, file_name))

    def save_as(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Сохранить файл с номерами как", "", "text file (*.txt)")
        cat = os.path.split(os.path.abspath(__file__))[0]
        full_path = os.path.join(cat, file_name)
        with open(full_path, 'w') as f:
            f.write(self.ui.txt_sms_num.toPlainText())
        self.response_decode((6, file_name))

    def clear_numbers(self):
        self.ui.txt_sms_num.clear()


    def prefs_open(self):
        if self.prefs_window is None:
            self.prefs = Preferences(self.config)
            self.connect(self.prefs, QtCore.SIGNAL('config(PyQt_PyObject)'), self.reload_config)
            self.connect(self.prefs, QtCore.SIGNAL("response(PyQt_PyObject)"), self.response_decode)
            self.prefs.show()

    def reload_config(self, config):
        self.config = config

    def sanitarize_numbers(self):
        pattern = re.compile(r'\d+', flags=re.IGNORECASE)

        numbers = list(self.ui.txt_sms_num.toPlainText().split('\n'))

        phone_numbers = []
        for number in numbers:
            digits = re.findall(pattern, number)
            fixed_number = ''
            if len(digits) > 1:
                for digit in digits:
                    fixed_number += digit
                phone_numbers.append(fixed_number)
            elif len(digits) == 1:
                phone_numbers.append(digits[0])
        return phone_numbers

    def sanitarize_text(self):
        text = self.ui.txt_sms_text.toPlainText()
        pattern = re.compile(r'([\"\'])', flags=re.IGNORECASE)
        r_pattern = re.compile(r'[\"\']', flags=re.IGNORECASE)
        index = re.findall(pattern, text)

        if len(index) != 0:
            for i in range(1, len(index)+1):
                print(i%2)
                if i % 2 == 1:
                    text = re.sub(r_pattern, "<<", text, 1)
                elif i % 2 == 0:
                    text = re.sub(r_pattern, ">>", text, 1)
        return text

    def send(self):
        # Следующие аргументы должны быть загружены из файла в момент инициализации!!!
        numbers = list(self.ui.txt_sms_num.toPlainText().split('\n'))
        sms_text = self.ui.txt_sms_text.toPlainText()


        if self.config['sanitarize'] == 'true':
            numbers = self.sanitarize_numbers()
            sms_text = self.sanitarize_text()
        if numbers[0] == '':
            self.ui.txt_log.insertPlainText('Не указано ни одного номера телефона для отправки!\n')
        else:
            print(sms_text)
            self.GSM = GSMGateway(self.loop,(self.config['username'], self.config['password']),
                                  self.config['gateway'], SIMSlot=self.config['simslot'],
                                  numbers_list=numbers, text=sms_text)
            self.connect(self.GSM, QtCore.SIGNAL("response(PyQt_PyObject)"), self.response_decode)
            self.GSM.start()

    def response_decode(self, response):
        stage, data = response
        if stage == 0:
            if data == 'Connection established':
                self.ui.txt_log.insertPlainText('\nСоединение с шлюзом установлено успешно.')
            else:
                self.ui.txt_log.insertPlainText('\nНевозможно установить соединение со шлюзом.')
        elif stage == 1:
            if 'Success' in data:
                self.ui.txt_log.insertPlainText('\nДанные авторизации приняты')
            else:
                self.ui.txt_log.insertPlainText('\nШлюз отверг запрос авторизации')
        elif stage == 2:
            pattern = re.compile(r"\w+:\s?(\d+)", flags=re.IGNORECASE)
            if 'failed' in data:
                number = re.findall(pattern, data)[0]
                self.ui.txt_log.insertPlainText('\nОшибка отправки СМС на номер: %s' % number)
            elif 'Response: Follows' in data:
                number = re.findall(pattern, data)[0]
                self.ui.txt_log.insertPlainText('\nСМС отправлена на номер: %s' % number)
        #-------------------------------------------------------------------------------------
        elif stage == 5:
            self.ui.txt_log.insertPlainText('\nЗагружен файл списка номеров: %s' % data)
        elif stage == 6:
            self.ui.txt_log.insertPlainText('\nСохранен файл списка номеров: %s' % data)
        elif stage == 7:
            self.ui.txt_log.insertPlainText('\nФайл настроек изменен: %s' % data)

def load_config():
    cat = os.path.split(os.path.abspath(__file__))[0]
    filename = os.path.join(cat,'config.txt')
    config = dict()

    with open(filename, 'r') as f:
        while True:
            try:
                k, v = f.readline().split('=')
                config[k] = v.replace('\n','')
            except ValueError:
                break
    return config

def main(loop):
    app = QtGui.QApplication(sys.argv)
    config = load_config()
    myapp = MainFrame(loop, config)
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    try:
        loop.run_until_complete(main(loop))
        loop.run_forever()
    finally:
        loop.close()
