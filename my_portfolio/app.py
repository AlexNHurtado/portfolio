"""
This Flask application serves as a personal portfolio website with the following features:
- Display skills, languages, experiences, projects, and personal information.
- User authentication and authorization using Flask-Login.
- Admin interface to manage skills, languages, experiences, projects, and personal information.
Routes:
- /: Home page displaying skills, languages, and experiences.
- /projects: Page displaying projects.
- /about: Page displaying personal information.
- /contact: Contact form page.
- /login: User login page.
- /logout: User logout route.
- /admin/skills: Admin page to manage skills.
- /admin/languages: Admin page to manage languages.
- /admin/addlanguage: Route to add a new language.
- /admin/deletelanguage: Route to delete a language.
- /admin/updatelanguage: Route to update a language.
- /admin/experience: Admin page to manage experiences.
- /admin/addexperience: Route to add a new experience.
- /admin/deleteexperience: Route to delete an experience.
- /admin/updateexperience: Route to update an experience.
- /admin/projects: Admin page to manage projects.
- /admin/addproject: Route to add a new project.
- /admin/deleteproject: Route to delete a project.
- /admin/updateproject: Route to update a project.
- /admin/about: Admin page to manage personal information.
- /admin/updateabout: Route to update personal information.
- /admin/addskills: Route to add new skills.
- /admin/deleteskill/<skill>: Route to delete a skill.
- /admin/updateskill: Route to update a skill.
Models:
- User: Represents a user with fields for id, username, and password.
Configuration:
- SQLALCHEMY_DATABASE_URI: Database URI for SQLAlchemy.
- SECRET_KEY: Secret key for session management.
- SQLALCHEMY_TRACK_MODIFICATIONS: Disable modification tracking for SQLAlchemy.
Initialization:
- Initializes Flask app, SQLAlchemy, and Flask-Login.
- Creates the 'user' table if it doesn't exist.
- Adds a default admin user if it doesn't exist.
Usage:
- Run the application with `python app.py`.
- Access the admin interface to manage portfolio content.
"""


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/postgres'
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False)
    position = db.Column(db.String(250), nullable=False)
    dates = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(250), nullable=True)


