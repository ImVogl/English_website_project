import sys

def printLog(*args, **kwargs):
    with open('logs/Logfile.txt', 'a') as file:
        print(*args, **kwargs, file = file)

