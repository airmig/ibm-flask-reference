"""
basic reference stub for flask app
flask --app server --debug run --port 3000
"""
from flask import Flask, make_response, request
from data import data

app = Flask(__name__)

@app.route("/")
def home():
    """
    default home page
    """
    response_message = { 'message': 'request received.'}
    return response_message

@app.route("/no_content")
def no_content():
    """
    no content method
    """
    tuple_response = ('No content found')
    return tuple_response

@app.route("/exp")
def index_explicit():
    """
    index explicit
    """
    response = make_response({'message': 'index explicit'})
    response.status_code = 200
    return response

@app.route("/data")
def get_data():
    """
    get data sample
    """
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return {"message": f"Data of length {len(data)} found"}
        # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
        return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404

@app.route("/name_search")
def name_search():
    """
    search dictionary by first name
    """
    name = request.args.get("q")
    print('name received:', name)
    if name is None:
        return {"message": "Invalid input parameters"}, 422
    search_result = None

    for record in data:
        if record.get('first_name').lower() == name.lower():
            search_result = record
            break

    if search_result is None:
        return {"message": "Person not found"}, 404

    return  search_result,400

@app.route("/count")
def count():
    """
    count elements in data
    """
    return {"count": len(data)}

@app.route("/person/<string:uuid>", methods=['GET', 'DELETE'])
def find_by_uuid(uuid):
    """
    find user by uuid
    """
    search_result = None
    for record in data:
        if record.get('id') == uuid:
            search_result = record
            if request.method == 'DELETE':
                data.remove(search_result)
                return {"message": "deleted"}, 200
            break

    if search_result is None:
        return {"message": "not found"}, 404
    return search_result

@app.route('/person',  methods=['POST'])
def add_by_uuid():
    """
    add a person
    """
    new_person = request.get_json()
    if not new_person:
        return {"message": "Invalid input"}, 400

    #validate fields and add to db
    #data.add(new_person)

    return {"message": "Person created"}, 201

@app.errorhandler(404)
def api_not_found(error):
    """
    not found api methods
    """
    return str(error), 404

if __name__ == "__main__":
    app.run(debug=True)
