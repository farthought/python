#!/usr/bin/env python2
#! -*- coding:utf-8 -*-

import re

text = "JGood is a handsome boy, he is cool, clever, and so on..."
m = re.match(r"(\w+)\s", text)
if m:
    print m
    print m.group(0), '\n', m.group(1)
else:
    print 'not match'

n = re.search(r"(\w+)\s", text)
if n:
    print n
    print n.group(0), '\n' , n.group(1)
else:
    print 'not match'

p = re.compile(r'(\W+)')
l = p.split('This is a test, short and sweet, of split().')
s = p.split('This is a test, short and sweet, of split().', 3)

print l, '\n', s
print re.findall(r'\w*oo\w*',text)
print re.findall(r'(\w)*oo(\w)*',text)
print re.findall(r'(\w)oo(\w*)',text)
print re.findall(r'(?:\w)*oo(?:\w)*',text)
