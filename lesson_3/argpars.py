import argparse

parser = argparse.ArgumentParser(description='новая Программа')
# parser.add_argument('name', help='ваше имя')
# parser.add_argument('-l', '--last_name', help='фамилия') # -l сокращенный аргумент(необязяательный)
# parser.add_argument('--my_flag', action='store_true',help='True or False')
parser.add_argument('a')
parser.add_argument('b')
args = parser.parse_args()
print(args)

def sumarize(a,b):
    print(a+b)
