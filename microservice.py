from uuid import uuid4
from flask import Flask, request, jsonify
from pydblite import Base

app = Flask(__name__)

app.user_db = Base('user.pdl')

if app.user_db.exists():
    app.user_db.open()
else:
    app.user_db.create('id', 'first_name', 'last_name')


@app.route('/users', methods=["POST"])
def post_user():
    body = request.json
    first_name = body.get("first_name")
    last_name = body.get("last_name")
    if not first_name or not last_name:
        return jsonify({"status": "failure",
                        "result": {
                            "reason": "Invalid user name"
                        }})
    if app.user_db(first_name=first_name, last_name=last_name):
        return jsonify({"status": "failure",
                        "result": {
                            "reason": "User is existing"
                        }})
    uuid = uuid4()
    app.user_db.insert(uuid, first_name, last_name)
    app.user_db.commit()
    return jsonify({
        "status": "success",
        "result": {
            "id": uuid
        }
    })


@app.route('/users/<user_id>', methods=["POST"])
def post_userid(user_id):
    body = request.json
    command = body.get("command")
    if not command:
        return jsonify({"status": "failure",
                        "result": {
                            "reason": "Invalid request"
                        }})

    users = app.user_db(id=user_id)
    if not users:
        return jsonify({"status": "failure",
                        "result": {
                            "reason": f"User id {user_id} is not existing"
                        }})
    user = users[0]
    return jsonify({
        "status": "success",
        "result": {
            "user": {
                "id": user["id"],
                "first_name": user["first_name"],
                "last_name": user["last_name"]
            },
            "greeting": "Hello, World!"
        }
    }
    )


app.run()
