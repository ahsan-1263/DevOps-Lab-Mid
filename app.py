
from flask import Flask, render_template, request, redirect, url_for, flash
from urllib.parse import urlparse

from database import (
    initialize_database,
    save_submission,
    get_all_submissions
)

app = Flask(__name__)
app.secret_key = "devops-lab-secret-key"

initialize_database()


def is_valid_url(url):
    """Check whether the URL has a valid HTTP or HTTPS format."""
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
            and "." in parsed.netloc
        )
    except ValueError:
        return False


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        student_name = request.form.get("student_name", "").strip()
        registration_number = request.form.get(
            "registration_number", ""
        ).strip()
        assignment_title = request.form.get(
            "assignment_title", ""
        ).strip()
        submission_url = request.form.get(
            "submission_url", ""
        ).strip()

        if not all([
            student_name,
            registration_number,
            assignment_title,
            submission_url
        ]):
            flash("All fields are required!", "error")
            return redirect(url_for("home"))

        if not is_valid_url(submission_url):
            flash("Please enter a valid HTTP or HTTPS URL!", "error")
            return redirect(url_for("home"))

        save_submission(
            student_name,
            registration_number,
            assignment_title,
            submission_url
        )

        flash("Assignment submitted successfully!", "success")
        return redirect(url_for("home"))

    submissions = get_all_submissions()

    return render_template(
        "index.html",
        submissions=submissions
    )


if __name__ == "__main__":
    app.run(debug=True)
