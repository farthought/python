#!/usr/bin/python 
#-*- coding:utf-8 -*-

from enum import Enum, unique

@unique #装饰器可以帮助我们检查保证没有重复值
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

for name, member in Month.__members__.items():
    print name, '=>', member, ',', member.value

for name, member in Weekday.__members__.items():
    print name, '=>', member, ',', member.value

day1 = Weekday.Mon
print day1

print day1.value

print Weekday.Tue

print Weekday['Tue']

print Weekday.Tue.value

print day1 == Weekday.Mon

print Weekday(1)

print day1 == Weekday(1)
