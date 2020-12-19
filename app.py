
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
import joblib
import pandas as pd
from dateutil.relativedelta import relativedelta
import io
import os
import json
import numpy as np

print('Application has started.')
app = Flask(__name__)
api = Api(app)
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'model.pkl')
model = joblib.load(filename)

class DemoApplication(Resource):
    def post(self):
        print('Into the NEW POST request')

        gender = request.form.get('gender').lower()
        dob = request.form.get('dob')
        is_employed = request.form.get('is_employed').lower()
        income = request.form.get('income')
        amount = request.form.get('amount')
        txn_date = request.form.get('txn_date')

        data = """dob;income;amount;age;gender_MALE;gender_FEMALE;is_employed_YES;is_employed_NO"""
        data = data + '\n' + dob + ';' + income + ';' + amount

        df = pd.read_csv(io.StringIO(data), sep = ";")
        print('Input DataFrame is \n' , df)

        df.dob = pd.to_datetime(df.dob)

        df['age'] = relativedelta(pd.to_datetime('now'), pd.to_datetime(dob)).years

        df = df.drop('dob', axis = 1)

        if gender == 'male':
            df['gender_MALE'] = '1'
            df['gender_FEMALE'] = '0'
        else:
            df['gender_MALE'] = '0'
            df['gender_FEMALE'] = '1'

        if is_employed == 'yes':
            df['is_employed_YES'] = '1'
            df['is_employed_NO'] = '0'
        else:
            df['is_employed_YES'] = '0'
            df['is_employed_NO'] = '1'

        print(df, '\n', df.shape)
        print('DATASET created')
        print(type(model))
        y_pred = model.predict(df)
        print(y_pred)
        y_pred_prob = model.predict_proba(df)
        print(y_pred_prob)

        print('PREDICTION completed')

        df_res = pd.DataFrame(data = y_pred_prob, columns = ["COULD BE FRAUD", "FRAUD", "NORMAL", "SUSPECT"])
        df_res['PREDICTED_STATUS'] = y_pred

        print('RESULT object created')
        response = df_res.to_json()
        print('RESPONSE is\n', response)

        dummy = {
            "PREDICTED_STATUS": np.array_str(y_pred),
            "COULD_BE_FRAUD": df_res["COULD BE FRAUD"][0],
            "FRAUD": df_res["FRAUD"][0],
            "NORMAL": df_res["NORMAL"][0],
            "SUSPECT": df_res["SUSPECT"][0]
        }

        result = json.dumps(dummy)

        return result


api.add_resource(DemoApplication, '/')

if __name__ == '__main__':
    app.run(host='localhost', port=5444, debug=True)
