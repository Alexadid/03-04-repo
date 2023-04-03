import RPi.GPIO as gpio
import time as tm


# Настройка Малинки
gpio.setmode(gpio.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
# Troyka-модуль
troyka = 17
gpio.setup(dac, gpio.OUT)
gpio.setup(troyka, gpio.OUT, initial=gpio.HIGH)
gpio.setup(comp, gpio.IN)


# Функция перевода в двоичную систему
def translate(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]


# Функция возвращает десятичное число, пропорциональное напряжению клемме S Troyka-модуя
def adc():
    for i in range(256):
        dacc = translate(i)
        gpio.output(dac, dacc)
        compvalue = gpio.input(comp)
        tm.sleep(0.01)
        if compvalue == 0:
            return i


try:
    while True:
        i = adc()
        if i != 0:
            print(i, '{:.2f}v'.format(3.3 * i / 256))
finally:
    gpio.output(dac, 0)
    gpio.cleanup()