# -*- coding: utf-8 -*-
"""
 Author      : Lida Liu
 Version     : 1.0
 Copyright   : All rights reserved. Do not distribute. 
 You are welcomed to modify the code.
 But any commercial use you need to contact me
"""

from google.cloud import storage
import os
import time
from matplotlib import pyplot as plt


def get_FileSize(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)


def draw_hist2(areaList,Title,Xlabel,Ylabel,Xmin,Xmax,Ymin,Ymax,totalAverage):
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
    plt.show()
    plt.close()


def file_name(file_dir): 
    fileList=[] 
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            fileList.append(os.path.join(root, file))
    return fileList
    
    
def get_Speed(fileSize,timeStamp1,timeStamp2):
    processSpeed = fileSize/(timeStamp2-timeStamp1)
    return round(processSpeed,2)
    

def main():   
    fileList=[]
    fileSize = []
    writingTime = []
    writingSpeed = []
    readingTime = []
    readingSpeed = []
    
    fileList = file_name("/Users/harry/Desktop/Test1")
    
    for fileName in fileList:
        
        size = get_FileSize(fileName)
        fileSize.append(size)
    
        client= storage.Client.from_service_account_json('Group6-p2p-6044660939e4.json')
        
        bucket = client.get_bucket('id2210task1')
        blob = bucket.blob(fileName.replace("/Users/harry/Desktop/",""))
        
        timeStamp1 = time.time()
        blob.upload_from_filename(fileName)
        timeStamp2 = time.time()
        writingTime.append(timeStamp2 - timeStamp1)
        wspeed = get_Speed(size,timeStamp1,timeStamp2)
        writingSpeed.append(wspeed)
        
        
        timeStamp3 = time.time()
        blob.download_to_filename(fileName.replace("Test1","Test2"))
        timeStamp4 = time.time()
        readingTime.append(timeStamp4 - timeStamp3)
        rspeed = get_Speed(size,timeStamp3,timeStamp4)
        readingSpeed.append(rspeed)
        
        print "FileName:",fileName
        print "FileSize;",size,"mb"
        print "Uploading time:", timeStamp2 - timeStamp1,"s"
        print "Writing Speed:", wspeed,"mb/s"
        print "Downloading time:", timeStamp4 - timeStamp3,"s"
        print "Reading Speed:", rspeed,"mb/s","\n"

        blob.delete()
        
        
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
    print "Total uploading time consume:",totalWTime,"s"
    print "Average Wring Speed:",averageWriting,"mb/s"
    print "Total downloading time consume:",totalRTime,"s"
    print "Average Reading Speed:",averageReading,"mb/s","\n"
    
    draw_hist2(writingSpeed,'Storage Writing Throughput','File','Throughput(MB/S)',0,11,0,max(writingSpeed)*1.5,averageWriting)
    
    draw_hist2(readingSpeed,'Storage Reading Throughput','File','Throughput(MB/S)',0,11,0,max(readingSpeed)*1.5,averageReading)
    
if __name__ == "__main__": 
  main()