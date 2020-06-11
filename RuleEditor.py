#!/usr/bin/env python3
#coding:utf-8
# 2019/5/14
__author__ = 'xmxoxo<xmxoxo@qq.com>'

'''
文本匹配工具  规则编辑器
版本： v0.1.10
'''

import argparse
import time
from RuleLib import *

from flask import Flask,request,render_template,jsonify
from flask_restful import Resource, Api

current_rule_fileName = ''

#HTTP server
def flask_server(args):
    global current_rule_fileName
    app = Flask(__name__)
    version = 'V 0.1.10'
    current_rule_fileName = args.rule_file
    test_file = args.test_file

    @app.route('/')
    def index():
        test_text = RuleFinder.readtxtfile(test_file)
        return render_template('index.html', version=version, test_text=test_text )
  
    # 匹配
    @app.route('/api/v0.1/query', methods=['POST'])
    def query ():
        res = {}
        txt = request.values['text']
        if not txt :
            res["result"]="error"
            return jsonify(res)
        if request.method == 'POST':
            myfinder = RuleFinder(configfile=current_rule_fileName, debug=1)
            lstseg = myfinder.findKey(txt)
            res['result'] = lstseg
        print('\nresult:%s' % str(res))
        return jsonify(res)

    # 更新单条规则
    @app.route('/api/v0.1/rule_single', methods=['POST'])
    def rule_single ():
        if request.method == 'POST':
            res = {}
            r_id = request.values['id']
            r_class = request.values['class']
            r_rule = request.values['rule']
            print(r_id , r_class , r_rule)

            if r_id and r_class and r_rule:
                r_rule = r_rule.replace('\n','')
                # 更新单条
                myfinder = RuleFinder(configfile=current_rule_fileName, debug=1)
                all_rule = myfinder.getSubjectRule()
                #print(len(all_rule))
                r_id = int(r_id)
                if r_id<0:
                    all_rule.insert(0,[r_class,r_rule])
                    print('new:', [r_class,r_rule])
                    r_id = 0
                else:
                    print(all_rule[r_id])
                    all_rule[r_id] = [r_class,r_rule]
                
                #print(all_rule[r_id])
                #print(len(all_rule))
                lstSubject, lstRule = myfinder.splitRule(all_rule)
                if lstRule:
                    myfinder.setSubject (lstSubject)
                    myfinder.setRule (lstRule)
                    myfinder.saveRule()
                    res["result"] = "OK"
                else:
                    res["result"] = "Error"
            return jsonify(res)
            pass

    @app.route('/api/v0.1/rule', methods=['GET','POST'])
    def rule():
        res = {}
        res["result"] = "Error"
        print('current_rule_fileName:' , current_rule_fileName)
        myfinder = RuleFinder(configfile=current_rule_fileName)
        # 读取规则
        if request.method == 'GET':
            res['rule_file'] = current_rule_fileName
            res['rule'] = myfinder.getSubjectRule()
            res["result"] = "OK"
            return jsonify(res)

        # 更新所有规则
        if request.method == 'POST':
            print('正在更新全部规则...')
            txt = request.values['rule']
            if txt:
                lstSubject, lstRule = myfinder.splitRule(txt)
                if lstRule:
                    myfinder.setSubject (lstSubject)
                    myfinder.setRule (lstRule)
                    myfinder.saveRule()
                    res["result"] = "OK"
            return jsonify(res)

    # 规则文件 current_rule_fileName
    @app.route('/api/v0.1/ruleFile', methods=['GET','POST'])
    def ruleFile():
        global current_rule_fileName
        res = {}
        if request.method == 'GET':
            res['rule_file'] = current_rule_fileName
            res["result"] = "OK"
            return jsonify(res)
        if request.method == 'POST':
            nfile = request.values['rule_file']
            if nfile:
                current_rule_fileName = nfile
                res['rule_file'] = current_rule_fileName
                res["result"] = "OK"
            else:
                res["result"] = "Error"
            print('current_rule_fileName:' , current_rule_fileName)
            return jsonify(res)

    app.run(
        host = args.ip,     #'0.0.0.0',
        port = args.port,   #8910,  
        debug = True 
    )

# command line
def main_cli ():
    pass
    parser = argparse.ArgumentParser(description='RuleEditor server')
    parser.add_argument('-ip', type=str, default="0.0.0.0", help='IP address')
    parser.add_argument('-port', type=int, default=8910, help='listen port,default:8910')
    parser.add_argument('-rule_file', type=str, default='./rules/rule.txt', help='rules file name')
    parser.add_argument('-test_file', type=str, default='./test/test.txt', help='test dat file name')
    args = parser.parse_args()

    flask_server(args)


if __name__ == '__main__':
    main_cli()
