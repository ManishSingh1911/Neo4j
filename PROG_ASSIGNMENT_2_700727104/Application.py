from flask import Flask, request, jsonify
from neo4jInteract import NeoFunc
from neo4j import GraphDatabase

app = Flask(__name__)
apiCalls = NeoFunc()
#Connect to database
try:
    url= "bolt://localhost:7687"
    usr="neo4j"
    pwd="Admin1234"
    graph=GraphDatabase.driver(uri=url,auth=(usr,pwd))
    session = graph.session()
    print("Database connection is established successfully.")
except Exception as e:  
    print(str(e))
    print("Connection to neo4j is failed.")


@app.route('/title', methods=['POST'])
def movieInsertion():
    input_body = request.get_json()
    output = apiCalls.InsertMovieAndShow(input_body,session)
    return jsonify({"Message_Operation": output})

@app.route('/title/<string:fname>', methods=['PATCH'])
def movieUpdating(fname):
    fname = request.view_args['fname']
    input_body = request.get_json()
    output = apiCalls.UpdateMovieAndShow(input_body,session,fname=fname)
    return jsonify({"Message_Operation": output})

@app.route('/title/<string:fname>', methods=['DELETE'])
def movieDeletion(fname):
    fname = request.view_args['fname']
    output = apiCalls.DeleteMovieAndShow(session,fname=fname)
    return jsonify({"Message_Operation": output})

@app.route('/title', methods=['GET'])
def getAllMovieAndShows():
    output = apiCalls.GetMovieAndShows(session)
    return jsonify(output)

@app.route('/title/<string:fname>', methods=['GET'])
def getMoviesAndDetails(fname):
    fname = request.view_args['fname']
    output = apiCalls.GetMovieAndShowDetail(session,fname=fname)
    return jsonify(output)




if __name__ == '__main__':
    app.run()
