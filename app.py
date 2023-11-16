from flask import Flask, render_template, send_file
from pymongo import MongoClient
import datetime
import json
from fpdf import FPDF
from bson import ObjectId

app = Flask(__name__)

#convert string list to int list
def convertStringList2IntList(StringList):
    IntList = [int(x) for x in StringList]
    #print("convertStringList2IntList Method Test: ", IntList)
    return IntList

#feed into convertStringList2IntList
#convert int list to human readable
def convertEpoch2HumanTime(epochTime):
    datetimeObjects = [datetime.datetime.fromtimestamp(epoch) for epoch in epochTime]
    #for HumanTime in datetimeObjects:
        #("convertEpoch2HumanTime Method Test: ", HumanTime)    
    return datetimeObjects

def convertEpochToReadableString(epochTime):
    """ Convert a list of epoch times to a list of human-readable date-time strings. """
    readableStrings = [datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S') for epoch in epochTime]
    return readableStrings


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
        return hosts_info
    except Exception as e:
        return f"Failed to retrieve hosts information: {e}"


def createPdfFromJson(json_data, pdf_file):
    pdf = FPDF()
    pdf.add_page()
    
    # Use monospaced font for better JSON representation
    pdf.set_font("Courier", size=10)
    
    # Dump the JSON data with indentation
    json_str = json.dumps(json_data, indent=4)
    
    # Add JSON data to the PDF
    pdf.multi_cell(0, 10, json_str)

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
        
        #change epoch time in pdf report human readable
        #print("HostsInfo type: ", type(hostsInfo))
        #for host in hostsInfo:
        # Check if 'DateEpoch' is an integer before conversion
            #if isinstance(host['DateEpoch'], int):
                #host['DateEpoch'] = convertEpoch2HumanTime([host['DateEpoch']])[0]
                #print("[host['DateEpoch']] Test D1: ", host['Hostname'], host['DateEpoch'])
            #else:
                #print("DateEpoch is not an int on host ", host)

        #fix string issue?
        #did this break the capital Objects in the app/download route?
        #object_id = ObjectId(object_id)
        print("getJsonDataForId(object_id) object_id is 4a", object_id, type(object_id))
        object_idStripped = object_id.strip('ObjectId(').rstrip(')')
        print("getJsonDataForId(object_id) object_id is 4b", object_idStripped, type(object_idStripped))
        object_id = ObjectId(object_idStripped)
        print("getJsonDataForId(object_id) object_id is 4c", object_id, type(object_id))

        json_data = next((host for host in hostsInfo if host['_id'] == object_id), None)
        print("json_data in getjsondataforID TEST 3c", json_data)
        #returning 'None'
        if json_data:
            # Check and convert DateEpoch to human-readable string format
            if 'DateEpoch' in json_data and isinstance(json_data['DateEpoch'], int):
                json_data['DateEpoch'] = convertEpochToReadableString([json_data['DateEpoch']])[0]
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
        # Connect to MongoDB
        username = "webappUser"
        password = "ReportT!me"
        host = "192.168.168.142"
        port = "27017"
        myDatabase = 'ForwardDB'

        connectionURL = f"mongodb://{username}:{password}@{host}:{port}/{myDatabase}"
        
        client = MongoClient(connectionURL)
        
        # Create reference to 
        db = client[myDatabase]

        # Define collection
        collection = db['ForwardCollection']

        # Use aggregation pipeline to get the most recent document for each host
        pipeline = [
            {"$sort": {"DateEpoch": -1}},
            {"$group": {"_id": "$Hostname", "latest_doc": {"$first": "$$ROOT"}}},
            {"$replaceRoot": {"newRoot": "$latest_doc"}}
        ]

        # Execute the aggregation pipeline
        documents = list(collection.aggregate(pipeline))

        # Needed to get the number of compliant and noncompliant machines
        compliantCount = sum(doc.get('CompliantTF') == True for doc in documents)
        noncompliantCount = sum(doc.get('CompliantTF') == False for doc in documents)

        CompliantHosts = [doc.get('Hostname') for doc in documents if doc.get('CompliantTF') == True]
        NoncompliantHosts = [doc.get('Hostname') for doc in documents if doc.get('CompliantTF') == False]

        # Get 'DateEpoch' values. 
        date_epoch_values = [doc.get('DateEpoch') for doc in documents]
        Hostname = [doc.get('Hostname') for doc in documents]
        CompliantTF = [doc.get('CompliantTF') for doc in documents]

        # Get details for the last scan
        LastScanCursor = collection.find().sort("DateEpoch", -1).limit(1)
        LastScanDocument = list(LastScanCursor)[0]
        LastScanEpoch = LastScanDocument.get('DateEpoch')
        LastScanHuman = convertEpoch2HumanTime([LastScanEpoch])[0]

        return render_template('index.html', NoncompliantHosts=NoncompliantHosts, CompliantHosts=CompliantHosts, compliantCount=compliantCount, noncompliantCount=noncompliantCount, LastScanHuman=LastScanHuman, Hostname=Hostname, CompliantTF=CompliantTF, TimeOfHuman=convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))

    except Exception as e:
        return f"Def index error: {e}"












    

