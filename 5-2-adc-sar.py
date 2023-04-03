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


# Функция adc() с алгоритмом последовательного приближения
def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2**i
        gpio.output(dac, translate(k))
        tm.sleep(0.01)
        if gpio.input(comp) == 0:
            k -= 2**i
    return k


try:
    while True:
        k = adc()
        if k != 0:
            print(k, '{:.2f}v'.format(3.3 * k / 256))
finally:
    gpio.output(dac, 0)
    gpio.cleanup()   