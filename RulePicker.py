#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

'''
规则提取器，可加载规则后从批量文件中提取匹配结果；

'''

import argparse
import random
import sys
import string
import time

from RuleLib import *


#根据时间自动生成文件名
def autoFileName (pre = '',ext = ''):
    return '%s%s%s' % (pre, time.strftime('%Y%m%d%H%M%S',time.localtime()) , ext) 


# main function 
def main(args):
    rulefile = args.rule
    if not rulefile:
        sys.exit()

    datapath = args.data
    if not datapath:
        sys.exit()
    
    output = args.output
    if not os.path.exists(output):
        os.mkdir(output)


    #自动生成文件名
    outfile = autoFileName ( os.path.join(output, 'result_'),'.csv')

    print('正在批量处理，请稍候...')

    myfinder = RuleFinder(configfile=rulefile)
    start_t = time.perf_counter()
    ret = myfinder.searchPath(datapath)
    myfinder.saveDict(ret, outfile)
    print('保存结果:%s' % outfile)
    print('匹配用时: %2.2f秒' % (time.perf_counter() - start_t))

    # 输出明细
    print('匹配结果共%d个文件:' % len(ret))
    for x in ret:
        fn = RuleFinder.pathsplit(x['filename'])[1]
        rt = x['result']
        print('=====文件:%s 匹配:%d条=====' % (fn,len(rt)))
        #for item in rt :
        #    print('%s.txt - [%s,%s]【 %s 】' % (fn, item[0], item[1],item[3]) )

def main_cli ():
    parser = argparse.ArgumentParser(description='RulePicker v_0.1.10  by xmxoxo')
    parser.add_argument('-rule', type=str, default="", required=True, help='rule file')
    parser.add_argument('-data', type=str, default="./test/", help='data file path, default: ./test/')
    parser.add_argument('-output', type=str, default="./output/", help='output path, default: ./output/')
    args = parser.parse_args()

    main(args)

if __name__ == '__main__':
    pass
    main_cli()
