import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('Housing.csv')
le = LabelEncoder()
df['mainroad']= le.fit_transform(df["mainroad"])
df['furnishingstatus'] = le.fit_transform(df["furnishingstatus"])
df['basement'] = le.fit_transform(df["basement"])
df['hotwaterheating'] = le.fit_transform(df["hotwaterheating"])
df['airconditioning'] = le.fit_transform(df["airconditioning"])
df['prefarea'] = le.fit_transform(df["prefarea"])
df['guestroom'] = le.fit_transform(df["guestroom"])

X= df.drop('price', axis=1).values
Y= df['price'].values

bias = 0.01
a= 0.00001
theta = [0.001] * 13
prediction=0
error=0
sum=0


def predict (thetas, features):
    predict= thetas[0]
    for j in range(len(features)):
        predict += thetas[j+1] * features[j]
    return predict


features = 12
for epochs in range(5):
    for i in range(len(Y)):
        prediction = predict(theta, X[i])
        error = prediction - Y[i]
        theta[0] += -a * (1/len(X)) * error
        for j in range(features):
            theta[j+1]+= - a * (1/len(X)) * (error * X[i][j]) 



newdata = input("enter data: ").split(",")
newdata = [float(x) for x in newdata] 
print("Prediction: ",predict(theta, newdata))
print("Error: ",error )










