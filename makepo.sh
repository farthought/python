#!/bin/bash
###########################################
#
# 该脚本的主要作用是提取python脚本中需要翻译的
# 的内容，生成po文件，并更新po文件，更行完成之
# 后需要手动翻译文件，这里主要用到了xgettext命令
# xgettext命令参数：
# -d表示domain
# -s 表示排序
# -o 生成文件的名字
# -p 生成新的po文件的位置
# -k_指导xgettext搜寻可翻译字符串（前导下划线_），
# 同事仍然搜索默认的gettext
# 
###########################################

# 获得当前的工作目录

PWD=`pwd`

# 判断调用脚本方法是否正确，调用该脚本时应该传递一个参数，
# 该参数为要翻译的文件
if [ $# != 1 ];then
	echo "Usage:$0 argv1";
	echo "Your take wrong number of arguments,please try again!"; 
	exit 1;
fi

# 将python文件的扩展名.py去掉，只取文件名，例如guess.py只取前面的guess
FILE="$1"
PREFIX=${FILE%.*}

# 判断po文件是否存在，如果存在则更新旧的po文件，如果po文件不存在，则重新
# 生成po文件

if [ -e $PWD/po/${PREFIX}.po ];then
	xgettext -d $PREFIX -k_ -s -o ${PREFIX}-new.po -p $PWD/po/ $FILE
	sed -i '/Content-Type/s/CHARSET/UTF-8/g' $PWD/po/${PREFIX}-new.po
	msgmerge -s -U $PWD/po/$PREFIX.po $PWD/po/${PREFIX}-new.po
	sed -i '/Content-Type/s/CHARSET/UTF-8/g' $PWD/po/$PREFIX.po
	rm $PWD/po/${PREFIX}-new.po
else
	xgettext -k_ -o $PWD/po/$PREFIX.po $FILE
	sed -i '/Content-Type/s/CHARSET/UTF-8/g' $PWD/po/$PREFIX.po 
fi 

# 删除生成的中间文件
if [ -e $PWD/po/${PREFIX}.po~ ];then
	rm $PWD/po/${PREFIX}.po~
fi
