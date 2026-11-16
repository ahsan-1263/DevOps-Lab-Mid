
import requests
import json
import sys
from datetime import datetime, timezone


RECEIVER_URL = "http://127.0.0.1:5001/report"


def send_report(report):

    try:
        response = requests.post(
            RECEIVER_URL,
            json=report,
            timeout=10
        )

        print("HTTP Status:", response.status_code)
        print("Receiver Response:", response.text)

        response.raise_for_status()

        return True

    except requests.RequestException as error:
        print("Failed to send report:", error)
        return False


if __name__ == "__main__":

    sample_report = {
        "repository": "DevOps-Lab-Mid",
        "branch": "main",
        "commit_sha": "local-test-commit",
        "run_id": "local-test-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "tests": [
            {
                "name": "test_valid_submission_is_saved",
                "result": "PASSED",
                "failure_message": None
            },
            {
                "name": "test_missing_registration_number_is_rejected",
                "result": "PASSED",
                "failure_message": None
            },
            {
                "name": "test_invalid_url_is_rejected",
                "result": "PASSED",
                "failure_message": None
            }
        ],

        "total": 3,
        "passed": 3,
        "failed": 0,
        "status": "PASSED"
    }

    success = send_report(sample_report)

    if not success:
        sys.exit(1)
