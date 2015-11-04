#exp should be included in act
#mean act is greater than exp
#so the order must not be changed

import json
from data_process import *

def result_cmp(result,code,message,data,filter=False):
    try:
        exp_code =code
        exp_message = message
        exp_data = data
        for item in result:
            if item == "message":
                act_message = result.get(item)
                if act_message != exp_message:
                    fail_message = {"result":"message not equal","exp_message":exp_message,"act_message": act_message}
                    setLog("Fail: %s"%fail_message)
                    return fail_message
            if item == "act_code":
                act_code = result.get(item)
                if result.get(item) != exp_code:
                    fail_message = {"result":"code not equal","exp_code":exp_code,"act_code": act_code}
                    setLog("Fail: %s"%fail_message)
                    return fali_message
            if item == "act_data":
                act_data = result.get(item)
                if filter == True:
                   result = get_expKey(exp_data)
                   act_data = data_filter(act_data,result["filters"],result["infos"])
                if cmp(act_data,exp_data) != 0:
                 
                    fail_message = {"result":"data not equal","exp_data":exp_data,"act_data": act_data}
                    setLog("Fail: %s"%fail_message)
                    return fail_message
        
        return True
        
    except Exception,e:
        print "--- erro info:",str(e)
        return setLog("Result_cmp erro: %s"%str(e),level="error")
    
