#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'


'''
文本规则匹配 类库
版本： v0.1.13

'''
import os
import sys
import re
import json
import logging
import traceback
import pandas as pd


# 规则匹配对象包装
class RuleFinder():
    def __init__(self, configfile='./rule.txt' , debug=0 ):
        self.configfile = configfile
        self.debug = debug
        self.dictRule = {}
        #自动加载规则
        self.loadRule()

    #-----------------------------------------
    # 读入文件
    @staticmethod
    def readtxtfile(fname):
        pass
        try:
            with open(fname,'r',encoding='utf-8') as f:  
                data=f.read()
            return data
        except Exception as e:
            return ''

    # 保存文件
    @staticmethod
    def savetofile(txt,filename):
        pass
        try:
            with open(filename,'w',encoding='utf-8') as f:  
                f.write(str(txt))
            return 1
        except :
            return 0

    # get all files and floders in a path
    # fileExt: ['png','jpg','jpeg']
    # return: 
    #    return a list ,include floders and files , like [['./aa'],['./aa/abc.txt']]
    @staticmethod
    def getFiles (workpath, fileExt = []):
        try:
            lstFiles = []
            lstFloders = []

            if os.path.isdir(workpath):
                for dirname in os.listdir(workpath) :
                    file_path = os.path.join(workpath, dirname)
                    #file_path = workpath  + '/' + dirname
                    if os.path.isfile( file_path ):
                        if fileExt:
                            if dirname[dirname.rfind('.')+1:] in fileExt:
                               lstFiles.append (file_path)
                        else:
                            lstFiles.append (file_path)
                    if os.path.isdir( file_path ):
                        lstFloders.append (file_path)      

            elif os.path.isfile(workpath):
                lstFiles.append(workpath)
            else:
                return None
            
            lstRet = [lstFloders,lstFiles]
            return lstRet
        except Exception as e :
            return None

    # 拆分文件路径各部分    
    @staticmethod
    def pathsplit (fullpath):
        pass
        try:
            (filepath,tempfilename) = os.path.split(fullpath)
            (filename,extension) = os.path.splitext(tempfilename)
            return (filepath,filename,extension)
        except Exception as e:
            return ('','','')

    # 规则表达式转换为正则
    @staticmethod
    def GetRegex (txt):
        try:
            reg = txt
            reg = reg.replace('[','(?:')
            reg = reg.replace(']','$)?$')
            reg = reg.replace('<','(?:')
            reg = reg.replace('>',')')

            # reg = reg.replace('??','(?:.)')
            # 2020/4/30 文字字符规则"??"含义限制为中文汉字
            # reg = reg.replace('??','(?:[^，；;。‘’"“”]*?)')
            reg = reg.replace('??',r'(?:[\u4E00-\u9FA5]*?)')

            # 2020/8/18 "##" 表示纯数字，"$$"表示含中文的数字
            reg = reg.replace('##',r'(?:\d*?)')
            reg = reg.replace('$$',r'(?:[\d一二三四五六七八九十〇壹贰叁肆伍陆柒捌玖零]*?)')
            
            # "++" 表示非空字符
            #reg = reg.replace('++','(?:.+)')
            reg = reg.replace('++',r'(?:[^，　； ;。‘’"“”]+?)')

            # "**" 表示任意字符，可为空
            #reg = reg.replace('**','(?:.*?)')
            reg = reg.replace('**','(?:.*?)')

            reg = reg.replace('$)?$',')?')

            #p = re.compile(reg, re.S|re.U)
            return reg
        except Exception as e:
            print('Error in GetRegex("%s")' % txt)
            return None    


    # 规则文本批量生成正则表达式
    def TransRule (self, lstRule):
        try:
            return [[self.GetRegex(x) for x in item] for item in lstRule]
        except Exception as e :
            print('Error at TransRule:',e)
            return None

    # turn result to List
    # 把提取结果转换为列表
    @staticmethod
    def resultTurn (lstDat):
        pass
        if not lstDat:
            return None
        lstRet = []
        for item in lstDat:
            pass
            lstA = item[1]
            for x in lstA:
                lstRet.append( x ) #+[item[0],]
        return lstRet

    # 输出JSON格式化文本
    @staticmethod
    def PrintList (lstDat):
        json_list = json.dumps(lstDat, indent=1, ensure_ascii=False)
        return json_list

    # 把批量结果dict转换成DataFrame,并保存到文件中
    # returnlist: =1返回List, =0 返回DataFrame, =-1不返回
    @staticmethod
    def saveDict (dicDat, filename, returnlist=-1, encoding='utf-8'):
        try:
            if not dicDat:
                return 0
            lstDat = []
            for x in dicDat:
                fn = RuleFinder.pathsplit(x['filename'])[1]
                rt = x['result']
                for item in rt :
                    lstDat.append([fn, item[3], item[0], item[1],item[2]])
            # 文件编号	条件内容	分类名称    分类编号
            df = pd.DataFrame(lstDat, columns=['文件编号', '条件内容', '分类编号', '分类名称', '匹配文本']) 
            if filename:
                df.to_csv(filename, index=0, encoding=encoding ) #, encoding="GB2312", sep = '\t'
            if returnlist<0:
                return None
            if returnlist:
                return lstDat
            else:
                return df
        except Exception as e :
            print("Error at saveDict:")
            print(e)
            return None

    # 把表格形式的规则拆分出来，用于前后端传递规则
    # 返回结果： (lstSubject, lstRule)
    def splitRule (self, txt):
        pass
        try:
            if type(txt) == str :
                txt = txt.replace('\n','')
                #print('rule text: %s' %  (txt))
                lstDat = eval(txt)
            if type(txt) == list :
                lstDat = txt
            if lstDat:
                print(len(lstDat))
                dicA = {}
                #lstR = [ list(x) for x in zip(*lstDat)]
                for x in lstDat:
                    if x[0] in dicA.keys():
                        dicA[x[0]] += [x[1],]
                    else:
                        dicA[x[0]] = [x[1],]
                lstSubject = list(dicA.keys())
                lstRule = list(dicA.values())
                for item in lstRule:
                    for x in item:
                        if not self.GetRegex(x): 
                            return (None,None)
                            break;
                return (lstSubject,lstRule)
        except Exception as e:
            print(e)
            return (None,None)
    #-----------------------------------------

    # 设置规则, 是全体设置
    # 参数：lstR 必须是一个二层的List
    # 返回：无
    def setRule (self, lstR):
        try:
            # 生成正则
            if lstR:
                self.dictRule['Rule'] = lstR
                self.dictRule['Regexp'] = self.TransRule(lstR)
        except :
            pass
    
    # 读取规则，返回整个字典
    def getRule (self): 
        return self.dictRule.get('Rule',[])

    def setSubject (self,lstR):
        try:
            self.dictRule['Subject'] = lstR
        except :
            pass
    
    def getSubject (self):
        return self.dictRule.get('Subject',[])

    # 返回 主题+规则
    def getSubjectRule(self):
        rule = self.getRule() 
        subject = self.getSubject()
        res = []
        for i in range(len(rule)) :
            for x in rule[i]:
                res.append( [subject[i],x])
        return res            


    #把规则保存到文件中
    def saveRule (self): 
        pass
        try:    
            #正则为空则重新生成
            if not self.dictRule['Regexp']:
                lstReg = self.TransRule(self.dictRule['Rule'])
                if not lstReg:
                    print("规则转换错误！")
                    return 0
                self.dictRule['Regexp'] = lstReg
            
            '''
            #把规则持久化 保存到文件中，格式如下
            dictRule = {
                "Subject": self.dictRule['Subject'], # 分类清单
                "Rule": lstRule,  # 规则明细
                "Regexp": lstReg  # 规则对应的正则表达式
            }
            '''
            return self.savetofile (json.dumps(self.dictRule, indent=1, ensure_ascii=False), self.configfile)
        except Exception as e:
            print(e)
            return 0

    # 从规则文件中加载规则
    # 返回一个字典
    def loadRule (self):
        pass
        try:
            #2019/6/5 fix bug: change  to absolute path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            strRule = self.readtxtfile( os.path.abspath( os.path.join (current_dir, self.configfile)))
            dictRule = json.loads(strRule)
            self.dictRule = dictRule
            return 1
        except Exception as e:
            print(e)
            return 0

    # 通用方法，使用正则表达式判断匹配词
    # 返回结果：匹配到的文本列表
    def matchByRegex (self, txt, reg , rep = re.S|re.U):
        pass
        if not (txt and reg):
            return None
        try:
            #print(reg)
            #正则表达式处理
            #reg = GetRegex(reg)
            p = re.compile(reg, re.S|re.U|re.I)
            searchObj = re.findall(p,txt)
            #print('\n文本:%s \n正则表达式:[%s] \n' % (txt,reg) )
            #searchObj = re.match(p,txt)
            if searchObj:
                #返回所有的匹配结果？
                sret = '|=|=|'.join(list(set(searchObj)))
                #只返回第一个结果
                #sret = searchObj[0]
                if self.debug:
                    print('\n文本:%s \n正则表达式:[%s] \n规则匹配结果: %s' % (txt,str(reg), str(searchObj) ) )
                return sret
            else:
                return None
        except Exception as e:
            logging.error('Error in matchByRegex: '+ traceback.format_exc())
            return None        

    '''
    判断是否存在符合规则的匹配句子
    参数：
      txt:        待匹配的文本,单行；
      dictRule:    规则字典，dict
    返回：
        '分类编号', '分类名称','条件内容', '匹配文本'
    '''
    def exitsKey (self,txt):
        pass
        lstR = []
        #lstK = []
        for n in range(len(self.dictRule['Regexp'])):
            x = self.dictRule['Regexp'][n]
            for i in range(len(x)):
                ret = self.matchByRegex(txt,x[i])
                if ret:
                    #print(ret)
                    #2019/5/7 多个结果要拆分开来
                    lstRet = ret.split('|=|=|')
                    for t in lstRet :
                        #2019/5/15 判断是否为空或者重复
                        #if t and not t in lstK:
                        #    lstK.append(t)
                        lstR.append((n, self.dictRule['Subject'][n], t, txt)) #return detail
                    #lstR.append((n, self.dictRule['Subject'][n],ret,txt)) #return detail
                    #return (n,Finder.lstSubject[n],txt,ret)
                    #lstR.append(n)  #lstRule.index(x)
                    if self.debug:
                        #print('n=%d,i=%d' % (n,i))
                        #print('匹配结果', lstR)
                        print("规则表达式:%d, %s" % (i, self.dictRule['Rule'][n][i]) )
                    break #一类规则匹配到一个规则就可以了, 规则越前面优先级越高；
        return lstR

    # 从一个文件中匹配所有关键句
    # match all Rule from file
    # 返回结果： List
    #   匹配规则索引号
    def findKey(self, txt):
        pass
        if not self.dictRule['Rule']:
            return None
        #[2019/6/21] 只按行处理是不行的，这里需要增加文本格式预处理
        txt = txt.replace('。','。\n')
        txt = re.sub('([　\t]+)',r" ",txt)  #去掉特殊字符
        txt = re.sub('([ "?\t]{2,})',r" ",txt)  #多个连续的空格换成一个空格
        txt = re.sub('(\n\s+)',r"\n",txt)  # blank line
        lsttxt = txt.split('\n')
        lstRet = []
        for segment in lsttxt:
            pass
            ret = self.exitsKey(segment)
            if ret:
                #print('-'*30)
                #print("匹配：%s, 句子:%s" % (str(ret), segment) )
                lstRet.append(ret)
        # 提取子句
        lstRet = [x for item in lstRet for x in item]
        # 按匹配的规则序号排序，升序
        lstRet = sorted(lstRet, key=lambda x: x[0])
        return lstRet

    # 单个文件查找关键句
    # 返回结果：List
    # '分类编号', '分类名称', '条件内容','匹配文本'
    def searchSingleFile (self,filename):
        if not self.dictRule['Rule']:
            return None
        txt = self.readtxtfile(filename)
        result = self.findKey(txt)
        #ret = self.resultTurn(result)
        ''' 输出结果用于调试
        '''
        #print(result)
        if self.debug:
            if result:
                #print( '\n' + ('文件名:%s' % filename).center(30,'=') )
                print( ('\n------文件名:%s' % filename) )
                for item in result:
                    print(item)
                    pass
            #print('-'*35)
        return result

    # 按目录批量查找关键句, 
    # 返回结果：匹配结果字典，可使用saveDict保存
    def searchPath (self, path):
        pass
        if not self.dictRule['Rule']:
            return None
        ret = []
        lstFiles = self.getFiles(path)
        for fn in lstFiles[1]:
            print('正在匹配文件：%s' % fn )
            fret = self.searchSingleFile(fn)
            if fret:
                ret.append ({"filename":fn,"result": fret}) 
        return ret




if __name__ == '__main__':
    pass

