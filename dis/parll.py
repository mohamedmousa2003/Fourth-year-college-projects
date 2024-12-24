from mpi4py import MPI
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report,recall_score,precision_score
from sklearn.svm import SVC
import time
data=pd.read_csv("weather_classification_data.csv")
start_time=time.time()
def Label_Encoder(data):
    dect_Cloud={'overcast':0,
      'partly cloudy':1,
      'clear':2,
      'cloudy':3}
    dect_Season={'Summer':0,
             'Winter':1,
             'Autumn':2,
             'Spring':3}
    dect_Location={'inland':0,
               'mountain':1,
               'coastal':2}
    dect_WeatherType={'Rainy':0,
                  'Cloudy':1,
                  'Snowy':2,
                  'Sunny':3
                  }
    
    data['Cloud Cover']=data['Cloud Cover'].map(dect_Cloud)
    data['Season']=data['Season'].map(dect_Season)    
    data['Location']=data['Location'].map(dect_Location)
    data['Weather Type']=data['Weather Type'].map(dect_WeatherType)
    return data

class_name=['Rainy','cloudy','snowy','sunny']
# Initialize the MPI environment
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Get the rank of the process
size = comm.Get_size()  # Get the total number of processes
#--------------Split_Data--------------
if rank ==0:
    try:
        data1=data[data['Weather Type']=='Rainy']
        data2=data[data['Weather Type']=='Cloudy']
        comm.send(data1,dest=3)
        comm.send(data2,dest=4)
        print("Data has been sent to process 3 and 4")
    except Exception as e:
        print("Error in sending data:", e)
elif rank==1:
    try:
        data3=data[data['Weather Type']=='Sunny']
        data4=data[data['Weather Type']=='Snowy']
        comm.send(data3,dest=5)
        comm.send(data4,dest=6)
        print("Data has been sent to process 5 and 6")
    except Exception as e:
        print("Error in sending data:", e)
#--------------preprossecing--------------
if rank==3:
    try:
        data1=comm.recv(source=0)
        print("data has been recived from process 0")
    except Exception as e:
        print("Error in reciving data:", e)
    try:
        data1.drop_duplicates(inplace=True)
        data1=Label_Encoder(data1)
        print("Data has been preprocessed in process 3")
    except Exception as e:
        print("Error in preprocessing data:", e)
    try:
        comm.send(data1,dest=7)
        print("Data has been sent to process 7")
    except Exception as e:
        print("Error in sending data:", e)
    
elif rank==4:
    try:
        data2=comm.recv(source=0)
        print("Data has been recived from process 0")
    except Exception as e:
        print("Error in reciving data:", e)
    try:
        data2.drop_duplicates(inplace=True)
        data2=Label_Encoder(data2)
        print("Data has been preprocessed in process 4")
    except Exception as e:
        print("Error in preprocessing data:", e)

    try:
        comm.send(data2,dest=7)
        print("Data has been sent to process 7")
    except Exception as e:
        print("Error in sending data:", e)


elif rank==5:    
    try:
        data3=comm.recv(source=1)
        print("Data has been received from process 1")
    except Exception as e:
        print("Error in receiving data:", e)
    try:
        data3.drop_duplicates(inplace=True)
        data3=Label_Encoder(data3)
        print("Data has been preprocessed in process 5")
    except Exception as e:
        print("Error in preprocessing data:", e)
    try:
        comm.send(data3,dest=7)
        print("Data has been sent to process 7")
    except Exception as e:
        print("Error in sending data:", e)
    
    
elif rank==6:
    try:
        data4=comm.recv(source=1)
        print("Data has been received from process 1")
    except Exception as e:
        print("Error in receiving data:", e)
    try:
        data4.drop_duplicates(inplace=True)
        data4=Label_Encoder(data4)
        print("Data has been preprocessed in process 6")
    except Exception as e:
        print("Error in preprocessing data:", e)
    try:
        comm.send(data4,dest=7)
        print("Data has been sent to process 7")
    except Exception as e:
        print("Error in sending data:", e)

#--------------Data gathering--------------
if rank==7:
    try:
        data1=comm.recv(source=3)
        data2=comm.recv(source=4)
        data3=comm.recv(source=5)
        data4=comm.recv(source=6)
        print("Data has been recived from process 3,4,5,6")
    except Exception as e:
        print("Error in reciving data:", e)
    datax=pd.concat([data1,data2,data3,data4])

