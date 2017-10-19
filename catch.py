#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)                         # 2
sys.setdefaultencoding('utf-8')     # 3



# 引入 MySQLdb 模組，提供連接 MySQL 的功能
import MySQLdb

# 連接 MySQL 資料庫
#db = MySQLdb.connect(host="xxx.xxxx.xxxx.xxxx",user="root", passwd="root_password", db="db_liat_name",charset='utf8')
db = MySQLdb.connect(host="140.118.37.196",user="root", passwd="ytwu57874", db="ets_search",charset='utf8')
cursor = db.cursor()



def exeSQl(sql):
    # 執行 MySQL 查詢指令
    cursor.execute(sql)

    # 取回所有查詢結果
    results = cursor.fetchall()
    '''
    # 輸出結果
    for record in results:
        row = ""
        for col in record:
            row += str(col).replace("\n", "")
            row += ","        
        print row
    '''
    return results

def ReplaceContent(data,ColumnNum,before,after):
    reData = []
    for record in data:
        row = []
        for col in record:
            if before in str(col) and col == record[ColumnNum]:         
                row.append(col.replace(before, after))
            else:
                row.append(str(col))
        reData.append(row)
    return reData



def ShowDBList(data):
    for record in data:
        row = ""
        for col in record:
            row += str(col).replace("\n", "")
            row += " | "        
        print row
        print '-'*10


def DeleteRow(data,ColumnNum,Target):
    reData = []
    for record in data:
        if record[ColumnNum] != Target:
            row = []
            for col in record:
                    row.append(str(col))
            reData.append(row)
        else:
            pass
    return reData

def Addcolumn(array1,array2):
    #Input: array1 -> One-dimensional array , array2 -> two-dimensional array
    reData = []    
    
    for con2 in array2:
        row = []
        for con1 in array1:
            row.append(con1)
        for con2_sub in con2:
            row.append(con2_sub)
        reData.append(row)

    return reData

def DBfilter_keep_column(data,keepColumn):
    reData=[]
    for record in data:
        row = []
        for col_idx in range(len(record)):
            if col_idx in keepColumn:
                row.append(str(record[col_idx]))
        reData.append(row)
    return reData

def DBfilter_sorting(data,sorting):
    reData=[]
    for record in data:
        row = []
        for col_idx in sorting:
            row.append(str(record[col_idx]))
        reData.append(row)
    return reData

def DBfilter_Dropbreak(data):
    reData=[]
    for record in data:
        row = []
        for col in record:
            str(col).replace("\n", "")
            str(col).replace("\t", "")
            str(col).replace("\r", "")
            row.append(col)
        reData.append(row)
    return reData

def Combine_List(arr1,arr2):
    reData=[]
    for record in arr1:
        reData.append(record)
    for record in arr2:
        reData.append(record)
    return reData
############################

search_web = exeSQl("SELECT * FROM search_web")
note = exeSQl("SELECT * FROM note")
search = exeSQl("SELECT * FROM search")
chat_record = exeSQl("SELECT * FROM chat_record") #the list didn't have `stu_id` column


#ShowDBList(note)                                           #show data of SQL list

#ShowDBList(note)
note = DBfilter_Dropbreak(note)                             #Drop break in content
note = ReplaceContent(note,5,'60','59')                     #correct time
note = DeleteRow(note,5,'')                                 #delete rows that don't have quit time
note = DeleteRow(note,2,'')                                 #delete rows that don't have content of note
note = DeleteRow(note,3,'')                                 #delete rows that don't have id of student 
note = DBfilter_keep_column(note,[2,3,5])                   #keep some column and drop other columns

note = DBfilter_sorting(note,[1,0,2])                       #Reset sort of list

note = Addcolumn(['筆記'],note)                             #Add new column to list
#ShowDBList(note)


#ShowDBList(search_web)                                     #show data of SQL list
search_web = DBfilter_Dropbreak(search_web)                 #Drop break in content
search_web = ReplaceContent(search_web,4,'60','59')         #correct time
search_web = DeleteRow(search_web,1,'')                     #delete rows that don't have id of student 
search_web = DeleteRow(search_web,2,'')                     #delete rows that don't have title of web
search_web = DeleteRow(search_web,4,'')                     #delete rows that don't have quit time
search_web = DBfilter_keep_column(search_web,[1,2,4])       #keep some column and drop other columns
search_web = Addcolumn(['瀏覽網頁'],search_web)             #Add new column to list
#ShowDBList(search_web)

#ShowDBList(search)                                         #show data of SQL list
search = DBfilter_Dropbreak(search)                         #Drop break in content
search = ReplaceContent(search,8,'60','59')                 #correct time
search = DeleteRow(search,11,'')                            #delete rows that don't have id of student 
search = DeleteRow(search,7,'')                             #delete rows that don't have title of web
search = DeleteRow(search,8,'')                             #delete rows that don't have quit time
search = DBfilter_keep_column(search,[7,8,11])              #keep some column and drop other columns
search = DBfilter_sorting(search,[2,0,1])                   #Reset sort of list
search = Addcolumn(['搜索關鍵字'],search)                    #Add new column to list
#ShowDBList(search)                                          


#ShowDBList(chat_record)                                    #show data of SQL list
chat_record = DBfilter_Dropbreak(chat_record)               #Drop break in content
chat_record = ReplaceContent(chat_record,4,'60','59')       #correct time
chat_record = ReplaceContent(chat_record,1,'辯論者','s10')  #Correct dirty content of id
chat_record = DeleteRow(chat_record,1,'')                   #delete rows that don't have id of student 
chat_record = DeleteRow(chat_record,2,'')                   #delete rows that don't have content of chat
chat_record = DeleteRow(chat_record,4,'')                   #delete rows that don't have quit time
chat_record = DBfilter_keep_column(chat_record,[1,2,4])     #keep some column and drop other columns
chat_record = Addcolumn(['論證'],chat_record)               #Add new column to list
#ShowDBList(chat_record)                                    #show data of SQL list



correct_list = []
correct_list = Combine_List(correct_list,chat_record)
correct_list = Combine_List(correct_list,search)
correct_list = Combine_List(correct_list,search_web)
correct_list = Combine_List(correct_list,note)

#ShowDBList(MainList)

# 關閉連線
db.close()


#自定的比較函式
import datetime
def compare(var1, var2):
    var1_d = datetime.datetime.strptime(var1[3], '%Y-%m-%d %H:%M:%S')
    var2_d = datetime.datetime.strptime(var2[3], '%Y-%m-%d %H:%M:%S')
    if var1_d > var2_d:
        return 1  # var1 > var2
    else:
        return -1 # var1 < var2

MainList=[]
for i in sorted(correct_list, reverse=True, cmp=compare):
    MainList.append(i)
#ShowDBList(MainList)


import csv
f = open('exportExample.csv', 'a+')
csvCursor = csv.writer(f)

csvCursor.writerow(['type','user','content','time'])
for row in MainList:
    csvCursor.writerow(row)
f.close()









