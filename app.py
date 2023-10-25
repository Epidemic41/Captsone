from flask import Flask, render_template
from pymongo import MongoClient
import datetime

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


#display humanreadable human time in html

 
#def Connect2MongoDB():



@app.route('/')
def index():
    try:
        #connect to MongoDB
        usename = "webappUser"
        paswd = "ReportT!me"
        host = "192.168.1.30"
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


        #get 'DateEpoch' values. 
            #'DateEpoch' is json key
            #'date_epoch_values' is reference in the html
        date_epoch_values = [doc.get('DateEpoch') for doc in documents]
        Hostname = [doc.get('Hostname') for doc in documents]
        CompliantTF = [doc.get('CompliantTF') for doc in documents]

        
        
        #print("convertEpoch2HumanTime method test: ", convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))

        #convert epochtime into integer so datetime will take it 
        #print(convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))
        #print("date_epoch_values: ", date_epoch_values)

        return render_template('index.html' , Hostname = Hostname, CompliantTF = CompliantTF, TimeOfHuman = convertEpoch2HumanTime(convertStringList2IntList(date_epoch_values)))
     
    except Exception as e:
        return f"Failed to connect to database: {e}"
    











    

#+++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/hosts')
def hosts():
    return render_template ('hosts.html')
#+++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/machine')
def machine():
    return '<title>machine</title><h1>machine1  page</h1>'
#+++++++++++++++++++++++++++++++++++++++++++++++++++++





#covers all app.routes
#enables dbugmode and runs on port 8000
if __name__ == '__main__':
    app.run(debug=True, port=8000)

