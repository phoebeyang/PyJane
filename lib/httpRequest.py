#encoding=utf-8
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"../lib"))
from result_cmp import *
import requests
import json
from nose.tools import assert_equals
from log import *

def HttpRequest(url,uri='',params='',d=None,headers=None,method='GET'):
    try:
        _func = {
            "GET" : requests.get,
            "POST" : requests.post,
            "PUT" : requests.put,
            "DELETE" : requests.delete
            }
        url = url + uri
        #print 'url----',url
        #print 'data---',d
        if d != None:
            d = json.dumps(d)
        #print 'headers---',headers
        #print 'params---',params
    #    try:
        rs = _func[method](url,params = params,data=d,headers=headers)
        s = rs.status_code
        #print rs.url
        #print "--------",s,rs.content
        #print type(rs.content)
        j = json.loads(rs.content)
        setLog("HttpRequest succ: %s"%rs.content,level = "debug")
        return {'resp_code':s,'content':j}
       
    except Exception,e:
       setLog("HttpRequest error:%s,detail:%s"%(str(e),rs.content),level="error")

def gainResult(resp_result,status="status",result="result",message="message"):
    try:
        status = status
        result= result
        message = message
        #print type(resp_result)
        s = resp_result['resp_code']
        j = resp_result['content']
        if status in j :
            erno = int(j[status])
            act_code = (s,erno)
            if result in j:
                act_data = j[result]
                return {'act_code':act_code,'act_data':act_data,'message':j[message]}
            else:
                return {'act_code':act_code,'message':j[message]}
    except Exception,e:
        print '-----Except erro:',str(e)
        setLog("GainResult error: %s"%str(e),level="error")
    

def Read_file(file,url,method='POST'):
    try:
        with open(file) as fd:
             content = json.load(fd)
             print content
             if 'uri' in content.keys():
                 uri = content['uri']
             else:
                 uri = ''
             if 'params' in content.keys():
                 params = content['params']
             else:
                params = None
             if 'data' in content.keys():
                 d = content['data']
             else:
                 d = None    
             if 'headers' in content.keys():
                 headers = content['headers']
             else:
                 headers = None
        return HttpRequest(url,uri,params=params,d=d,headers=headers,method=method)
    except e:
        logging.error(str(e))

def params(**args):
    return args

if __name__ == "__main__":
    params = {
        "COOKIE_SESSION_ID" : "116805502712BC721B7B9A6A11EFE21A",
        "COOKIE_TOKEN_ID" : "1443175408155",
        "COOKIE_TOKEN_DATE" : "1443175408155",
        "COOKIE_USER_ID" : "273873795",
        "type" : 0
        }
    exp_code = (200,1)
    url = "http://address.go.lemall.com"
    uri = "/api/web/query/userAddress.json"
    rs = HttpRequest(url,uri=uri,params=params)
    print rs
    result = gainResult(rs)
    print result
    exp_message = u"服务调用成功"
    exp_data = [
         {
            "ADDRESS_DETAIL":"朝阳区",
            "ADDRESS_ID":"8768184",
	    "ADDRESS_NAME":"fwq",
	    "CITY_ID":"83",
            "CITY_NAME":"东城区",
	    "CREATE_AT":"2015-09-21 18:45:52.0",
	    "DISTRICT_ID":"524",
	    "DISTRICT_NAME":"内环到三环里",
	    "E_MAIL":"xhe@163.com",
	    "INVOICE_CATEGORY_ID":"1",
	    "INVOICE_CATEGORY_NAME":None,
	    "INVOICE_CONTENT":"个人",
	    "INVOICE_TYPE_ID":"2",
	    "INVOICE_TYPE_NAME":None,
	    "IS_DEFAULT":"1",
	    "MOBILE":"13676456789",
	    "PAYMENT_METHOD_ID":"",
	    "PAYMENT_METHOD_NAME":None,
	    "PHONE":"",
	    "POSTCODE":"100020",
	    "PROVINCE_ID":"1",
	    "PROVINCE_NAME":"北京",
	    "RECEIVER":"tew",
	    "REMARK":None,
	    "SHIPPING_METHOD_ID":"1",
	    "SHIPPING_METHOD_NAME":None,
	    "SHIPPING_TIME_ID":"0",
	    "SHIPPING_TIME_NAME":None,
	    "STATUS":"1",
	    "TYPE":"0",
	    "UPDATE_AT":"2015-09-22 09:36:39.0",
	    "UPGRADE_BY":None,
	    "USER_ID":"273873795"

            }
        ]
    exp_data = json.dumps(exp_data)
    exp_data = json.loads(exp_data)
    print "exp:",exp_data
    print "act:",result
    test_result = result_cmp(result,exp_code,exp_message,exp_data)
    print "--------------result",test_result
    assert_equals(test_result,True)
#    for item in result:
#        if item == "message":
#            act_message = result.get(item)
#            print act_message,exp_message
#            assert act_message == exp_message
#        if item == "act_code":
#            assert result.get(item) == exp_code
#        if item == "act_data":
#            act_data = result.get(item)
#            print act_data
#            print exp_data
#            assert cmp(act_data,exp_data) == 0
    
  


    
