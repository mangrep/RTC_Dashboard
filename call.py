'''
Created on Jun 4, 2015

@author: manish_choudhary
'''
import re
import requests
import json
from JazzClint import JazzClient  
import csv

user= 'xxxx'
pw = 'xxxx'
host= 'xxxx'
nameTag=['xxxx']
monthTag='xxxx'
COMPLEXITY_FACTOR=0.125
workItemsList = []
keyList=['typeOfIssue','ticketId','description','ownedBy','status','priority','severity','modificationDate','complexity','estimate','tags','createdBy']
# Log into Jazz/RTC instance

print ("Starting...")
jazz = JazzClient(host,user,pw) #Login

# Grab a specific work item , just to prove that we can do it
for tag in nameTag:  
    url= host + 'oslc/contexts/_uUlSAX8fEeKbRq-TfFhUFA/workitems?oslc.where=dcterms:subject=%22'+ tag +'%22%20and%20dcterms:subject=%22'+ monthTag +'%22'
    print ("Grabbing Work Items URLs for " + tag + " ...")
    accept='application/rdf+xml'
    workItemXml = jazz.getDataFromUrl(url, accept)
    #extracting url from workItemXml
    urls = re.findall('https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', workItemXml) 
    accept='application/json'
    #Downloading workitems
    for url in urls:
        if 'com.ibm.team.workitem.WorkItem' in url:    
            #print (url)
            #workItemsList.append(jazz.getDataFromUrl(url1,accept)
            workItemsList.append(jazz.parse1(jazz.getDataFromUrl(url,accept)))
fileall=open(monthTag + '_all' +'.csv',"wb")
fileWithEstimate=open(monthTag + '_WithEstimate' +'.csv',"w")
fileWithoutEstimate=open(monthTag+ '_WithoutEstimate' + '.csv',"w")

fileAll = csv.DictWriter(fileall,keyList);
fileWith = csv.DictWriter(fileWithEstimate, keyList)
fileWithout = csv.DictWriter(fileWithoutEstimate, keyList)

fileAll.writeheader()
fileWith.writeheader()
fileWithout.writeheader()
#
#for workItem in workItemsList:
#    if workItem['estimate'] != '' :
#        fileWithEstimate.write(workItem.get)
#    else:
#        fileWithoutEstimate.write()
# 
#fileWithEstimate.close()
#fileWithoutEstimate.close()


for workItem in workItemsList:
    #print (workItem['estimate'])
    w = workItem['estimate']
    if w != "None":
        fileWith.writerow(workItem)
    else:
        fileWithout.writerow(workItem)
        


fileAll.writerows(workItemsList)
fileall.close()
fileWithEstimate.close()
fileWithoutEstimate.close()



