from trustedAuthority import app, crypto
from db.connection import get_db_connection
from db.voters import get_user_from_db
from db.candidates import get_candidate_from_db_by_id
from db.votes import set_votes_in_db
from flask import request, jsonify

connection = get_db_connection()


@app.route("/public_key", methods=["GET"])
def public_key():
    return jsonify({"public_key": crypto.public_key})


@app.route("/sign", methods=["POST"])
def sign():
    data = request.json

    # Check if the user is authorized to vote
    user = get_user_from_db(data["username"], connection)
    if not user:
        return jsonify({"message": "User not registered to vote"}), 404

    m1 = data["blinded_vote"]
    s1 = crypto.blind_sign(m1)
    return jsonify({"signed_vote": s1})


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    s = data["vote"]
    candidate_id = crypto.decrypt_signature(s)

    # Update the votes in the database
    candidate = get_candidate_from_db_by_id(candidate_id, connection)
    set_votes_in_db(candidate["candidate"], connection)

    return jsonify({"message": "Vote submitted successfully"})


# Sample route to check if API is running
@app.route("/")
def index():
    return jsonify({"message": "API is running"}), 200


if __name__ == "__main__":
    app.run(debug=True)
