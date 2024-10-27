from functools import wraps
from trustedAuthority import app, crypto
from db.connection import get_db_connection
from db.voters import get_user_from_db, get_user_from_id_from_db
from db.candidates import get_candidate_from_db_by_id
from db.votes import set_votes_in_db
from trustedAuthority.trustedAuthority_votePool import (
    set_vote_counted_in_db,
    get_vote_pool,
)
from flask import request, jsonify
from flask import request, jsonify, current_app
import jwt


connection = get_db_connection()


@app.route("/vote_count", methods=["POST"])
def count_votes():
    votes = get_vote_pool(connection)
    for vote in votes:
        if vote["counted"]:
            continue
        s = vote["signed_vote"]
        vote_id = vote["id"]
        candidate_id = crypto.decrypt_signature(s)

        # Update the votes in the database
        candidate = get_candidate_from_db_by_id(candidate_id, connection)
        set_votes_in_db(candidate["candidate"], connection)
        set_vote_counted_in_db(vote_id, connection)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized",
            }, 401

        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = get_user_from_id_from_db(data["user_id"], connection)
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized",
                }, 401

            return f(current_user, *args, **kwargs)
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
            }, 500

    return decorated


@app.route("/public_key", methods=["GET"])
def public_key():
    return jsonify({"public_key": crypto.public_key})


@app.route("/get_token", methods=["POST"])
def get_token():
    data = request.json
    print(data)
    if data["username"] == "admin" and data["password"] == "admin":
        try:
            token = jwt.encode(
                {"user_id": 0},
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            )

            return jsonify({"token": token})

        except Exception as e:
            print(e)
            return jsonify({"message": str(e)}), 500

    user = get_user_from_db(data["username"], connection)

    if not user:
        return jsonify({"message": "User not registered"}), 404

    try:
        token = jwt.encode(
            {"user_id": user["id"]},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        return jsonify({"token": token})

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500


@app.route("/sign", methods=["POST"])
@token_required
def sign(current_user):
    data = request.json

    # Check if the user is authorized to vote
    if not current_user:
        return jsonify({"message": "User not registered to vote"}), 404

    m1 = data["blinded_vote"]
    s1 = crypto.blind_sign(m1)

    # Create receipt for the user
    receipt = crypto.encrypt_receipt(current_user["id"])
    return jsonify({"signed_vote": s1, "receipt": receipt})


@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    user_id = crypto.decrypt_receipt(data["receipt"])
    print(user_id)
    # Check if the user is authorized to vote
    user = get_user_from_id_from_db(user_id, connection)
    if not user:
        return jsonify({"message": "Vote not recognized"}), 404

    return jsonify({"message": "Vote verified successfully"})


# Needs to be modified to use third party API introduced by @Nusal
@app.route("/vote_submit", methods=["POST"])
def vote_submit():
    try:
        data = request.json
        votes = data["votes"]
        count_votes(votes)

        return jsonify({"message": "Vote Counting finished"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500


# Sample route to check if API is running
@app.route("/")
def index():
    return jsonify({"message": "API is running"}), 200


if __name__ == "__main__":
    app.run(debug=True)
