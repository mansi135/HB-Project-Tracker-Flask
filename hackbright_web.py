"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    results = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", github=github,
                           first=first, last=last, results=results)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add():
    """Display form to add student."""

    return render_template("student_add.html")


@app.route("/new-student", methods=['POST'])
def new_student():
    """Add student to database"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("new_student.html", first_name=first_name,
                           last_name=last_name, github=github)


@app.route("/project-search")
def get_project_form():
    """Show form for searching for a project."""

    return render_template("project_search.html")

@app.route("/project")
def show_project_listing():
    """Shows info about project"""

    title = request.args.get('title')

    title, description, max_grade = hackbright.get_project_by_title(title)

    return render_template("project_listing.html", title=title,
                            description=description, max_grade=max_grade)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
