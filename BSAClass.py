#coding:utf-8
#Csv file of Source Data convert to Behavior Sequential class
'''
using;

FirstBSA = BSA('DataFormWuret.csv',6)
print FirstBSA.SelectedArray

FirstBSA.ComputeMotionGroup('21')
print FirstBSA.SelectedArray
'''


import csv
import numpy

class BSA:
    def __init__(self,CsvDir,TypeNum):
        self.listmotion = self.ReadFile(CsvDir)
        self.SelectedArray = [[]]        
        self.TypeNum = TypeNum
        self.ComputeMotionALL()
        ####


    def ComputeMotionGroup(self,wantSet):
        FirstMotion = -1
        SecondMotion = -1
        TypeNum = self.TypeNum    
        listmotion = self.listmotion
        TypeNum +=1 # Because Data not contain 0
        MotionSet=numpy.zeros((TypeNum,TypeNum),int)
        ####

        for index in range(TypeNum-1):
            MotionSet[0][index+1]=index+1
            MotionSet[index+1][0]=index+1

        for index in range(len(listmotion)-1):
            if listmotion[index][0] == listmotion[index+1][0] and wantSet == listmotion[index][0]:
                # if not same group, pass
                # if didn't select group, pass
                FirstMotion = listmotion[index][1]
                SecondMotion = listmotion[index+1][1]
                MotionSet[FirstMotion][SecondMotion] += 1
        #print MotionSet
        self.SelectedArray = MotionSet

    def ComputeMotionALL(self):
        FirstMotion = -1
        SecondMotion = -1
        TypeNum = self.TypeNum    
        listmotion = self.listmotion
        TypeNum +=1 # Because Data not contain 0
        MotionSet=numpy.zeros((TypeNum,TypeNum),int)
        ####

        for index in range(TypeNum-1):
            MotionSet[0][index+1]=index+1
            MotionSet[index+1][0]=index+1

        for index in range(len(listmotion)-1):
                FirstMotion = listmotion[index][1]
                SecondMotion = listmotion[index+1][1]
                MotionSet[FirstMotion][SecondMotion] += 1
        self.SelectedArray = MotionSet

    def ReadFile(self,FileDir):
        listmotion = []
        Tfile = open(FileDir, 'r')
        csvCursor = csv.reader(Tfile)
        ####

        for row in csvCursor:
            try:
                if row[2] != '':
                    listmotion.append([str(row[0]),int(row[2])])# Group , type
            except:
                print "warring: Input data:\'"+str(row[2])+'\' not Int'
        Tfile.close()
        return listmotion



FirstBSA = BSA('DataFormWuret.csv',6)
print FirstBSA.SelectedArray

FirstBSA.ComputeMotionGroup('21')
print FirstBSA.SelectedArray



