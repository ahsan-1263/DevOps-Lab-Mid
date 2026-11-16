
from flask import Flask, request, jsonify
from pathlib import Path
import json
from datetime import datetime, timezone

app = Flask(__name__)

REPORT_FOLDER = Path(__file__).parent / "reports"
REPORT_FOLDER.mkdir(exist_ok=True)

REPORT_FILE = REPORT_FOLDER / "test-report.json"


@app.route("/report", methods=["POST"])
def receive_report():

    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({
            "error": "Invalid JSON report"
        }), 400

    required_fields = [
        "repository",
        "branch",
        "commit_sha",
        "run_id",
        "timestamp",
        "tests",
        "total",
        "passed",
        "failed",
        "status"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in report
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing fields",
            "fields": missing_fields
        }), 400

    report["received_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return jsonify({
        "message": "Test report received successfully",
        "file": str(REPORT_FILE)
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "Receiver is running"
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
