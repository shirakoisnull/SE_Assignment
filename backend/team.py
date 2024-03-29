from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS
import pymysql
import os

# Install requirements with pip install --upgrade -r requirements.txt

app = Flask(__name__)
CORS(app)

load_dotenv()

db_host = os.environ["DB_HOST"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]

db = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

# Checking for SQL injections, basically if characters @ and ! in returned values
def sqlInj(*values):
    forbidden_symbols = ["@", "!"]
    for value in values:
        if any(symbol in str(value) for symbol in forbidden_symbols):
            return True
    return False



# Get list of all teams, returns TID, name, city, wins, losses in this order.
 
@app.route("/teams", methods=["GET"])
def getTeams():
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM team")
            results = cursor.fetchall()
        

    except Exception as e:
        return jsonify({"error": f"Error getting teams: {str(e)}"}), 500

  
        
    return jsonify(results), 200


# Create new team
@app.route("/teams", methods=["POST"])
def createTeam():
    try:
        # Requesting variables
        tName = request.json.get("tName")
        tCity = request.json.get("tCity")
        tWins = request.json.get("tWins")
        tLosses = request.json.get("tLosses")

        if sqlInj(tName, tCity, tWins, tLosses):
            return (
                jsonify(
                    {"error": "Invalid input detected. SQL injection attempt detected."}
                ),
                400,
            )
        # Calling function for creating team.
        with db.cursor() as cursor:
            function = "CreateTeam(%s, %s, %s, %s)"
            cursor.execute(f"SELECT {function}", (tName, tCity, tWins, tLosses))
            db.commit()
       
    except Exception as e:
        return jsonify({"error": f"Error creating team: {str(e)}"}), 500
 
        
    return "Success\n", 201


# Update selected team
@app.route("/teams/<int:tId>", methods=["PUT"])
def updateTeam(tId):
    try:
        # Requesting variables
        tName = request.json.get("tName")
        tCity = request.json.get("tCity")
        tWins = request.json.get("tWins")
        tLosses = request.json.get("tLosses")
     

        if sqlInj(tName, tCity, tWins, tLosses, tId):
            return (
                jsonify(
                    {"error": "Invalid input detected. SQL injection attempt detected."}
                ),
                400,
            )
        # Calling function for updating team
        with db.cursor() as cursor:
            function = "UpdateTeam(%s, %s, %s, %s, %s)"
            cursor.execute(f"SELECT {function}", (tId, tName, tCity, tWins, tLosses))
            db.commit()
        

    except Exception as e:
        return jsonify({"error": f"Error updating team: {str(e)}"}), 500

 
        
    return "Success\n", 200


# Get specific team based on TID
@app.route("/teams/<int:tId>", methods=["GET"])
def getTeam(tId):
    try:
    

        if sqlInj(tId):
            return (
                jsonify(
                    {"error": "Invalid input detected. SQL injection attempt detected."}
                ),
                400,
            )

        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM team WHERE TID = %s", (tId))
            result = cursor.fetchone()
        

    except Exception as e:
        return jsonify({"error": f"Error viewing team: {str(e)}"}), 500

  
       
    return jsonify(result), 200


# Delete selected team
@app.route("/teams/<int:tId>", methods=["DELETE"])
def deleteTeam(tId):
    try:
        # Checking for SQL injection symbols
        if sqlInj(tId):
            return (
                jsonify(
                    {"error": "Invalid input detected. SQL injection attempt detected."}
                ),
                400,
            )

        with db.cursor() as cursor:
            function = "DeleteTeam(%s)"
            cursor.execute(f"SELECT {function}", (tId,))
            db.commit()
   

    except Exception as e:
        return jsonify({"error": f"Error deleting team: {str(e)}"}), 500

 
        
    return "Success\n", 200


if __name__ == "__main__":
    app.run(port=5003)
