from flask import Flask, render_template, send_file
from pymongo import MongoClient
import datetime
import json
#Download module in 'my_env'
# from fpdf import FPDF

app = Flask(__name__)

#get epoch time in list 'date_epoch_values'

#convert string list to int list
def convertStringList2IntList(StringList):
    IntList = [int(x) for x in StringList]
    print("convertStringList2IntList Method Test: ", IntList)
    return IntList

#get rid of list so datetime library will convert to humanreadable
#feed into convertStringList2IntList
#convert int list to human readable
def convertEpoch2HumanTime(epochTime):
    datetimeObjects = [datetime.datetime.fromtimestamp(epoch) for epoch in epochTime]
    for HumanTime in datetimeObjects:
        print("convertEpoch2HumanTime Method Test: ", HumanTime)    
    return datetimeObjects

#display number of compliant machines
def countCompliantHosts(collection):
    try:
        count = collection.count_documents({"CompliantTF": True})
        return count

    except Exception as e:
        return f"Failed to connect to the database: {e}"
    
def countNoncompliantHosts(collection):
    try:
        count = collection.count_documents({"CompliantTF": False})
        return count

    except Exception as e:
        return f"Failed to connect to the database: {e}"


#display humanreadable human time in html

 
#def Connect2MongoDB():



@app.route('/')
def index():
    try:
        #connect to MongoDB
        usename = "webappUser"
        paswd = "ReportT!me"
        host = "192.168.168.142"
        port = "27017"
        myDatabase = 'ForwardDB'

        connectionURL = f"mongodb://{usename}:{paswd}@{host}:{port}/{myDatabase}"
        
        client = MongoClient(connectionURL)
        
        #create reference to 
        db = client[myDatabase]

        #define collection
        collection = db['ForwardCollection']

        #find all documents in the collection
        cursor = collection.find({})
            #print("cursor is: ", cursor)
        #convert cursor to a list of dictionaries. all database contents are stored here?
        documents = list(cursor)
            #print(documents)

        #needed to get number of compliant and noncompliant machines
        CompliantTF = [doc.get('CompliantTF') for doc in documents]
        compliantCount = countCompliantHosts(collection)
        noncompliantCount = countNoncompliantHosts(collection)

        CompliantHosts = [doc.get('Hostname') for doc in documents if doc.get('CompliantTF') == True]
        NoncompliantHosts = [doc.get('Hostname') for doc in documents if doc.get('CompliantTF') == False]


        #get 'DateEpoch' values. 
            #'DateEpoch' is json key
            #'date_epoch_values' is reference in the html
        date_epoch_values = [doc.get('DateEpoch') for doc in documents]
        Hostname = [doc.get('Hostname') for doc in documents]
        CompliantTF = [doc.get('CompliantTF') for doc in documents]

        #LastScan = collection.find().sort("DateEpoch", -1 ).limit(1)
        #LastScan = str(LastScan)

        LastScanCursor = collection.find().sort("DateEpoch", -1 ).limit(1)
        LastScanDocument = list(LastScanCursor)[0]
        LastScanEpoch = LastScanDocument.get('DateEpoch')
        LastScanHuman = convertEpoch2HumanTime([LastScanEpoch])[0]

        
        
        #print("convertEpoch2HumanTime method test: ", convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))

        #convert epochtime into integer so datetime will take it 
        #print(convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))
        #print("date_epoch_values: ", date_epoch_values)

        return render_template('index.html' ,NoncompliantHosts = NoncompliantHosts, CompliantHosts = CompliantHosts, compliantCount = compliantCount,noncompliantCount = noncompliantCount, LastScanHuman = LastScanHuman, Hostname = Hostname, CompliantTF = CompliantTF, TimeOfHuman = convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))
     
    except Exception as e:
        return f"Failed to connect to database: {e}"
    











    

#+++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/hosts')
def hosts():
    return render_template ('hosts.html')
#+++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/machine')
def machine():
    try:
        #connect to MongoDB
        usename = "webappUser"
        paswd = "ReportT!me"
        host = "192.168.168.142"
        port = "27017"
        myDatabase = 'ForwardDB'

        connectionURL = f"mongodb://{usename}:{paswd}@{host}:{port}/{myDatabase}"
        
        client = MongoClient(connectionURL)
        
        #create reference to 
        db = client[myDatabase]

        #define collection
        collection = db['ForwardCollection']

        #find all documents in the collection
        cursor = collection.find({})
            #print("cursor is: ", cursor)
        #convert cursor to a list of dictionaries. all database contents are stored here?
        documents = list(cursor)
            #print(documents)

        #needed to get number of compliant and noncompliant machines
        CompliantTF = [doc.get('CompliantTF') for doc in documents]
        compliantCount = countCompliantHosts(collection)
        noncompliantCount = countNoncompliantHosts(collection)

        #get 'DateEpoch' values. 
            #'DateEpoch' is json key
            #'date_epoch_values' is reference in the html
        date_epoch_values = [doc.get('DateEpoch') for doc in documents]
        Hostname = [doc.get('Hostname') for doc in documents]
        CompliantTF = [doc.get('CompliantTF') for doc in documents]

        #LastScan = collection.find().sort("DateEpoch", -1 ).limit(1)
        #LastScan = str(LastScan)

        LastScanCursor = collection.find().sort("DateEpoch", -1 ).limit(1)
        LastScanDocument = list(LastScanCursor)[0]
        LastScanEpoch = LastScanDocument.get('DateEpoch')
        LastScanHuman = convertEpoch2HumanTime([LastScanEpoch])[0]

        
        
        #print("convertEpoch2HumanTime method test: ", convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))

        #convert epochtime into integer so datetime will take it 
        #print(convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))
        #print("date_epoch_values: ", date_epoch_values)

        return render_template('machine.html' ,compliantCount = compliantCount,noncompliantCount = noncompliantCount, LastScanHuman = LastScanHuman, Hostname = Hostname, CompliantTF = CompliantTF, TimeOfHuman = convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))
     
    except Exception as e:
        return f"Failed to connect to database: {e}"
#+++++++++++++++++++++++++++++++++++++++++++++++++++++





#covers all app.routes
#enables dbugmode and runs on port 8000
if __name__ == '__main__':
    app.run(debug=True, port=8000)

