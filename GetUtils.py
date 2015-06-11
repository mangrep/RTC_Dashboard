'''
Created on Jun 4, 2015

@author: manish_choudhary
'''
import json
def strip_ml_tags(in_text):
    """Description: Removes all HTML/XML-like tags from the input text.
    Inputs: s --> string of text
    Outputs: text string without the tags
    
    # doctest unit testing framework

    >>> test_text = "Keep this Text <remove><me /> KEEP </remove> 123"
    >>> strip_ml_tags(test_text)
    'Keep this Text  KEEP  123'
    """
    # convert in_text to a mutable object (e.g. list)
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

#def parse1(data):
#    COMPLEXITY_FACTOR=0.125
#    #filedes=open("11.json","r")
#    #data=filedes.read()
#    dictData = json.loads(data) #data in dictonary form
#    typeOfIssue = str(dictData['dc:type']['rdf:resource'].encode('utf-8'))
#    lastIndex = typeOfIssue.rfind("/")
#    typeOfIssue = str(typeOfIssue[lastIndex+1:]) #type of issue
#
#    ticketId = str( dictData['dc:identifier']) #id
#    description = str(dictData['dc:description'].encode('utf-8')) #description
#    description = strip_ml_tags(description).replace(","," ")
#    ownedBy = str(dictData['rtc_cm:ownedBy']['rdf:resource'].encode('utf-8'))  #ownedBy
#    lastIndex = ownedBy.rfind("/")
#    ownedBy = str(ownedBy[lastIndex+1:])
#    status = str(dictData['rtc_cm:remoteStatus'].encode('utf-8')) #status
#    priority =str(dictData['oslc_cm:priority']['rdf:resource']) #priority
#    
#    severity = str(dictData['rtc_cm:remoteSeverity'].encode('utf-8')) #severity
#    modificationDate = str(dictData['dc:modified'].encode('utf-8')) #modificationDate
#    estimate =dictData['rtc_cm:estimate'] #estimate
#    #print  estimate
#    complexity = 0.0
#    if estimate:
#       complexity = float(estimate) * COMPLEXITY_FACTOR
#    tags=str(dictData['dc:subject']).replace(","," ").encode('utf-8') #tags
#    createdBy=str(dictData['dc:creator']['rdf:resource'].encode('utf-8'))#createdBy
#    lastIndex = createdBy.rfind("/")
#    createdBy = createdBy[lastIndex+1:]
#
#    #print typeOfIssue + " " + ticketId + " " + description + " " + ownedBy + " " + status + " " + priority  + " " + severity + " " + modificationDate + " " + complexity + " " + estimate + " " + tags + " " + createdBy
#    return typeOfIssue + "," + str(ticketId) + "," + description + "," + ownedBy + "," + status + "," + priority  + "," + severity + "," + modificationDate + "," + str(complexity) + "," + str(estimate) + "," + tags + "," + createdBy

    


