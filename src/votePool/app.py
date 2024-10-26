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
        vote = data["signed_vote"]
        status = add_vote(vote)

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
        data = request.json
        token = data["signed_vote"]
        status = authenticate_JWT(token)

        if status:
            data_migrate()
            return jsonify({"message": "Votes Migrated Successfully"}), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500

# Sample route to check if API is running
@app.route("/")
def index():
    return jsonify({"message": "API is running"}), 200

if __name__ == "__main__":
    start_backup_task()
    app.run(debug=True)
