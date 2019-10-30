from time import sleep, gmtime, strftime
import sys


while True:
    time_cur = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(time_cur)
    sleep(10)