class AboutMe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    university = db.Column(db.String(250), nullable=False)
    degree = db.Column(db.String(250), nullable=False)
    year = db.Column(db.String(250), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    hobbies = db.Column(db.String(250), nullable=False)
    goals = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(250), nullable=False)
    linkedin = db.Column(db.String(250), nullable=False)
    github = db.Column(db.String(250), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


skills = {
    'Programming': ['Python', 'Java', 'C++', 'JavaScript', 'HTML', 'CSS'],
    'Frameworks': ['Flask', 'Django', 'React', 'Angular'],
    'Databases': ['MySQL', 'PostgreSQL', 'SQLite', 'MongoDB'],
    'Tools': ['Git', 'Docker', 'Jenkins', 'Jira', 'Confluence'],
    'Cloud': ['AWS', 'Azure', 'Google Cloud'],
}
languages = ['English', 'Spanish', 'French', 'German', 'Italian']

experiences = {
    'company1': {
        'name': 'Company 1',
        'position': 'Software Engineer',
        'dates': 'Jan 2019 - Present',
        'description': 'This is a job description.'},
    'company2': {
        'name': 'Company 2',
        'position': 'Software Engineer',
        'dates': 'Jan 2017 - Dec 2018',
        'description': 'This is a job description.'},
}
my_projects = {
    'project1': {
        'name': 'Project 1',
        'description': 'This is a project description.',
        'technologies': ['Python', 'Flask', 'MySQL'],
        'link': '#'
    },
    'project2': {
        'name': 'Project 2',
        'description': 'This is a project description.',
        'technologies': ['Python', 'Django', 'PostgreSQL'],
        'link': '#'
    },
}
about_me = {
    "name": "Alex Hurtado",
    "age": 21,
    "university": "University of Technology",
    "degree": "Bachelor of Computer Science",
    "year": "3rd Year",
    "bio": "I am a passionate computer science student with a keen interest in web development, artificial intelligence, and data science. I love learning new technologies and applying them to solve real-world problems.",
    "hobbies": ["Coding", "Reading", "Gaming", "Hiking"],
    "goals": "To become a full-stack developer and contribute to open-source projects.",
    "contact": {
        "email": "alex.hurtado@example.com",
        "phone": "123-456-7890",
        "linkedin": "https://www.linkedin.com/in/example",
        "github": "https://github.com/example"
    }
}


@app.route('/')
def index():
    message = request.args.get('message', '')

    return render_template('index.html', message=message, skills=skills, languages=languages, experience=experiences)


@app.route('/projects')
def projects():

    return render_template('projects.html', message=request.args.get('message', ''), my_projects=my_projects)


@app.route('/about')
def about():
    return render_template('about.html', message=request.args.get('message', ''), about_me=about_me)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']
            # Process the form data here
            return redirect(url_for('index', message='Thank you for your message!'))
        except KeyError as e:
            # Handle missing form data
            return redirect(url_for('index', message='Something Went Wrong! (400)'))
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user is None or user.password != password:
                return redirect(url_for('login', message='Invalid Credentials!'))
            else:
                if user.password == password:
                    login_user(user)
                else:
                    return redirect(url_for('login', message='Invalid Credentials!'))
                return redirect(url_for('admin_skills', message='Welcome, ' + username + '!'))
        except KeyError as e:
            return redirect(url_for('login', message='Something Went Wrong! (400)'))
    return render_template('login.html', message=request.args.get('message', ''))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index', message='You have been logged out!'))


@app.route('/admin/skills')
@login_required
def admin_skills():
    return render_template('admin-skills.html', message=request.args.get('message', ''),  skills=skills, languages=languages, experiences=experiences)


@app.route('/admin/languages')
@login_required
def admin_language():
    return render_template('admin-language.html', message=request.args.get('message', ''), languages=languages)


@app.route('/admin/addlanguage', methods=['POST'])
@login_required
def add_language():
    try:
        language = request.form['language_name']
        languages.append(language)
        return redirect(url_for('admin_language', message='Language added successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_language', message='Something Went Wrong! (400)'))


@app.route('/admin/deletelanguage', methods=['POST'])
@login_required
def delete_language():
    try:
        languages.pop(int(request.form['index']))
        return redirect(url_for('admin_language', message='Language deleted successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_language', message='Something Went Wrong! (400)'))


@app.route('/admin/updatelanguage', methods=['POST'])
@login_required
def update_language():
    try:
        language = request.form['language_name']
        index = request.form['index']
        languages[int(index)] = language
        return redirect(url_for('admin_language', message='Language updated successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_language', message=f'Something Went Wrong! ({e})'))


@app.route('/admin/experience')
@login_required
def admin_experience():
    return render_template('admin-experience.html', message=request.args.get('message', ''), experience=experiences)


@app.route('/admin/addexperience', methods=['POST'])
@login_required
def add_experience():
    try:
        title = request.form['experience_title']
        company_name = request.form['experience_company']
        position = request.form['experience_position']
        dates = request.form['experience_start_date'] + \
            ' - ' + request.form['experience_end_date']
        description = request.form['experience_description']
        experience = {}
        experience[title] = {
            'name': company_name,
            'position': position,
            'dates': dates,
            'description': description
        }
        experiences.update(experience)
        return redirect(url_for('admin_experience', message='Experience added successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_experience', message=f'Something Went Wrong! ({e})'))


@app.route('/admin/deleteexperience', methods=['POST'])
@login_required
def delete_experience():
    try:
        position = request.form['old_experience_title']
        experiences.pop(position)
        return redirect(url_for('admin_experience', message='Experience deleted successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_experience', message=f'Something Went Wrong! ({e})'))


@app.route('/admin/updateexperience', methods=['POST'])
@login_required
def update_experience():
    try:
        old_title = request.form['old_experience_title']
        title = request.form['experience_title']
        company_name = request.form['name']
        position = request.form['position']
        dates = request.form['dates']
        description = request.form['description']
        experience = {}
        experience[title] = {
            'name': company_name,
            'position': position,
            'dates': dates,
            'description': description
        }
        experiences.pop(old_title)
        experiences.update(experience)
        return redirect(url_for('admin_experience', message='Experience updated successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_experience', message=f'Something Went Wrong! ({e})'))


@app.route('/admin/projects')
@login_required
def admin_projects():
    return render_template('admin-projects.html', message=request.args.get('message', ''), projects=my_projects)


@app.route('/admin/addproject', methods=['POST'])
@login_required
def add_project():
    try:

        project_name = request.form['project_name']
        project_description = request.form['project_description']
        project_technologies = request.form['project_tech'].split(',')
        project_link = request.form['project_link']
        project = {}
        project[project_name] = {
            'name': project_name,
            'description': project_description,
            'technologies': project_technologies,
            'link': project_link
        }
        my_projects.update(project)
        return redirect(url_for('admin_projects', message='Project added successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_projects', message=f'Something Went Wrong! ({e})'))


@app.route('/admin/deleteproject', methods=['POST'])
@login_required
def delete_project():
    try:
        project = request.form['old_project_name']
        my_projects.pop(project)
        return redirect(url_for('admin_projects', message='Project deleted successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_projects', message='Something Went Wrong! (400)'))


@app.route('/admin/updateproject', methods=['POST'])
@login_required
def update_project():
    try:
        old_project_name = request.form.get('old_project_name')
        project_name = request.form.get('project_name')
        project_description = request.form.get('project_description')
        project_technologies = request.form.get('project_tech', '').split(',')
        project_link = request.form.get('project_link')
        project = {}
        project[project_name] = {
            'name': project_name,
            'description': project_description,
            'technologies': project_technologies,
            'link': project_link
        }
        my_projects.pop(old_project_name, None)
        my_projects.update(project)
        return redirect(url_for('admin_projects', message='Project updated successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_projects', message='Something Went Wrong! (400)'))


@app.route('/admin/about')
@login_required
def admin_about():
    return render_template('admin-about.html', message=request.args.get('message', ''), about_me=about_me)


@app.route('/admin/updateabout', methods=['POST'])
@login_required
def update_about():

    try:
        about_me['name'] = request.form['name']
        about_me['age'] = request.form['age']
        about_me['university'] = request.form['university']
        about_me['degree'] = request.form['degree']
        about_me['year'] = request.form['year']
        about_me['bio'] = request.form['bio']
        about_me['hobbies'] = request.form['hobbies'].split(',')
        about_me['goals'] = request.form['goals']
        about_me['contact']['email'] = request.form['email']
        about_me['contact']['phone'] = request.form['phone']
        about_me['contact']['linkedin'] = request.form['linkedin']
        about_me['contact']['github'] = request.form['github']
        return redirect(url_for('admin_about', message='About Me updated successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_about', message='Something Went Wrong! (400)'))


@app.route('/admin/addskills', methods=['POST'])
@login_required
def add_skill():
    try:
        skill_name = request.form['skill_name']
        skill_details = request.form['skill_details']
        skill_details_list = skill_details.split('\n')
        # Add the new skill to the appropriate category
        # For example, adding to the 'Programming' category
        if skill_name in skills:
            skills[skill_name].extend(skill_details_list)
        else:
            skills[skill_name] = skill_details_list
        return redirect(url_for('admin_skills', message='Skill added successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_skills', message='Something Went Wrong! (400)'))


@app.route('/admin/deleteskill/<skill>', methods=['POST'])
@login_required
def delete_skill(skill):
    try:
        # Remove the skill from the appropriate category
        if skill in skills:
            skills.pop(skill)
        return redirect(url_for('admin_skills', message='Skill deleted successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_skills', message='Something Went Wrong! (400)'))


@app.route('/admin/updateskill', methods=['POST'])
@login_required
def update_skill():
    try:
        skill_name = request.form['skill_name']
        skill_details = request.form.getlist('skill_details')

        skills[skill_name] = skill_details

        return redirect(url_for('admin_skills', message='Skill updated successfully!'))
    except KeyError as e:
        return redirect(url_for('admin_skills', message=f'Something Went Wrong! (400)'))


if __name__ == '__main__':

    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('user'):
            db.create_all()

        # Check if the user already exists before adding
        if not User.query.filter_by(username='admin').first():
            new_user = User(username='admin', password='admin')
            db.session.add(new_user)
            db.session.commit()
        users = User.query.all()
        for user in users:
            print(
                f'ID: {user.id}, Username: {user.username}, Password: {user.password}')

    app.run(debug=True)
