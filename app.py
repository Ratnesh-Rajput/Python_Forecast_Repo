
# # WWWWWWWWWWWWWWWWWWWWW
from flask import Flask, request, render_template, jsonify
from flask import Flask, request, jsonify, make_response

import os
import secrets
from ml import run_sarima_model
from db import get_connection, get_hana_dataframe
import pandas as pd
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global flag to track connection status
hana_connection = None

csrf_tokens = {}

@app.route('/test', methods=['GET'])
def handle_csrf():
    # Check if the request is asking for a CSRF token
    if request.headers.get('X-CSRF-Token') == 'Fetch':
        # Generate a CSRF token
        csrf_token = secrets.token_hex(16)  # Generate a secure token
        csrf_tokens[csrf_token] = True  # Store the token (key-value pair)
        
        # Respond with the token in the headers
        response = make_response(jsonify({"message": "CSRF token fetched"}))
        response.headers['X-CSRF-Token'] = csrf_token
        return response
    else:
        return jsonify({"message": "CSRF Token Fetch not requested"}), 400

@app.route('/test', methods=['POST'])
def validate_csrf():
    # Extract CSRF token from the headers
    csrf_token = request.headers.get('X-CSRF-Token')

    # if csrf_token and csrf_token in csrf_tokens:
    #     # Token is valid, process the request
    #     return jsonify({"message": "CSRF token validated successfully"})
    # else:
    #     # Token is missing or invalid
        

    def sarima_forecast():
        try:
            # data = request.get_json()
            # gl_account = data.get('GL_ACCOUNT')
            # description = data.get('DESCRIPTION')
            # profit_ctr = data.get('PROFIT_CTR')
            # company_code = data.get('COMPANY_CODE')

            # if not all([gl_account, description, profit_ctr, company_code]):
            #     return jsonify({"error": "Missing input parameters"}), 400

            result = run_sarima_model("600001", "Income 1", "PC1", "1000")            
            return jsonify(result)  # Return the summary JSON

        except Exception as e:
            print(f"Error in /sarima route: {e}")
            return jsonify({"error": "Server encountered an error"}), 500

    def connect_hana():
        """
        Establish SAP HANA DB connection when requested by the CAP application.
        """
        global hana_connection
        try:
            # # Check if connection already exists
            # if hana_connection:
            #     return jsonify({"message": "Connection to SAP HANA is already established"}), 200
            
            # Establish connection
            hana_connection = get_connection()
        #     if hana_connection:
        #         print("HANA DB Connection Established")
        #         return jsonify({"message": "Successfully connected to SAP HANA"}), 200
        #     else:
        #         return jsonify({"error": "Failed to connect to SAP HANA"}), 500
        except Exception as e:
            print(f"Error in /connect_hana route: {e}")
            return jsonify({"error": "Server encountered an error while connecting to HANA DB"}), 500
    
    connect_hana()
    result = sarima_forecast()
    return result

@app.route('/test')
def test():
    return 'test1'

# @app.route('/sarima', methods=['POST'])
# def sarima_forecast():
#     try:
#         data = request.get_json()
#         gl_account = data.get('GL_ACCOUNT')
#         description = data.get('DESCRIPTION')
#         profit_ctr = data.get('PROFIT_CTR')
#         company_code = data.get('COMPANY_CODE')

#         if not all([gl_account, description, profit_ctr, company_code]):
#             return jsonify({"error": "Missing input parameters"}), 400

#         result = run_sarima_model(gl_account, description, profit_ctr, company_code)

#         if "error" in result:
#             return jsonify({"error": result["error"]}), 400

#         summary = {
#             "Forecast Summary": {
#                 "Start Date": result["dates"][0],
#                 "End Date": result["dates"][-1],
#                 "Forecast Values": [
#                     {"Date": date, "Forecast": forecast, "Lower_CI": lower_ci, "Upper_CI": upper_ci}
#                     for date, forecast, lower_ci, upper_ci in zip(
#                         result["dates"], result["forecast"], result["lower_ci"], result["upper_ci"]
#                     )
#                 ],
#                 "MAPE": result["mape"]  # Include MAPE here
#             }
#         }

        
#         return jsonify(summary)  # Return the summary JSON
#     except Exception as e:
#         print(f"Error in /sarima route: {e}")
#         return jsonify({"error": "Server encountered an error"}), 500


# @app.route('/sarima', methods=['POST'])
# def connect_hana():
#     """
#     Establish SAP HANA DB connection when requested by the CAP application.
#     """
#     global hana_connection
#     try:
#         # Check if connection already exists
#         if hana_connection:
#             return jsonify({"message": "Connection to SAP HANA is already established"}), 200
        
#         # Establish connection
#         hana_connection = get_connection()
#         if hana_connection:
#             print("HANA DB Connection Established")
#             return jsonify({"message": "Successfully connected to SAP HANA"}), 200
#         else:
#             return jsonify({"error": "Failed to connect to SAP HANA"}), 500
#     except Exception as e:
#         print(f"Error in /connect_hana route: {e}")
#         return jsonify({"error": "Server encountered an error while connecting to HANA DB"}), 500

if __name__ == '__main__':
      print('hello')
      app.run(host='0.0.0.0', port=8000)





# 