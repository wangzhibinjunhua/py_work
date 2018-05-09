import sys
import xlrd
import time
from xlutils.copy import copy
#table=workfile.sheet_by_index(0)
table=None
new_xls=None
list_num=[]
list_money=[]
list_price=[]
def init():
    global  table
    global new_xls
    workfile = xlrd.open_workbook('main2.xls', formatting_info=True)
    new_xls = copy(workfile)
    table = new_xls.get_sheet(0)
    cols_len = len(workfile.sheet_by_index(0).col_values(0))
    print('total len is',cols_len)
    for i in range(cols_len):
        table.write(i + 2, 4, 0)
        table.write(i + 2, 5, 0)


    global list_num
    global list_money
    global list_price
    for i in range(cols_len-2):
        list_num.append(0)
        list_money.append(0)
        list_price.append(0)

    print('list num len is ',len(list_num))
    pass

def end():
    global new_xls
    new_xls.save('main3.xls')
    pass
def write_total(index,total_num,total_money):
    workfile=xlrd.open_workbook('main2.xls',formatting_info=True)

    #table.write(0,0,'test')
    #table.write(106, 4, 4000.0)
    #print(index,total_num,total_money,type(index),type(total_num))

    table.write(index+2, 4, total_num)
    table.write(index + 2, 5, total_money)
    print('########')
    print(index, total_num, total_money, type(index), type(total_num))
    #new_xls.save('main3.xls')
    pass
def gather_data(customer,model,pack,num,money,price):

    workfile = xlrd.open_workbook('main2.xls')
    r_table = workfile.sheet_by_index(0)
    global  table
    cols_len = len(r_table.col_values(0))
    list_customer = r_table.col_values(1)[2:cols_len]
    list_model = r_table.col_values(2)[2:cols_len]
    list_pack = r_table.col_values(3)[2:cols_len]
    #list_num = table.col_values(4)[2:cols_len]
   # list_money = table.col_values(5)[2:cols_len]
    #list_price = table.col_values(6)[2:cols_len]
    global list_price
    global list_num
    global list_money
    cur_customer = ''
    for i in range(len(list_customer)):
        if list_customer[i] == '合计':
            break;
        if list_customer[i].strip() != '':
            cur_customer=list_customer[i]
       # print('i is ',i)
        cur_model=list_model[i]
        cur_pack=list_pack[i]
        #cur_num=list_num[i]
        #cur_money=list_money[i]
        #cur_price=list_price[i]
        if cur_customer== customer and cur_model==model and cur_pack==pack :
            print(cur_customer,cur_model,cur_pack)
            print('num type=', type(list_num[i]))
            print('money type=', type(list_money[i]))
            print('cur_num is',list_num[i])
            list_num[i] +=num
            list_money[i] +=money

            print('cur_num=%f' % list_num[i], 'cur_money=%f' %list_money[i])
            write_total(i,list_num[i],list_money[i])
            break;

    pass
def read_sheet(name):

    cur_customer=''
    workfile = xlrd.open_workbook('main2.xls')
    table = workfile.sheet_by_name(name)
    nrows = table.nrows
    print(nrows)
    ncols = table.ncols
    print(ncols)
    print(table.cell(1,0).value)
    if table.cell(1,0).value != '客户名称':
        print('err!')
    cols_len=len(table.col_values(0))
    list_customer=table.col_values(0)[2:cols_len]
    list_model = table.col_values(1)[2:cols_len]
    list_pack = table.col_values(2)[2:cols_len]
    list_num = table.col_values(3)[2:cols_len]
    list_money = table.col_values(4)[2:cols_len]
    list_add_num = table.col_values(5)[2:cols_len]
    list_price = table.col_values(6)[2:cols_len]
    print(list_customer)
    for i in range(len(list_customer)):
        if list_customer[i] == '合计':
            break;
        if list_customer[i].strip() != '':
            cur_customer=list_customer[i]
        cur_model=list_model[i]
        cur_pack=list_pack[i]
        cur_num=list_num[i]
        cur_money=list_money[i]
        cur_add_num=list_add_num[i]
        cur_price=list_price[i]
        print(cur_customer)
        print(cur_model)
        print(cur_pack)
        print(cur_num)
        print(cur_money)
        print(cur_add_num)
        print(cur_price)
        gather_data(cur_customer,cur_model,cur_pack,cur_num,cur_money,cur_price)
        #time.sleep(1)

    pass


init()
workfile = xlrd.open_workbook('main2.xls')
list_table=workfile.sheet_names()
for sheet in list_table[1:len(list_table)-2]:
    print(sheet)
    read_sheet(sheet)

end()




#import pandas as pd
#data=pd.read_excel('main2.xls',skiprows=1)
#print(data[data.客户名称=='宝佳明'].订货数量)





