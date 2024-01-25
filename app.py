from flask import Flask, render_template, request, jsonify
import subprocess

import pandas as pd
import numpy
import pandas as pd
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler, StandardScaler, OneHotEncoder

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


df = pd.read_csv("https://raw.githubusercontent.com/jamshid-ds/Bank-Term-Deposit-Predictions/main/dataset/train.csv")
df.y = df.y.replace("no",0).replace("yes",1)
df.marital = df.marital.replace("married",1).replace('single',0).replace('divorced',2)
df.default = df.default.replace(['no','yes'],[0,1])
df.housing = df.housing.replace(['no','yes'],[0,1])
df.laon = df.loan.replace(['no','yes'],[0,1])   

x = df.drop('y',axis=1)
y = df['y']

nums = []
cats = []

for h in list(x.columns):
  if df[h].dtype == 'int64':
    nums.append(h)
  else:
    cats.append(h)
#Agar ustun sonli bo'lsa nums listiga, agar aksincha bo'lsa cats ustuniga qo'shiladi


#Sonli ustunlar uchun pipeline
nums_pipeline = Pipeline([
    ('st_scaler', StandardScaler()),
    ('minmaxscaler', MinMaxScaler())
])

#Satrli ustunlar uchun pipeline
cats_pipeline = Pipeline([
    ("O_Encoder", OrdinalEncoder())

])

#umumiy transformer
full_pipeline = ColumnTransformer([
    ('nums', nums_pipeline, nums),
    ('cats', cats_pipeline, cats),
])

x_pre = full_pipeline.fit_transform(x)

dt_model = DecisionTreeClassifier()
dt_model.fit(x_pre,y)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_function', methods=['POST'])
def run_function():
    data = request.json
    age = data['age']
    job = data['job']
    marital = data['marital']
    education = data['education']
    balance = data['balance']
    housing = data['housing']
    loan = data['loan']
    contact = data['contact']
    day = data['day']
    month = data['month']
    duration = data['duration']

    result = run_ipynb_function(age, job, marital, education, balance, housing, loan, contact, day, month, duration)  # Implement this function

    return jsonify({'result': result})

def run_ipynb_function(age, job, marital, education, balance, housing, loan, contact, day, month, duration):
  dataf = pd.DataFrame()
  dataf["age"] = age,
  dataf['job'] = job,
  dataf['marital'] = marital,
  dataf["education"] = education,
  dataf["default"] = 0,
  dataf["balance"] = balance,
  dataf["housing"] = housing,
  dataf["loan"] = loan,
  dataf["contact"] = contact
  dataf['day'] = day
  dataf['month'] = month
  dataf['duration'] = duration
  dataf['campaign'] = 1
  dataf['pdays'] = -1
  dataf['previous'] = -1
  dataf['poutcome'] = 'unknown'

  dataf_pre = full_pipeline.transform(dataf)
  a = dt_model.predict(dataf_pre)
  return a[0]

if __name__ == '__main__':
    app.run(debug=True)

