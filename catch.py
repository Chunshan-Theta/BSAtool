#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)                         # 2
sys.setdefaultencoding('utf-8')     # 3



# 引入 MySQLdb 模組，提供連接 MySQL 的功能
import MySQLdb

# 連接 MySQL 資料庫
db = MySQLdb.connect(host="xxx.xxxx.xxxx.xxxx",user="root", passwd="root_password", db="db_liat_name",charset='utf8')
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

def ReplaceContent(data,before,after):
    reData = []
    for record in data:
        row = []
        for col in record:
            if before in str(col):         
                row.append(col.replace(before, after))
            else:
                row.append(str(col).replace("\n", ""))
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


def DeleteRow(data,RowNum,Target):
    reData = []
    for record in data:
        if record[RowNum] != Target:
            row = []
            for col in record:
                    row.append(str(col).replace("\n", ""))
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
                row.append(str(record[col_idx]).replace("\n", ""))
        reData.append(row)
    return reData

def DBfilter_sorting(data,sorting):
    reData=[]
    for record in data:
        row = []
        for col_idx in sorting:
            row.append(str(record[col_idx]).replace("\n", ""))
        reData.append(row)
    return reData


############################

search_web = exeSQl("SELECT * FROM search_web")
note = exeSQl("SELECT * FROM note")
search = exeSQl("SELECT * FROM search")
chat_record = exeSQl("SELECT * FROM chat_record") #the list didn't have `stu_id` column

'''
ShowDBList(chat_record)
chat_record = ReplaceContent(chat_record,'辯論者','s10')
ShowDBList(chat_record)

ShowDBList(note)
note = DeleteRow(note,5,'')
ShowDBList(note)

ShowDBList(note)
note = DeleteRow(note,2,'')
ShowDBList(note)


note = DBfilter_keep_column(note,[0,1,3,4])
ShowDBList(note)


note = DBfilter_sorting(note,[3,2,1,0])
ShowDBList(note)
'''
#ShowDBList(note)                                #show data of SQL list
note = DeleteRow(note,5,'')                     #delete rows that don't have quit time
note = DeleteRow(note,2,'')                     #delete rows that don't have content of note
note = DBfilter_keep_column(note,[2,3,5])       #keep some column and drop other columns
note = DBfilter_sorting(note,[1,0,2])           #Reset sort of list
note = Addcolumn(['筆記'],note)                 #Add new column to list
#ShowDBList(note)


ShowDBList(search_web)                          #show data of SQL list
'''
note = DeleteRow(note,5,'')                     #delete rows that don't have quit time
note = DeleteRow(note,2,'')                     #delete rows that don't have content of note
note = DBfilter_keep_column(note,[2,3,5])       #keep some column and drop other columns
note = DBfilter_sorting(note,[1,0,2])           #Reset sort of list
note = Addcolumn(['筆記'],note)                 #Add new column to list
ShowDBList(note)
'''

#arr = [['type','stu_id','content','time']]


# 關閉連線
db.close()
