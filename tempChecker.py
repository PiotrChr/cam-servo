import time
import re
import subprocess

temp_pattern = re.compile(r'^temp=(.*?)\'C.*$')

limit_temp = 80.0

while (True):
    temp = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    temp_new = float(temp_pattern.sub(r'\1', temp.stdout.decode('UTF-8')))
    
    if temp_new > limit_temp:
        subprocess.run(['sudo reboot'])
    else:
        print(temp_new)
    
    # print(temp)
    time.sleep(5)