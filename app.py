from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = '1234'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

courses = [
    {
        'id': 1,
        'name': 'Robotics Development and Automation (RDA)',
        'description': 'Learn the fundamentals of robotics, automation, and control systems.',
        'requirements': ['Laptop with a minimum of 8Gb of RAM Running windows 10 or 11','High School Diploma or equivalent (WAEC,NECO,NABTEB)','Basic understanding of Mathematics (algebra, geometry, and trigonometry)'],
        'duration': '6 months',
        'cost': '₦230,000',
        'image': 'robotics.jpeg' 
    },
    {
        'id': 2,
        'name': 'Artificial Intelligence and Machine Learning (AIML)',
        'description': 'Explore the basics of AI, machine learning, and their applications.',
        'requirements': ['Laptop with a minimum of 8Gb of RAM Running windows 10 or 11','High School Diploma or equivalent (WAEC,NECO,NABTEB)','Basic understanding of Mathematics (algebra, geometry, and trigonometry)'],
        'duration': '6 months',
        'cost': '₦200,000',
        'image': 'ai.jpeg'  
    },
    {
        'id': 3,
        'name': 'Data Science and Analytics (DSA)',
        'requirements': ['Laptop with a minimum of 8Gb of RAM Running windows 10 or 11','High School Diploma or equivalent (WAEC,NECO,NABTEB)','Basic understanding of Mathematics (algebra, geometry, and trigonometry)'],
        'description': 'Master data science techniques and analytical skills for real-world data.',
        'duration': '6 months',
        'cost': '₦200,000',
        'image': 'data_science.jpg' 
    },
    {
        'id': 4,
        'name': 'App Development (AD)',
        'requirements': ['Laptop with a minimum of 8Gb of RAM Running windows 10 or 11','High School Diploma or equivalent (WAEC,NECO,NABTEB)','Basic understanding of Mathematics (algebra, geometry, and trigonometry)'],
        'description': 'Learn to design and develop mobile and web applications.',
        'duration': '6 months',
        'cost': '₦200,000',
        'image': 'app.avif'  
    }
]


@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    return response

class User(UserMixin):
    def __init__(self, id):
        self.id = id

ADMIN_USERNAME = 'prime'
ADMIN_PASSWORD = 'prime'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def get_db_connection():
    conn = sqlite3.connect('stem_courses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html', courses=courses)

@app.route('/about')
def about():
    return render_template('about.html', courses=courses)

@app.route('/contact')
def contact():
    return render_template('contact.html', courses=courses)

@app.route('/course/<int:course_id>')
def course_details(course_id):
    course = next((course for course in courses if course['id'] == course_id), None)
    if course:
        return render_template('course_details.html', course=course)
    return "Course not found", 404

@app.route('/courses')
def courses_list():
    return render_template('courses_list.html', courses=courses)


@app.route('/register/<int:course_id>', methods=['GET', 'POST'])
def register(course_id):
    course = next((course for course in courses if course['id'] == course_id), None)
    if not course:
        return "Course not found", 404
    
    if request.method == 'POST':

        surname = request.form.get('surname')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        personal_phone = request.form.get('personal_phone')
        sponsor_phone = request.form.get('sponsor_phone')
        email = request.form.get('email')

        conn = get_db_connection()
        conn.execute('INSERT INTO students (surname, first_name, last_name, address, personal_phone, sponsor_phone, email, course) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                     (surname, first_name, last_name, address, personal_phone, sponsor_phone, email, course['name']))
        conn.commit()
        conn.close()

        flash(f'Successfully registered for {course["name"]}')
        return redirect(url_for('home'))

    return render_template('register.html', course=course)


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            user = User(id=username)
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('students'))

        flash('Invalid credentials, please try again.')

    return render_template('admin_login.html')


@app.route('/students')
@login_required
def students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    
    return render_template('students.html', students=students)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
