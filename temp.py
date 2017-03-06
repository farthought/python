#!/usr/bin/python
# -*- coding:UTF-8 -*-

import time
import calendar

ticks = time.time()
print "Number of ticks since 12:00am, January 1, 1970:", ticks

localtime = time.localtime(time.time())
print "Local current time :", localtime

localtime2 = time.asctime(time.localtime(time.time()))
print "Local current time: ", localtime2

cal = calendar.month(2008, 1)
print "Here is the canlendar of January, 2008:"
print cal

for num in range(10, 20):
    for i in range(2, num):
        if num % i == 0:
            j = num / i
            print "%d = %d x %d" % (num, i, j)
            break;

    else:
        print "%d 是一个质数" % num

i = 2;

while(i<=100):
    j = 2
    while(j <= i/j):
        if not (i%j):break;
        j = j + 1
    if(j > i/j):
        print i, "是一个素数"
    i = i + 1

total = 0; # 这是一个全局变量
# 可写函数说明
def sum( arg1, arg2 ):
       #返回2个参数的和."
       total =  arg1 + arg2; # total在这里是局部变量.
       print "函数内是局部变量 : ", total
       return total;
             
#调用sum函数
sum( 10, 20 );
print "函数外是全局变量 : ", total 
