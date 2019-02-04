# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:38:17 2019

@author: dhiOmics
"""

import json
import requests


def lambda_handler(request, context):
    print(request)
    
    # Fetch records using api calls
    (insertTransactions, newTransactionCursor,hasMore) = api_response(request['state'], request['secrets'])

    # Populate records in insert    
    insert = {}    
    insert['test2'] = insertTransactions
    
    #delete = {}
    #delete['test2'] = deleteTransactions
    
    state = {}
    state['cursor'] = newTransactionCursor
    
    transactionsSchema = {}
    transactionsSchema['primary_key'] = ['Event_Id']
    
    schema = {}
    schema['test2'] = transactionsSchema
    
    response = {}
    
    # Add updated state to response
    response['state'] =  state
    
    # Add all the records to be inserted in response
    response['insert'] = insert
    
    # Add all the records to be marked as deleted in response
    #response['delete'] = delete
    
    # Add schema defintion in response
    response['schema'] = schema
    
    # Add hasMore flag
    response['hasMore'] = hasMore
    
    return response
    

def api_response(state, secrets):
    
    #Defining Cursor
    try:
        initialCursor=state['cursor']
    except:
        initialCursor = 0
    cursorLimit = 50
    
    #Parameter to API call
    mailAddress = secrets['Email']
    password = secrets['Password']
    query_tableContent = ("SELECT * from resume_cloning.meeting_info Limit {},{}").format(initialCursor,cursorLimit)
    query_tableColumns = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'meeting_info' ORDER BY ORDINAL_POSITION")
    Input = {'Query_Content': query_tableContent,'Query_Columns':query_tableColumns,'mailAddress':mailAddress,'password':password}
    apiCall = requests.get("http://35.abc.def.ghi/getMeetingsTableAll", params=Input) # PUT URL
    print(apiCall)
    
    #Response of API
    API_response = apiCall.text
    API_response=json.loads(API_response)
    print(API_response['Authentication'])       
    tableContent = API_response['content']
    columnNames= API_response['columns']
    
    #Serialize the table content
    serialized_outputData=[]
    for row in tableContent:
        row_data = dict(zip(columnNames, row))
        serialized_outputData.append(row_data)

    if(len(tableContent)<cursorLimit):
        hasMore = 'false'
        finalCursor = initialCursor + len(tableContent)
    else:
        hasMore = 'true'
        finalCursor = initialCursor + cursorLimit
    
    #deleteTransactions = []
    
    return (serialized_outputData, finalCursor, hasMore)


