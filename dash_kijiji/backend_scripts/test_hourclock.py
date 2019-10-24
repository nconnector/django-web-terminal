from time import sleep, gmtime, strftime

for i in range(24):
    time_cur = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(time_cur)
    sleep(2)
# sleep(60*60)
