from flask import Flask, jsonify , request
from dotenv import load_dotenv
from flask_cors import CORS
import pymysql
import os
 

#Install requirements with pip install --upgrade -r requirements.txt 

app = Flask(__name__)
CORS(app)

load_dotenv()


# (╯°□°)╯︵ ┻━┻
# (╯°□°)╯︵ ┻━┻
# (╯°□°)╯︵ ┻━┻
# (╯°□°)╯︵ ┻━┻
# (╯°□°)╯︵ ┻━┻

 


db_host = os.environ['DB_HOST'] 
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name=os.environ['DB_NAME']

db = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

def sqlInj(*values):
    forbidden_symbols = ['@', '!']
    for value in values:
        if any(symbol in str(value) for symbol in forbidden_symbols):
            return True
    return False

 
def matchResult(cId, teams):
    try:
        cursor = db.cursor()
        cursor.execute('SELECT MID FROM matches WHERE CID = %s', (cId,))
        mIds = cursor.fetchall()
        function1 = 'CreateMatch(%s,%s,%s,%s)'
        for mId in mIds:
            for i in range(len(teams)):
                team1 = teams[i]
                for j in range(i + 1, len(teams)):
                    team2 = teams[j]
                    cursor.execute(f"SELECT {function1}", (cId, '', '',''))
                    function2 = 'CreateMatchResult(%s,%s,%s)'
                    cursor.execute(f"SELECT {function2}", (mId, team1, 0))
                    cursor.execute(f"SELECT {function2}", (mId, team2, 0))
                    db.commit()

        return 'Success'
    except db.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Error creating match results: {str(e)}'}), 500

    finally:
        cursor.close()

@app.route('/draw/<int:cId>', methods=['POST'])
def drawChamp(cId):
    try:
        teams = request.json.get('teams', [])

        if not teams:
            return jsonify({'error': 'Teams are NULL'}), 400
 
        results = matchResult(cId, teams)

        return jsonify(results), 200
 
    except Exception as e:
        return jsonify({'error': f'Error creating drawing champ: {str(e)}'}), 500

    finally:
        db.close()




# Get list of all matches and match results 
@app.route('/championship/<int:cId>/matches', methods=['GET'])
def getMatches(cId):
    try:
  
        cursor = db.cursor()
    
        if sqlInj(cId):
            return jsonify({'error': 'Invalid input detected. SQL injection attempt detected.'}), 400

        
        cursor.execute('''
                        SELECT *
                        FROM matches
                        JOIN matchresult ON matches.MID = matchresult.MID
                        WHERE matches.CID = %s;''',(cId,))
        results=cursor.fetchall()
      
        return jsonify(results)
    except db.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Error getting matches: {str(e)}'}), 500

    finally:
        cursor.close()


@app.route('/championship/<int:cId>/matches/<int:mId>', methods=['PUT'])
def updateMatch():
    try:
        mDate = request.json.get('mDate')
        mTime = request.json.get('mTime')
        mLocation = request.json.get('mLocation')

        if sqlInj(mDate, mTime, mLocation):
            return jsonify({'error': 'Invalid input detected. SQL injection attempt detected.'}), 400


        cursor = db.cursor()
        function = 'CreateMatch(%s,%s,%s)'
        cursor.execute(f"SELECT {function}", (mDate, mTime, mLocation))
        db.commit()


        return 'Success'
    except db.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Error updating matches: {str(e)}'}), 500

    finally:
        cursor.close()

@app.route('/championship/<int:cId>/matches/<int:mId>/matchresults/<int:mrId>', methods=['PUT'])
def updateMR(mId, mrId):
    try:
        mrScore = request.json.get('mrScore')
        if sqlInj(mrId, mId, mrScore):
            return jsonify({'error': 'Invalid input detected. SQL injection attempt detected.'}), 400

        cursor = db.cursor()
        function = 'UpdateMR(%s,%s,%s)'
        cursor.execute(f"SELECT {function}", (mrId, mId, mrScore))
        db.commit()

        return 'Success'
    except db.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Error updating matches: {str(e)}'}), 500

    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(port=5005)