#!/usr/bin/env python
# -*- coding:utf-8 -*-
import list  
  
def main():  
    print ("start main()")  
    mylist = list.List()  
    for i in range(0,10):  
        mylist.Insert(i)  
    print ('输出该单链表：\n')  
    mylist.Print()  
    print ("\nmylist的size：", mylist.GetSize())  
    print ("\n删除1号索引的元素：")  
    mylist.Remove(1)  
    print ("输出删除1号索引后链表的元素：\n")  
    mylist.Print()  
    print ("\n删除后的元素个数：%s" % mylist.GetSize())  
  
main()  
