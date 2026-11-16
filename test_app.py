
import pytest

import database
import app as app_module


@pytest.fixture
def client(tmp_path):
    # Use a separate temporary database for every test
    database.DATABASE_NAME = str(tmp_path / "test_submissions.db")
    database.initialize_database()

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client


def test_valid_submission_is_saved(client):
    response = client.post("/", data={
        "student_name": "Ali",
        "registration_number": "FA24-020",
        "assignment_title": "DevOps Lab",
        "submission_url": "https://github.com/"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Assignment submitted successfully!" in response.data

    submissions = database.get_all_submissions()

    assert len(submissions) == 1
    assert submissions[0]["student_name"] == "Ali"
    assert submissions[0]["registration_number"] == "FA24-020"


def test_missing_registration_number_is_rejected(client):
    response = client.post("/", data={
        "student_name": "Ali",
        "registration_number": "",
        "assignment_title": "DevOps Lab",
        "submission_url": "https://github.com/"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"All fields are required!" in response.data
    assert len(database.get_all_submissions()) == 0


def test_invalid_url_is_rejected(client):
    response = client.post("/", data={
        "student_name": "Ali",
        "registration_number": "FA24-020",
        "assignment_title": "DevOps Lab",
        "submission_url": "not-a-valid-url"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Please enter a valid HTTP or HTTPS URL!" in response.data
    assert len(database.get_all_submissions()) == 0
