from trustedAuthority import app, crypto
from db.connection import get_db_connection
from db.voters import get_user_from_db, get_user_from_id_from_db
from db.candidates import get_candidate_from_db_by_id
from db.votes import set_votes_in_db
from flask import request, jsonify

connection = get_db_connection()

vote_count = 0
nonce = "nonce"


@app.route("/public_key", methods=["GET"])
def public_key():
    return jsonify({"public_key": crypto.public_key})


@app.route("/vote_count", methods=["GET"])
def get_vote_count():
    return jsonify({"vote_count": vote_count})


@app.route("/sign", methods=["POST"])
def sign():
    data = request.json

    # Check if the user is authorized to vote
    user = get_user_from_db(data["username"], connection)
    if not user:
        return jsonify({"message": "User not registered to vote"}), 404

    m1 = data["blinded_vote"]
    s1 = crypto.blind_sign(m1)

    # Increment the vote count - how to handle race conditions?
    global vote_count
    vote_count += 1

    # Create receipt for the user
    receipt_m = hash(str(user["id"]) + nonce)
    receipt = crypto.encrypt_message(receipt_m)

    print(receipt, user["id"], nonce)
    return jsonify({"signed_vote": s1, "receipt": receipt})


@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    user_id = data["user_id"]
    receipt = crypto.decrypt_message(data["receipt"])

    hashed_calc = hash(str(user_id) + nonce)
    print(user_id, receipt, hashed_calc)

    # Check if the user is authorized to vote
    user = get_user_from_id_from_db(user_id, connection)
    if not user or receipt != hashed_calc:
        return jsonify({"message": "Vote not recognized"}), 404

    return jsonify({"message": "Vote verified successfully"})


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
