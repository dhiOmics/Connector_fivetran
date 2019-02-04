# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 13:54:19 2019

@author: dhiOmics
"""
from flask import Flask, request, json, jsonify, render_template, redirect, url_for, session, escape
from flask_cors import CORS
import traceback
import databaseOperations
app = Flask(__name__)
CORS(app)

#To AWS lambda function trigger using fivetran connector
@app.route("/getMeetingsTableAll", methods=['POST','GET'])
def getMyMeeting_table():
    print("Enter in /getMeetingsTableAll API")
    try:
        #get values from the parameter
        userMail = request.args.get('mailAddress')
        password = request.args.get('password')
        query_tableContent = request.args.get('Query_Content')
        query_tableColumns = request.args.get('Query_Columns')
        authentication = databaseOperations.verifyClientAuthentication(userMail,password)
        if(authentication==True):
            output=databaseOperations.fetchMeetingTable(query_tableContent,query_tableColumns)
            output['Authentication']='Pass'
        else:
            output = {"Fail":"Access Denined, error in authentication"}
        print("output",output)
        return(str(json.dumps(output)))
    except Exception as e:
        error=traceback.print_exc() 
        print(error)#Print the exeption
        #Write in log files
        ExceptionOut = {"Fail":"Action failed. Try again."}
        #convert into JSON format and return
        return(str(json.dumps(ExceptionOut)))    


if __name__ == '__main__':
    app.run()
    #test_word_cloud()
    #register_test()
    
