from trustedAuthority import app, crypto
from db.connection import get_db_connection
from db.voters import get_user_from_db, get_user_from_id_from_db
from db.candidates import get_candidate_from_db_by_id
from db.votes import set_votes_in_db
from db.votepool import set_vote_counted_in_db
from flask import request, jsonify

connection = get_db_connection()

vote_count = 0


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
    receipt = crypto.encrypt_receipt(user["id"])
    return jsonify({"signed_vote": s1, "receipt": receipt})


@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    user_id = crypto.decrypt_receipt(data["receipt"])

    # Check if the user is authorized to vote
    user = get_user_from_id_from_db(user_id, connection)
    if not user:
        return jsonify({"message": "Vote not recognized"}), 404

    return jsonify({"message": "Vote verified successfully"})


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


def count_votes(votes):
    for vote in votes and not vote["counted"]:
        s = vote["signed_vote"]
        vote_id = vote["id"]
        candidate_id = crypto.decrypt_signature(s)

        # Update the votes in the database
        candidate = get_candidate_from_db_by_id(candidate_id, connection)
        set_votes_in_db(candidate["candidate"], connection)
        set_vote_counted_in_db(vote_id, connection)


if __name__ == "__main__":
    app.run(debug=True)
