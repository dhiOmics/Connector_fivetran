# -*- coding: utf-8 -*-
"""
@author: dhiOmics
"""

import MySQLdb
import base64
import traceback


class Database:
    host="localhost"  # your host 
    user="root"       # usernames
    password="root"     # password
    db="resume_cloning"
    
    def __init__(self):
            print('Connection Opened')
            self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
            
    
    def insert(self, query):
            print('inside insert')
            var = ''
            try:
                self.cursor = self.connection.cursor()
#                print("HEY")
                var = self.cursor.execute(query)
                print(str(var))
                self.connection.commit()
            except:
                self.connection.rollback()
            finally:
                self.cursor.close()
                print('Cursor closed')
    
            return(var)


    def callPro(self, query1, query2,procedurName):
        print("Procedure...")
        try:
            self.cursor = self.connection.cursor()
            var = self.cursor.callproc(procedurName,query1)
            var1 = self.cursor.execute(query2)
            print(var)
            print(var1)
            
            self.connection.commit()
        except:
                self.connection.rollback()
        finally:
                self.cursor.close()
                print('Cursor closed')   

    def query(self, query):
        try:
            self.cursor = self.connection.cursor()
            print('inside query')
            self.cursor.execute(query)
            return self.cursor.fetchall()
        finally:
            self.cursor.close()
            print('Cursor closed')
                
    
    def tupleToList(self,tupleVar):
            listVar=[]
            for tupleVarEach in tupleVar:
                listVar.append(tupleVarEach[0])
            return(listVar)

                
    def __del__(self):
#        self.cursor.close()
        print("---------query finished------------")
        self.connection.close()


#verify the credential sent by lambda function
def verifyClientAuthentication(mailAddress,Password):
    print("databaseOperations.py: clientAuthentication()")
    try:
        password = base64.b64encode(bytes(Password, 'utf-8'))
        password = password.decode()
        db=Database()
        query= "SELECT COUNT(1) FROM resume_cloning.login WHERE Email = '{}' and Password_User='{}' and status='Registered' and Role='Admin' ".format(mailAddress,password)
        info=db.query(query)
        count=info[0][0]
        print("\ndatabaseOperations.py: clientAuthentication(): Pass: Executed Successfully")
        if(count==0):
            return(False)
        else:
            return(True)
    except Exception as e:
        error=traceback.print_exc()
        print(error)#Print the exeption
        print("\ndatabaseOperations.py: clientAuthentication(): Fail: Not Executed\n")


def fetchMeetingTable(query_tableContent,query_tableColumns):
    try:
        db=Database()
        #query to fetch content of the table
        tableContent = db.query(query_tableContent)
        #query to fetch names of the column of the table
        columns = db.query(query_tableColumns)
        columnNames=db.tupleToList(columns)
        return({'columns':columnNames,'content':tableContent})
    except:
        error=traceback.print_exc()
        print(error)#Print the exeption
        return({'error':error})
        
