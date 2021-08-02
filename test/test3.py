import time

from PyQt5.QtCore import QTime, qRound, QDateTime

git
def my_time(ms: int):
    h = int(ms / 3600000)
    ms %= 3600000
    m = int(ms / 60000)
    ms %= 60000
    s = int(ms / 1000)
    return str(h)+':'+str(m)+':'+str(s)


def date_time(ms: int):
    datetime = QDateTime()
    return datetime.fromMSecsSinceEpoch(ms).toString("hh:mm:ss")


def q_time(ms: int):
    time = QTime(0, int(ms / 60000), int(qRound(ms / 60000) / 1000.0))
    return time.toString("mm:ss")


if __name__ == '__main__':
    t = 99999999
    print('*'+QDateTime.currentDateTime().toString("ss:Zzz"))
    print(my_time(t))
    print('*'+QDateTime.currentDateTime().toString("ss:Zzz"))
    print(date_time(t))
    print('*'+QDateTime.currentDateTime().toString("ss:Zzz"))
