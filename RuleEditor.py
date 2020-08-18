#!/usr/bin/env python3
#coding:utf-8
# 2019/5/14
__author__ = 'xmxoxo<xmxoxo@qq.com>'

'''
文本匹配工具  规则编辑器
版本： v0.1.13
'''

import argparse
import time
from RuleLib import *

from flask import Flask,request,render_template,jsonify,session
from flask_restful import Resource, Api


#HTTP server
def flask_server(args):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)

    version = 'V 0.1.13'
    current_rule_fileName = args.rule_file
    dat_file = args.dat_file

    @app.route('/')
    def index():
        dat_file = session.get('dat_file', None)
        if not dat_file:
            dat_file = args.dat_file
            session['dat_file'] = dat_file

        current_rule_fileName = session.get('rule_file', None)
        if not current_rule_fileName:
            current_rule_fileName = args.rule_file
            session['rule_file'] = current_rule_fileName

        test_text = RuleFinder.readtxtfile(dat_file)
        return render_template('index.html', version=version, dat_file=dat_file, test_text=test_text )
  
    # 查询匹配结果
    @app.route('/api/v0.1/query', methods=['POST'])
    def query ():
        res = {}
        txt = request.values['text']
        current_rule_fileName = session.get('rule_file', args.rule_file)
        if not txt :
            res["result"]="error"
            return jsonify(res)
        if request.method == 'POST':
            print('current_rule_fileName:', current_rule_fileName)
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

    # 规则操作，CRUD
    @app.route('/api/v0.1/rule', methods=['GET','POST'])
    def rule():
        res = {}
        res["result"] = "Error"
        current_rule_fileName = session.get('rule_file', args.rule_file)
        print('/api/v0.1/rule current_rule_fileName:' , current_rule_fileName)
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

    # 加载数据文件 
    @app.route('/api/v0.1/datfile', methods=['GET','POST'])
    def datfile():
        res = {}
        res["result"] = "Error"
        # 2020/8/18 POST方法 表示保存数据
        if request.method == 'POST':
            pass
            nfile = request.values['dat_file']
            txt = request.values['text']
            # 保存数据文件
            ret = RuleFinder.savetofile(txt, nfile)
            if ret:
                session['dat_file'] = nfile
                res["dat_file"] = nfile
                res["result"] = "OK"
            else: 
                res["result"] = "Error"
            
        # GET方法表示加载数据
        if request.method == 'GET':
            nfile = request.values['dat_file']
            test_text = RuleFinder.readtxtfile(nfile)
            if test_text:
                # 保存数据文件名：如果需要所有用户同步变化则使用args.dat_file修改
                # args.dat_file = nfile
                session['dat_file'] = nfile

                res["dat_file"] = nfile
                res["dat"] = test_text
                res["result"] = "OK"
        
        return jsonify(res)

    # 规则文件 
    @app.route('/api/v0.1/ruleFile', methods=['GET','POST'])
    def ruleFile():
        #global current_rule_fileName
        current_rule_fileName = session.get('rule_file', args.rule_file)
        res = {}
        if request.method == 'GET':
            res['rule_file'] = current_rule_fileName
            res["result"] = "OK"
            return jsonify(res)
        
        if request.method == 'POST':
            nfile = request.values['rule_file']
            if nfile:
                current_rule_fileName = nfile
                session['rule_file'] = current_rule_fileName
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
    parser.add_argument('-dat_file', type=str, default='./test/test.txt', help='test dat file name')
    args = parser.parse_args()

    flask_server(args)


if __name__ == '__main__':
    main_cli()
