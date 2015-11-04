#encoding=utf-8

import xml.etree.cElementTree as ET
from pyh import *


def xml_json(file):
    tree = ET.ElementTree(file=file)
    root = tree.getroot()
    print '---root',root
    report = {}
    try:
        report.update({'summary':root.attrib})
        suit = []
        for element in root:
            print element
            case = {}
            attr = element.attrib
            class_name = attr['classname']
            project_name = class_name.split('.')[0]
            suit_name = class_name.split('.')[1]
            print project_name
            print suit_name
            case.update({'project_name':project_name,'suit_name':suit_name})
            case.update({'case_name':attr['name'],'time':attr['time']})
            if element.getchildren():
                child = element.getchildren()
                result = child[0].tag
                print result
                if result == 'system-out':
                    result = 'pass'
                    message = 'Result is equal!'
                elif result == 'failure':
                    #print '----',child[0].attrib
                    info = child[0].attrib['message']
                    message = info.split('!=')[0]
                    print '-----------erro info',message
                else:
                    message = child[0].attrib
            else:
                result = 'pass'
                message = 'Result is equal!'
            
            case.update({'result':result,'detail':message})
            suit.append(case)
        report.update({'detail':suit})
        return report
                     
    except Exception,e:
        print str(e)

def json_html(data,repName):
    def genTable(pro,data):
        t = table(caption = '%s' % pro,border = "1", cl = 'table1',cellpadding = '0', cellspacing = '0')
        
        if pro == "summary":
            t<<tr(td('概况：' ,bgColor='#4169E1'))
            t<<tr(td('执行总数')+td('成功数')+td('失败数')+td('错误数'),bgColor='#48D1CC')
            succ_num = int(data['tests'])-int(data['failures'])-int(data['errors'])
            t<<tr(td('%d'%int(data['tests']),style='color:#4169E1')+td('%d'%int(succ_num),style='color:#32CD32')+td('%d'%int(data['failures']),style='color:#ff0000')+td('%d'%int(data['errors']),style='color:#FFC125'))

        if pro == "detail":
            t<<tr(td('执行详情：' ,bgColor='#4169E1'))
            t<<tr(td('测试项目')+td('测试套件')+td('测试用例')+td('耗时')+td('测试结果')+td('详情'),bgColor='#48D1CC')
            
            for project in data:
                if project['result'] == 'pass':
                    t<<tr(td('%s'%project['project_name'])+td('%s'%project['suit_name'])+td('%s'%project['case_name'])+td('%s'%project['time'])+td('%s'%project['result'])+td('%s'%project['detail']),bgColor='#00EE00')
                else:
                    t<<tr(td('%s'%project['project_name'])+td('%s'%project['suit_name'])+td('%s'%project['case_name'])+td('%s'%project['time'])+td('%s'%project['result'])+td('%s'%project['detail']),bgColor='#FF4040')        

                
        return t
    def toHtml(tables,repName):
        charset = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />\n'
        page = PyH('测试报告')
        page<<charset
        page.addCSS('common.css')
        page<<h1('测试报告',align='center')
        tab = table(cellpadding='10', cellspacing='10',cl='table0',align="center")
        for t in range(0,len(tables),2):
            tab<<tr(td(tables[t-1],cl="table0_td"))
            
            tab<<tr(td(tables[t],cl="table0_td"))
        page<<tab
        page.printOut(file='%s_report.html'%repName)

    tabrows=[]
    
    for k,v in data.items():
        t=genTable(k,v)
        tabrows.append(t)
        toHtml(tabrows,repName)
    

if __name__ == '__main__':
    file = 'report.xml'
    repName = file.split('.')[0]
    rs = xml_json(file)
    print '----rs',rs
    json_html(rs,repName)
    
  
