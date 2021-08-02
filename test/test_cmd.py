import subprocess

order = 'ping baidu.com'

pi = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pi2 = subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
pi2.kill()
c = 0
try:
    for i in iter(pi.stdout.readline, 'b'):
        if not i:
            break
        c += 1
        print(c)
        if c == 5:
            pi.kill()
        print(i.decode('utf8'))
except KeyboardInterrupt:
    print('stop')