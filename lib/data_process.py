#encoding = utf-8
import json
from log import *
'''
a = {"a1":"1","b":[]}
below process a
'''
def data_filter(datas,filters,infos):
    try:
        if isinstance(datas,list):
            return lis_filter(datas,filters,infos)
        if isinstance(datas,dict):
            return dic_filter(datas,filters,infos)
    except Exception,e:
        print str(e)
        setLog("Error in data_filter: %s"%str(e),level="error")
def dic_filter(datas,filters,infos):
    try:
        result = {} 
        for data in datas:
            if data in filters:
                result.update({data:datas.get(data)})
            elif data in infos:
                if isinstance(datas.get(data),list):
                    item = lis_filter(datas.get(data),filters,infos)
                    result.update({data:item})
                elif isinstance(datas.get(data),dict):
                    item = dic_filter(datas.get(data),filters,infos)
                    result.update({data:item})
        return result

    except Exception,e:
        print str(e)
        setLog("Error in dic_filter: %s"%str(e),level="error")

'''
list_filter:
a = [{"a1":12,"a2":1},[1,2,3]]
'''
def lis_filter(datas,filters,infos):
    try:
        result = []
        for item in datas:
            if isinstance(item,list):
                new_item = lis_filter(item,filters,infos)
                result.append(new_item)
            if isinstance(item,dict):
                new_item = dic_filter(item,filters,infos)
                result.append(new_item)
        return result
    except Exception,e:
        print str(e)
        setLog("Error in lis_filter: %s"%str(e),level="error")

'''            
gain keywords of exp_data to set in filters and infos
'''
def get_expKey(exp_data):
    filters = []
    infos = []
    try:
        if isinstance(exp_data,list):
            for item in exp_data:
                result = get_expKey(item)
                filters.extend(result["filters"])
                infos.extend(result["infos"])
        if isinstance(exp_data,dict):
            for item in exp_data:
                if isinstance(exp_data[item],dict):
                    infos.append(item)
                    result = get_expKey(exp_data[item])
                    filters.extend(result["filters"])
                    infos.extend(result["infos"])
                elif isinstance(exp_data[item],list):
                    data = exp_data[item]
                    for i in data:
                        if isinstance(i,dict):
                            infos.append(item)
                            result = get_expKey(i)
                            filters.extend(result["filters"])
                            infos.extend(result["infos"])
                        if isinstance(i,list):
                            result = get_expKey(i)
                            filters.extend(result["filters"])
                            infos.extend(result["infos"])
                        else:
                            filters.append(item)       
                else:
                    filters.append(item)
        return {"filters":filters,"infos":infos} 
    except Exception,e:
        print str(e)
        setLog("Error in get_expKey: %s"%str(e))
            

if __name__ == "__main__":
##below data is check filter def
    filters = ["a","c","a4"]
    infos = ["a2"]
    datas = {
        "a":"1",
        "a2":{
            "a":"er",
            "c":"12"
            },
        "a3":[{"a":2,"b":"123"}],
        "a4":[1,2]
        }   
#    datas = json.dumps(datas)
#    datas = json.loads(datas)      
    result = dic_filter(datas,filters,infos)
    print result
##below data to check get_expKey
    exp1 = [{"a":1,"b":{"c":1,"d":2}},{"a":2,"b":{"c":"","d":2,"e":32}}]
    exp2 = {"a":1,"b":["1",{"d":1},{"c":{"a1":12}}]}
    rs = get_expKey(exp1)
    rs1 = get_expKey(exp2)
#    print "1111111111",exp1,rs
    print "2222222222",exp2,rs1

##below to transfer expKey to filter def

    result1 = lis_filter(exp1,rs["filters"],rs["infos"])
    print result1
    assert result1 == exp1
  
    result2 = dic_filter(exp2,rs1["filters"],rs1["infos"])
    print result2
    print exp2
    assert result2 == exp2
