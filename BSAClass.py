import csv
import numpy
import json


def outcsv(datasource,filename):      
  outputname = str(filename)+'.csv'
  with open(outputname, 'w',encoding='utf-8') as myfile:
    wr = csv.writer(myfile,quoting=csv.QUOTE_ALL)
    #wr.writerow(fieldnames)
    for row in datasource:
      arr = []
      for key,value in row.items():
        arr.append(value)
      
      wr.writerow(arr)


class BSA:
    def __init__(self,CsvSource,TypeNum):
        try:
            self.listmotion = self.ReadFile(CsvSource)
        except:
            self.listmotion = self.ReadCSV(CsvSource.encode("utf-8"))
        self.SelectedArray = [[]]        
        self.TypeNum = TypeNum
        self.ComputeMotionALL()
        self.ZscoreOfSelectedArray=[]
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
            if listmotion[index][0] == listmotion[index+1][0] and str(wantSet) == str(listmotion[index][0]):
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
                print("warring: Input data:\'"+str(row[2])+'\' not Int')
        Tfile.close()
        return listmotion


    def ReadCSV(self,CSV_TEXT):
        listmotion = []
        CSV_TEXT = CSV_TEXT.split('\n')
        csvCursor = csv.reader(CSV_TEXT)
        ####
        for row in csvCursor:
            
            try:
                if row[2] != '':
                    listmotion.append([str(row[0]),int(row[2])])# Group , type
            except:
                print("warring: Input data:\'"+str(row[2])+'\' not Int')

        return listmotion

    def showBSArray(self,Actiontype=0):
        if Actiontype ==1: #print without title
            for i in range(1,self.TypeNum+1):
                PrintStr =''
                for p in range(1,self.TypeNum+1):
                    PrintStr += str(self.SelectedArray[i,p])
                    PrintStr += ','
                print(PrintStr)

        elif Actiontype == 0: #print           
            print(self.SelectedArray)

        elif Actiontype == 2: # return list of count
            PrintStr = ""
            for i in range(1,self.TypeNum+1):
                for p in range(1,self.TypeNum+1):
                    PrintStr += str(i)+" "+str(p)+" "
                    PrintStr += str(self.SelectedArray[i,p])
                    PrintStr += "\n"
            return PrintStr
        else:
            print("Not found the action type")

    def ReNumOfMotionSet(self,Fir,Sec):
        return self.SelectedArray[Fir,Sec]
    def Re_ZscoreArray_Json(self):
        print(self.SelectedArray)    
        x_IJ=self.SelectedArray
        ZscoreArray =numpy.zeros((self.TypeNum+1,self.TypeNum+1),float)
        
        x_PlusPlus=0.0
        for I in range(1,self.TypeNum+1):
            for J in range(1,self.TypeNum+1):
                x_PlusPlus += x_IJ[I,J]

        for I in range(1,self.TypeNum+1):
            for J in range(1,self.TypeNum+1):
                x_IPlus=0.0
                x_PlusJ=0.0
                for idx in range(1,self.TypeNum+1):
                    x_IPlus +=x_IJ[I,idx]
                    x_PlusJ +=x_IJ[idx,J]
                                   
                m_IJ=float(x_IPlus*x_PlusJ)/float(x_PlusPlus)
                #print x_IPlus,x_PlusJ,x_PlusPlus
                p_IPlus=float(x_IPlus)/float(x_PlusPlus)
                p_PlusJ=float(x_PlusJ)/float(x_PlusPlus)
                
                #print(float(x_IJ[I,J]-m_IJ),float((m_IJ*(1-p_IPlus)*(1-p_PlusJ))))

                if float(x_IJ[I,J]-m_IJ)!=0.0 :
                  z_IJ=round(float(x_IJ[I,J]-m_IJ)/float((m_IJ*(1-p_IPlus)*(1-p_PlusJ))**0.5),3)
                else:
                  z_IJ=0.0

                ZscoreArray[I,J] = z_IJ
        self.ZscoreOfSelectedArray = self.Np2Json(ZscoreArray,self.TypeNum,self.TypeNum)
        return self.ZscoreOfSelectedArray
        
    def Re_BoolenZscoreArray_Json(self):      
      if self.ZscoreOfSelectedArray == []:
        self.Re_ZscoreArray_Json()
      #print(self.ZscoreOfSelectedArray)
      idx = 0
      for i in self.ZscoreOfSelectedArray:
        idx+=1
        for key, value in i.items():
          if float(value) >1.96:
            print(idx,key,value)
      
      
    def Np2Json(self,np,x,y):
        '''
        brief:Convert Numpy Array to Json (only x*y array) 
        input:
             np : NumpyArray(x*y)
             x  : Width of np
             y  : height of np
        output:
            {["1":"1383","1,2":"183".......],["1":"1383","1,2":"183".......],[...],...,[...]}
        '''
        reJsonString="["
        for i in range(1,x+1):
            reJsonString += "{"
            for p in range(1,y+1):
                reJsonString += "\""+str(p)+"\":"                
                if p != int(self.TypeNum):
                    reJsonString += "\""+str(np[i,p])+"\","
                else:# For End process
                    reJsonString += "\""+str(np[i,p])+"\""
            if i != int(self.TypeNum):
                reJsonString += "},"
            else:# For End process
                reJsonString += "}"
        reJsonString = reJsonString + "]"
        return json.loads(reJsonString)




##using
FirstBSA = BSA('source.csv',6)
#FirstBSA.showBSArray()
group = 'Community dynamics and Status of C K and P Ideas'
#FirstBSA.ComputeMotionGroup(group)
FirstBSA.showBSArray()
ZscoreArray_Json = FirstBSA.Re_ZscoreArray_Json()
print(ZscoreArray_Json)


outcsv(ZscoreArray_Json,'data')
print(group)

#print(FirstBSA.show(2))
'''
FirstBSA.ComputeMotionGroup('5')
FirstBSA.show()
FirstBSA.ComputeMotionALL()
print FirstBSA.show(2)
print FirstBSA.ReNumOfMotionSet(1,3)
'''