import urllib
import httplib2
import json
import re
import datetime

from xml.dom.minidom import parse, parseString
from exceptions import Exception

class JazzClient(object):
   def __init__(self, server_url, user, password):

      self.base_url = server_url
      self.http = httplib2.Http()
      self.http.follow_redirects=True
      self.http.disable_ssl_certificate_validation=True
      self.http.verify=False
      self.headers = {'Content-type': 'text/xml'}

      #1) before authentification one needs to go first to a "restricted resource"

      resp, content = self.http.request( self.base_url + "/oslc/workitems/1.xml", 'GET', headers=self.headers)

      #TODO sometimes returns capital X-
      #TODO check before if the key is in dictionary, if not something is wrong as well
      print ('JazzClient:Init - Setting up cookies......')
      if resp['x-com-ibm-team-repository-web-auth-msg'] != 'authrequired':
         raise Exception("something is wrong seems the server doesn't expect authentication!")
      self.headers['Cookie']=  resp['set-cookie'] 
      self.headers['Content-type'] = 'application/x-www-form-urlencoded'

      #2 now we can start the authentication via j_security_check page
      print ("JazzClient:Init - Authenticating......")
      resp, content = self.http.request(self.base_url+'/j_security_check' , 'POST', headers=self.headers, body=urllib.urlencode({'j_username': user, 'j_password': password}))

      # Save the new cookie returned here
      self.headers['Cookie']=  resp['set-cookie']

      #TODO check auth worked fine, if not throw exception

      #3 get the requested resource - finish the authentication
      print ("JazzClient:Init - Getting catalog......")
      url1='resource/itemOid/com.ibm.team.workitem.query.QueryDescriptor/_5wW70Nj0EeSwntm5B_U5cg?_mediaType=text/html'
      resp, content = self.http.request( self.base_url + url1 , 'GET', headers=self.headers)
      if resp.status != 200:
         print ("JazzClient:Init - BAD RESPONSE")
         print (content)
         raise Exception("JazzClient response status != 200 !!!")

#
# Get Work Item method takes a passed work item number, and returns that work item object in XML format
#
   def getDataFromUrl(self, url,accept): 
      self.headers['Accept'] = accept
  
      resp, content = self.http.request(url, headers=self.headers)
      #print  (resp.status)
      #print  resp.content
      if resp.status != 200:
         print ("BAD RESPONSE")
         print (content)
         raise Exception("JazzClient responce status != 200 !!!")
      return content
   
   def strip_ml_tags(self, in_text):
    s_list = list(in_text)
    i,j = 0,0
    
    while i < len(s_list):
        # iterate until a left-angle bracket is found
        if s_list[i] == '<':
            while s_list[i] != '>':
                # pop everything from the the left-angle bracket until the right-angle bracket
                s_list.pop(i)
                
            # pops the right-angle bracket, too
            s_list.pop(i)
        else:
            i=i+1
            
    # convert the list back into text
    join_char=''
    return join_char.join(s_list)
   def parse1(self, data):
    COMPLEXITY_FACTOR=0.125
    #filedes=open("11.json","r")
    #data=filedes.read()
    dictData = json.loads(data) #data in dictonary form
    typeOfIssue = str(dictData['dc:type']['rdf:resource'].encode('utf-8'))
    lastIndex = typeOfIssue.rfind("/")
    typeOfIssue = str(typeOfIssue[lastIndex+1:]) #type of issue

    ticketId = str( dictData['dc:identifier']) #id
    description = str(dictData['dc:description'].encode('utf-8')) #description
    description = self.strip_ml_tags(description).replace(","," ")
    ownedBy = str(dictData['rtc_cm:ownedBy']['rdf:resource'].encode('utf-8'))  #ownedBy
    ownedByData = (self.getDataFromUrl(ownedBy, 'application/rdf+xml'))
    ownedBy= re.findall('<j.0:name>(.*?)<\/j.0:name>', ownedByData, 0)
    # print (ownedBy + " " + ownedByData)
    status = str(dictData['rtc_cm:remoteStatus'].encode('utf-8')) #status
    
    priority =str(dictData['oslc_cm:priority']['rdf:resource']) #priority
    priorityData = json.loads(self.getDataFromUrl(priority, 'application/json'))
    priority=str(priorityData['dc:title'])
    #print (str(priorityData['dc:title']))
    
    severity = str(dictData['rtc_cm:remoteSeverity'].encode('utf-8')) #severity
    modificationDate = str(dictData['dc:modified'].encode('utf-8')) #modificationDate
    estimate =dictData['rtc_cm:estimate'] #estimate
    #print  estimate
    complexity = 0.0
    if estimate:
       estimate = estimate/3600000
       complexity = float(estimate) * COMPLEXITY_FACTOR
    tags=str(dictData['dc:subject']).replace(","," ").encode('utf-8') #tags
    createdBy=str(dictData['dc:creator']['rdf:resource'].encode('utf-8'))#createdBy
    createdByData = (self.getDataFromUrl(createdBy, 'application/rdf+xml'))
    createdBy= re.findall('<j.0:name>(.*?)<\/j.0:name>', createdByData, 0)
    
    finalData = {'typeOfIssue':typeOfIssue,'ticketId':str(ticketId),'description':description,'ownedBy':str(ownedBy[0]),'status':status,'priority':priority,'severity':severity,'modificationDate':modificationDate,'complexity':str(complexity),'estimate':str(estimate),'tags':tags,'createdBy':str(createdBy[0])}
    #print typeOfIssue + " " + ticketId + " " + description + " " + ownedBy + " " + status + " " + priority  + " " + severity + " " + modificationDate + " " + complexity + " " + estimate + " " + tags + " " + createdBy
    #return typeOfIssue + "," + str(ticketId) + "," + description + "," + str(ownedBy[0]) + "," + status + "," + priority  + "," + severity + "," + modificationDate + "," + str(complexity) + "," + str(estimate) + "," + tags + "," + str(createdBy[0])
    return finalData

    