#--------------Train_Test_Split--------------
    x=datax.drop('Weather Type',axis=1)
    y=datax['Weather Type']
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)
    send_data={'x_train':x_train,
               'x_test':x_test,
              'y_train':y_train,
             'y_test':y_test}
    try:
        comm.send(send_data,dest=8)
        comm.send(send_data,dest=9)
        comm.send(send_data,dest=10)
        print("Data has been sent to process 8,9,10") 
    except Exception as e:
        print("Error in sending data:", e)

if rank==8:
    try:
        recive_data=comm.recv(source=7)
        print("Data has been recived from process 7")
    except Exception as e:
        print("Error in reciving data:", e)
    x_train=recive_data['x_train']
    x_test=recive_data['x_test']
    y_train=recive_data['y_train']
    y_test=recive_data['y_test']
    model=SVC()
    model.fit(x_train,y_train)
    pred=model.predict(x_test)
    Acc=accuracy_score(y_test,pred)
    recall=recall_score(y_test,pred,average='macro')
    presion=precision_score(y_test,pred,average='macro')
    class_Report=classification_report(y_test, pred,target_names=class_name)
    dect_acc={'Report':[Acc,recall,presion],
              "class_report":class_Report}
    try:
        comm.send(dect_acc,dest=0)
    except Exception as e:
        print("Error in sending data:", e)
#--------------Decision_Tree_Model--------------
elif rank==9:
    try:
        recive_data=comm.recv(source=7)
        print("Data has been received from process 7")
    except Exception as e:
        print("Error in receiving data:", e)
    x_train=recive_data['x_train']
    x_test=recive_data['x_test']
    y_train=recive_data['y_train']
    y_test=recive_data['y_test']
    model=DecisionTreeClassifier()
    model.fit(x_train,y_train)
    pred=model.predict(x_test)
    Acc=accuracy_score(y_test,pred)
    recall=recall_score(y_test,pred, average='macro')
    presion=precision_score(y_test,pred, average='macro')
    class_Report=classification_report(y_test, pred,target_names=class_name)
    dect_acc={'Report':[Acc,recall,presion],
              "class_report":class_Report}
    try:
        comm.send(dect_acc,dest=0)
        print("Data has been sent to process 0")
    except Exception as e:
        print("Error in sending data:", e)
#--------------Random_Forest_Model--------------
elif rank==10:
    try:
        recive_data=comm.recv(source=7)
        print("Data has been received from process 7")
    except Exception as e:
        print("Error in receiving data:", e)
    x_train=recive_data['x_train']
    x_test=recive_data['x_test']
    y_train=recive_data['y_train']
    y_test=recive_data['y_test']
    model=RandomForestClassifier()
    model.fit(x_train,y_train)
    pred=model.predict(x_test)
    Acc=accuracy_score(y_test,pred)
    recall=recall_score(y_test,pred, average='macro')
    presion=precision_score(y_test,pred, average='macro')
    class_Report=classification_report(y_test, pred,target_names=class_name)
    dect_acc={'Report':[Acc,recall,presion],
              "class_report":class_Report}
    try:
        comm.send(dect_acc,dest=0)
        print("Data has been sent to process 0")
    except Exception as e:
        print("Error in sending data:", e)

#--------------Display_Model_ACC--------------
if rank==0:
    try:
        Report_DT=comm.recv(source=8)
        Report_RF=comm.recv(source=9)
        Report_SVC=comm.recv(source=10)
    except Exception as e:
        print("Error in receiving data:", e)
    print(f"Classification Report for SVC : {Report_SVC['class_report']} ")
    print(f"Classification Report for Decision Tree : {Report_DT['class_report']} ")
    print(f"Classification Report for Random Forest : {Report_RF['class_report']} ")
    report=pd.DataFrame([Report_SVC['Report'],Report_DT['Report'],Report_RF['Report']],columns=['Accuracy','Recall','Precision'],index=['SVC','Decision Tree','Random Forest'])
    print(report.head())
    end_time=time.time()
    print("==============================================================")
    print(f"Time taken to execute the code is {end_time-start_time} seconds")
MPI.Finalize()