#+++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/hosts')
def hosts():
    try:
        # Connect to MongoDB
        usename = "webappUser"
        paswd = "ReportT!me"
        host = "192.168.168.142"
        port = "27017"
        myDatabase = 'ForwardDB'

        connectionURL = f"mongodb://{usename}:{paswd}@{host}:{port}/{myDatabase}"
        client = MongoClient(connectionURL)
        
        # Create a reference to the database
        db = client[myDatabase]

        # Define the collection
        collection = db['ForwardCollection']

        # Use aggregation pipeline to get the most recent document for each host
        pipeline = [
            {"$sort": {"DateEpoch": -1}},
            {"$group": {"_id": "$Hostname", "latest_doc": {"$first": "$$ROOT"}}},
            {"$replaceRoot": {"newRoot": "$latest_doc"}}
        ]

        # Execute the aggregation pipeline
        hostsInfo = list(collection.aggregate(pipeline))

        # Convert DateEpoch to human-readable format
        for host in hostsInfo:
            if isinstance(host['DateEpoch'], int):
                host['DateEpoch'] = convertEpoch2HumanTime([host['DateEpoch']])[0]

        # Get the details for the last scan
        LastScanCursor = collection.find().sort("DateEpoch", -1).limit(1)
        LastScanDocument = list(LastScanCursor)[0]
        LastScanEpoch = LastScanDocument.get('DateEpoch')
        LastScanHuman = convertEpoch2HumanTime([LastScanEpoch])[0]

        return render_template('hosts.html', hostsInfo=hostsInfo, LastScanHuman=LastScanHuman)

    except Exception as e:
        return f"Def hosts() error: {e}"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/machine/<hostname>')
def machine(hostname):
    try:
        # Connect to MongoDB
        usename = "webappUser"
        paswd = "ReportT!me"
        host = "192.168.168.142"
        port = "27017"
        myDatabase = 'ForwardDB'

        connectionURL = f"mongodb://{usename}:{paswd}@{host}:{port}/{myDatabase}"

        client = MongoClient(connectionURL)

        # Create reference to
        db = client[myDatabase]

        # Define collection
        collection = db['ForwardCollection']

        # Find documents for the specified hostname
        cursor = collection.find({'Hostname': hostname}).sort("DateEpoch", -1)
        # Convert cursor to a list of dictionaries
        documents = list(cursor)

        # Convert DateEpoch to human-readable format
        for host in documents:
            if isinstance(host['DateEpoch'], int):
                host['DateEpoch'] = convertEpoch2HumanTime([host['DateEpoch']])[0]
        # Extract relevant information
        #date_epoch_values = [doc.get('DateEpoch') for doc in documents]
        #Hostname = [doc.get('Hostname') for doc in documents]
        #CompliantTF = [doc.get('CompliantTF') for doc in documents]

        # Find the last scan for the specified hostname
        #LastScanCursor = collection.find({'Hostname': hostname}).sort("DateEpoch", -1).limit(1)
        #LastScanDocument = list(LastScanCursor)[0]
        #LastScanEpoch = LastScanDocument.get('DateEpoch')
        #LastScanHuman = convertEpoch2HumanTime([LastScanEpoch])[0]

        return render_template('machine.html', hostname=hostname, documents=documents)

    except Exception as e:
        return f"Def machine error: {e}"
#+++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route('/download_pdf/<object_id>')
def download_pdf(object_id):
    try:
        print("download_PDF(Object_id) object_id TEST 1a: ", object_id)
       
        json_data = getJsonDataForId(object_id)
        print("download_PDF(Object_id) getjsondataforID TEST 2a: ", json_data)

        if json_data:
            pdf_file = f'{object_id}.pdf'
            print("download_PDF(Object_id) If json_data TEST 3a: ", pdf_file)
            createPdfFromJson(json_data, pdf_file)
            return send_file(pdf_file, as_attachment=True)
        else:
            return f"Error one: No data found for _id {object_id}"
          

    except Exception as e:
        return f"Error two: {e}"




#+++++++++++++++++++++++++++++++++++++++++++++++++++++

#covers all app.routes
#enables dbugmode and runs on port 8000
if __name__ == '__main__':
    app.run(debug=True, port=8000)

