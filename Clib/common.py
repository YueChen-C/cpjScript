#coding=utf8
def list_split(num,tied):
    '''平均分组
    :return:[[1, 51], [51, 101], [101, 151], [151, 201]]
    '''
    list=[]
    for i in range(1,num,tied):
        p=[i,i+tied]
        if i+tied>num:
            p=[i,num]
        list.append(p)
    return list


def list_all_dict(dict_a,dict_key=None):
    '''遍历所有键
    :param dict_a:
    :param _key: 需要的key值('msg','name')
    :return:
    '''
    keys=[]
    def list_dict(dict_a):
        if isinstance(dict_a,dict):
            for x in range(len(dict_a)):
                if dict_key:
                    key= dict_a.keys()[x]
                    value = dict_a[key]
                    for i in dict_key:
                        connet={}
                        if key==i:
                            connet[key]=value
                            keys.append(connet)
                    list_dict(value)
                else:
                    key= dict_a.keys()[x]
                    value = dict_a[key]
                    list_dict(value)
                    keys.append(key)
            return keys
    return list_dict(dict_a)
