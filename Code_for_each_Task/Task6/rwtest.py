# -*- coding: utf-8 -*-
"""
 Author      : Lida Liu
 Version     : 1.0
 Copyright   : All rights reserved. Do not distribute. 
 You are welcomed to modify the code.
 But any commercial use you need to contact me
"""

import os
import time
import matplotlib
matplotlib.use('Agg') 
from matplotlib import pyplot as plt
import shutil

def get_FileSize(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)


def draw_hist2(areaList,Title,Xlabel,Ylabel,Xmin,Xmax,Ymin,Ymax,totalAverage,filename):
    text = totalAverage
    index = [1,2,3,4,5,6,7,8,9,10]
    plt.bar(index , areaList, width=0.3 , color='g')
    plt.plot([0,11],[totalAverage,totalAverage],'r')
    plt.text(5, totalAverage, text, ha='center', va= 'bottom',fontsize=11) 
    plt.xlabel(Xlabel)
    plt.xlim(Xmin,Xmax)
    plt.ylabel(Ylabel)
    plt.ylim(Ymin,Ymax)
    plt.grid(True)
    plt.title(Title)
    plt.plot(totalAverage, color="red") 
    for a,b in zip(index,areaList):
        plt.text(a, b, b, ha='center', va= 'bottom',fontsize=11) 
    plt.savefig(filename , dpi=100)
    plt.close()


def file_name(file_dir): 
    fileList=[] 
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            fileList.append(os.path.join(root, file))
    return fileList
    
    
def get_Speed(fileSize,timeStamp1,timeStamp2):
    processSpeed = fileSize/((timeStamp2-timeStamp1))
    return round(processSpeed,2)
    

def main():   
    fileList=[]
    fileSize = []
    writingTime = []
    writingSpeed = []
    readingTime = []
    readingSpeed = []
    
    fileList = file_name("/home/ubuntu/internal")
    
    for fileName in fileList:
        
        size = get_FileSize(fileName)
        fileSize.append(size)
    
        timeStamp3 = time.time()
        command = '/srv/hops/hadoop/bin/hdfs dfs -moveFromLocal ' + fileName + ' /rwtest'
        os.popen(command)
        timeStamp4 = time.time()
        readingTime.append(timeStamp4 - timeStamp3)
        rspeed = get_Speed(size,timeStamp3,timeStamp4)
        readingSpeed.append(rspeed)


        timeStamp1 = time.time()
        command = '/srv/hops/hadoop/bin/hdfs dfs -copyToLocal /rwtest/' + fileName.replace("/home/ubuntu/internal/","") + ' /home/ubuntu/internal'
        os.popen(command)
        timeStamp2 = time.time()
        writingTime.append(timeStamp2 - timeStamp1)
        wspeed = get_Speed(size,timeStamp1,timeStamp2)
        writingSpeed.append(wspeed)
        
        
        print "FileName:",fileName
        print "FileSize;",size,"mb"
        print "Writing time:", timeStamp2 - timeStamp1,"s"
        print "Writing Speed:", wspeed,"MB/S"
        print "Reading time:", timeStamp4 - timeStamp3,"s"
        print "Reading Speed:", rspeed,"MB/S","\n"
        
        command = '/srv/hops/hadoop/bin/hdfs dfs -rm /rwtest/' + fileName.replace("/home/ubuntu/internal/","")
        os.popen(command)
        
    totalSize = 0
    for t_size in fileSize:
        totalSize = totalSize + t_size
        
    totalWTime = 0
    for t_time in writingTime:
        totalWTime = totalWTime + t_time
        
    totalRTime = 0
    for t_time in readingTime:
        totalRTime = totalRTime + t_time    
    
    
    averageWriting = round(totalSize/totalWTime,2)
    averageReading = round(totalSize/totalRTime,2)
     
    print "Total file size:",totalSize,"mb"
    print "Total writing time consume:",totalWTime,"s"
    print "Average Wring Speed:",averageWriting,"MB/s"
    print "Total reading time consume:",totalRTime,"s"
    print "Average Reading Speed:",averageReading,"MB/s","\n"
    
    draw_hist2(writingSpeed,'Storage Writing Throughput','File','Throughput(MB/S)',0,11,0,max(writingSpeed)+5,averageWriting,'writing.png')
    
    draw_hist2(readingSpeed,'Storage Reading Throughput','File','Throughput(MB/S)',0,11,0,max(readingSpeed)+5,averageReading,'reading.png')
    
if __name__ == "__main__": 
  main()