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