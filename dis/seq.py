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
#--------------preprossecing--------------

data.drop_duplicates(inplace=True)
data=Label_Encoder(data)

#--------------Train_Test_Split--------------
x=data.drop('Weather Type',axis=1)
y=data['Weather Type']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)

#--------------SVM--------------
model=SVC()
model.fit(x_train,y_train)
pred=model.predict(x_test)
Acc=accuracy_score(y_test,pred)
recall=recall_score(y_test,pred,average='macro')
presion=precision_score(y_test,pred,average='macro')
class_Report_SVM=classification_report(y_test, pred,target_names=class_name)
Report_SVC={'Report':[Acc,recall,presion],'class_report':class_Report_SVM}
#--------------Decision_Tree_Model--------------
model=DecisionTreeClassifier()
model.fit(x_train,y_train)
pred=model.predict(x_test)
Acc=accuracy_score(y_test,pred)
recall=recall_score(y_test,pred, average='macro')
presion=precision_score(y_test,pred, average='macro')
class_Report_DT=classification_report(y_test, pred,target_names=class_name)
Report_DT={'Report':[Acc,recall,presion],'class_report':class_Report_DT}
#--------------Random_Forest_Model--------------
model=RandomForestClassifier()
model.fit(x_train,y_train)
pred=model.predict(x_test)
Acc=accuracy_score(y_test,pred)
recall=recall_score(y_test,pred, average='macro')
presion=precision_score(y_test,pred, average='macro')
class_Report_RF=classification_report(y_test, pred,target_names=class_name)
Report_RF={'Report':[Acc,recall,presion],'class_report':class_Report_RF}
#--------------Display_Model_ACC--------------
print(f"Classification Report for SVC : {Report_SVC['class_report']} ")
print(f"Classification Report for Decision Tree : {Report_DT['class_report']} ")
print(f"Classification Report for Random Forest : {Report_RF['class_report']} ")
report=pd.DataFrame([Report_SVC['Report'],Report_DT['Report'],Report_RF['Report']],columns=['Accuracy','Recall','Precision'],index=['SVC','Decision Tree','Random Forest'])
print(report.head())
end_time=time.time()
print("==============================================================")
print(f"Time taken to execute the code is {end_time-start_time} seconds")
