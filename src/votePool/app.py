from services import add_vote, authenticate_JWT, data_migrate, get_count
from backup import start_backup_task
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/vote_count", methods=["GET"])
def get_vote_count():
    vote_count = get_count()
    return jsonify({"vote_count": vote_count})


@app.route("/vote_pool/vote_submit", methods=["POST"])
def vote_submit():
    try:
        data = request.json
        id = data["id"]
        vote = data["signed_vote"]
        status = add_vote(id, vote)

        if status:
            return jsonify({"message": "Vote Added Successfully"}), 200
        else:
            return jsonify({"message": "Error Adding the vote"}), 400

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500


@app.route("/migrate_votes", methods=["POST"])
def migrate_votes():
    try:
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized",
            }, 401

        status = authenticate_JWT(token)

        if status:
            migration_status = data_migrate()
            if migration_status:
                return jsonify({"message": "Votes Migrated Successfully"}), 200
            else:
                return jsonify({"message": "Votes Migration Unsuccessful"}), 409
        else:
            return jsonify({"message": "Unauthorized"}), 401

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500


# Sample route to check if API is running
@app.route("/")
def index():
    return jsonify({"message": "API is running well"}), 200


if __name__ == "__main__":
    start_backup_task()
    app.run(debug=True, port=5001)
