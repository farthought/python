#!/usr/bin/python 
#-*- coding:utf-8 -*-

import ConfigParser

conf = ConfigParser.ConfigParser()
conf.read("./user.conf")

# 获取指定的section， 指定的option的值
name = conf.get("user", "1")
print name
password = conf.get("password", "1")
print password

#获取所有的section
sections = conf.sections()
print sections

#写配置文件
# 更新指定section, option的值
i = 3
conf.set("user", str(i), "test")

# 写入指定section, 增加新option的值
conf.set("password", "2", "56789")

# 添加新的 section
#conf.add_section("face")
conf.set("face", "1", "/usr/share/icons/face.png")

# 写回配置文件
conf.write(open("./user.conf","w"))

