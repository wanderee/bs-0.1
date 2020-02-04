import datetime
import os

if __name__ == '__main__':
    cmd = 'rqalpha run -f {} -s {} -e {} --account stock {} --benchmark 000300.XSHG --plot'
    cmd = cmd.format('1','2','3','4')
    print(cmd)