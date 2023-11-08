from flask import Flask, render_template, send_file
from pymongo import MongoClient
import datetime
import json
from fpdf import FPDF
from bson import ObjectId

app = Flask(__name__)

#get epoch time in list 'date_epoch_values'

#convert string list to int list
def convertStringList2IntList(StringList):
    IntList = [int(x) for x in StringList]
    #print("convertStringList2IntList Method Test: ", IntList)
    return IntList

#get rid of list so datetime library will convert to humanreadable
#feed into convertStringList2IntList
#convert int list to human readable
def convertEpoch2HumanTime(epochTime):
    datetimeObjects = [datetime.datetime.fromtimestamp(epoch) for epoch in epochTime]
    #for HumanTime in datetimeObjects:
        #("convertEpoch2HumanTime Method Test: ", HumanTime)    
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

def getHostsInfo(collection):
    try:
        hosts_info = list(collection.find({}))
        #for host in hosts_info:
            #host['DateEpoch'] = convertEpoch2HumanTime(convertStringList2IntList([host['DateEpoch']]))[0]
        print("getHostsInfo called, returning", hosts_info)
        return hosts_info
    except Exception as e:
        return f"Failed to retrieve hosts information: {e}"

def createPdfFromJson(json_data, pdf_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, json.dumps(json_data, indent=4))
    pdf.output(pdf_file)

def getJsonDataForId(object_id):
    try:
        print("getJsonDataForId ojbect_id TEST 1b: ", object_id)
        #ObjectId(654aa93a5ecdc68f75d7858f)

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
        hostsInfo = getHostsInfo(collection)
        
        #fix string issue?
        #did this break the capital Objects in the app/download route?
        #object_id = ObjectId(object_id)
        object_id = ObjectId('654aa925f2fa34af89ddb845')

        json_data = next((host for host in hostsInfo if host['_id'] == object_id), None)
        print("json_data in getjsondataforID TEST 3b", json_data)
        #returning 'None'
        if json_data:
            return {
                key: json_data[key] for key in json_data.keys() if key != '_id'
            }
        else:
            return None
    except Exception as e:
        return f"Error retrieving JSON data: {e}"


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

        hostsInfo = getHostsInfo(collection)
        print("hostsinfo from host", hostsInfo)

#TimeOfHuman = convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values))

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

        return render_template('hosts.html' ,hostsInfo = hostsInfo, compliantCount = compliantCount,noncompliantCount = noncompliantCount, LastScanHuman = LastScanHuman, Hostname = Hostname, CompliantTF = CompliantTF, TimeOfHuman = convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))
     
    except Exception as e:
        return f"Failed to connect to database: {e}"
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

@app.route('/download_pdf/<object_id>')
def download_pdf(object_id):
    try:
        print("download_PDF(Object_id) object_id TEST 1a: ", object_id)
        #ObjectId(654aa93a5ecdc68f75d7858f)
        json_data = getJsonDataForId(object_id)
        print("download_PDF(Object_id) getjsondataforID TEST 2a: ", json_data)
            #returning 'None'

            #not triggering
        if json_data:
            pdf_file = f'{object_id}.pdf'
            print("download_PDF(Object_id) If json_data TEST 3a: ", pdf_file)
            createPdfFromJson(json_data, pdf_file)
            return send_file(pdf_file, as_attachment=True)
        else:
            return f"Error one: No data found for _id {object_id}"
            #Error one: No data found for _id ObjectId(654aa93a5ecdc68f75d7858f)

    except Exception as e:
        return f"Error two: {e}"




#+++++++++++++++++++++++++++++++++++++++++++++++++++++

#covers all app.routes
#enables dbugmode and runs on port 8000
if __name__ == '__main__':
    app.run(debug=True, port=8000)

