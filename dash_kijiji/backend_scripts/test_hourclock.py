from time import sleep, strftime


while True:
    time_cur = strftime("%Y-%m-%d %H:%M")
    print(time_cur)
    sleep(60)
