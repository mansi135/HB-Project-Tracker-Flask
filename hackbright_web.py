"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/")
def show_homepage():
    """Shows homepage with list of students and projects"""

    students = hackbright.get_all_students()

    projects = hackbright.get_all_projects()

    return render_template("homepage.html", students=students, projects=projects)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    results = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", github=github,
                           first=first, last=last, results=results)


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

    results = hackbright.get_grades_by_title(title)


    return render_template("project_listing.html", title=title,
                            description=description, max_grade=max_grade, results=results)


@app.route("/project-add", methods=['GET'])
def project_add():
    """Display form to add project."""

    return render_template("project_add.html")


@app.route("/project-add", methods=['POST'])
def new_project():
    """Add project to database"""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    return render_template("new_project.html", title=title,
        description=description, max_grade=max_grade)


@app.route("/assign-grade", methods=['GET'])
def assign_grade():
    """Assigns a grade to student"""

    all_students = hackbright.get_all_students()
    
    all_projects = hackbright.get_all_projects()

    return render_template("assign_grade.html", all_students=all_students, all_projects=all_projects)


@app.route("/assign-grade", methods=['POST'])
def update_grade():
    """Adds a grade for student"""

    github = request.form.get("github")

    title = request.form.get("title")

    grade = request.form.get("grade")

    if hackbright.get_grade_by_github_title(github, title):
        hackbright.update_grade(github, title, grade)
    else:
        hackbright.assign_grade(github, title, grade)

    url = '/student?github={}'.format(github)

    return redirect(url)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
