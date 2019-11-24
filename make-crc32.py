#/usr/local/python3
# -*- coding:utf-8 -*-
#BiliBili爬虫弹幕模块——弹幕用户生成代码
#作者:小丘
#个人博客:blog.2451cloud.cn
#联系方式:QQ2451437216
#欢迎各位大佬前来指导

#导入模块
from zlib import crc32
import multiprocessing
import sys
import os

def help():
    #帮助
    print('''BiliBili爬虫弹幕模块——弹幕用户生成代码
    本程序是用来生成在B站XML文件里用户经过加密所形成的不可逆加密的彩虹表
    使用的是CRC32加密
    使用方式:
    python make_crc32.py [最大数字] [文件夹] [方法] [线程数]
    [最大数字]:为int整数型
    [方法]:为int整数型,生成的方法有'memory' 'gradually'
        memory:即先把CRC32分类完，在写入文件,对内存需求较大
        gradually:即在写入时分类，对内存需求小
    [线程数]:默认为你电脑的核心数-1(除非你电脑的核心数是1),最好不要等于或超过电脑的核心数，会卡死
    例子:
    python make_crc32.py 1000000000 1_billion gradually 5
    目前，memory的方法还未开发完''')

def agradually(workername,worksections,maxnum,folord):
    #gradually的子进程的运行
    #worksections为子进程的通讯，记载了剩下的没分类玩的开头
    while worksections:
        worksection = worksections.pop()
        print('线程%s,正在分类CRC32开头以"%s"的字符....' % (workername,worksection))
        numlist = ((str(hex(crc32(str(x).encode('ascii'))))[2:],str(x)) for x in range(1,maxnum))
        with open(folord + '/' + worksection + '.txt','w',encoding='utf-8') as f:
            for co_crc32, planxin in numlist:
                if co_crc32[:2] == worksection:
                    f.writelines(co_crc32+'|'+planxin+'\n')
        print('线程%s,以完成开头以%s开头的CRC32！' % (workername,worksection))

def memory():
    pass

if __name__=='__main__':
    try:
        endnum = int(sys.argv[1])+1
        savefile = str(sys.argv[2])
        action = str(sys.argv[3])
    except IndexError:
        print('您没有传入最大数字,文件夹或生成方式！请检查您带入的参数是否正确')
        help()
        input('输入"Enter"键退出！')
        sys.exit()
    except ValueError:
        print('出现错误！你传入的[最大数字]不是一个正确的整数!')
        help()
        input('输入"Enter"键退出！')
        sys.exit()
    if (action != 'memory' and action != 'gradually'):
        print('出现错误！你传入的[方法]不是一个正确的方法!')
        help()
        input('输入"Enter"键退出！')
        sys.exit()
    try:
        theard = int(sys.argv[4])
    except IndexError:
        if multiprocessing.cpu_count()==1:
            theard = 1
        else:
            theard = multiprocessing.cpu_count() - 1
        print('您没有传入线程数，所以线程数将默认设置为%s' % theard)
    except ValueError:
        print('出现错误！你传入的线程数不为整数')
        help()
        input('输入"Enter"键退出！')
        sys.exit()
    
    print('成功通过检测！接下来进行生成!')
    print('生成数量:%s,文件夹名称:%s,传入方法:%s' % (endnum , savefile, action))
    os.mkdir(savefile)
    
    if action == 'gradually':
        q = multiprocessing.Manager().list([x+y for x in 'abcdef123456789' for y in 'abcdef1234567890'])
        p = multiprocessing.Pool(theard+1)
        for i in range(theard):
            p.apply_async(agradually, args=(i,q,endnum,savefile))
        print('正在分类中.....')
        p.close()
        p.join()
        print('全部进程已经装换完毕')
    
    elif action=='memory':
        pass
