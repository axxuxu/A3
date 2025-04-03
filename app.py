from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'b3a4d71f7cd54d2b95f749e3b7fa7a34'

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    accType = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}, {self.password}, {self.email}, {self.accType}>'
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False) 
    question1 = db.Column(db.Text, nullable=False)
    question2 = db.Column(db.Text, nullable=False)
    question3 = db.Column(db.Text, nullable=False)
    question4 = db.Column(db.Text, nullable=False)
    reviewed = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f"<Feedback id={self.id}, instructor_id={self.instructor_id}, reviewed={self.reviewed}>"
    
class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    assessment = db.Column(db.String(100), nullable=False)
    mark = db.Column(db.Integer)
    request_id = db.Column(db.Integer) 
    request_status = db.Column(db.String(100))

class RemarkRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String, nullable=False)
    assessment = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String, nullable=False)
    grade_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending / Approved / Rejected


@app.route("/")
def index():
    if 'user' in session:
        return render_template("homepage.html")
    return render_template("/login/index.html")

@app.route("/student/feedback")
def student_feedback():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    instructors = Account.query.filter_by(accType='instructor').all()
    user = session.get('user')
    return render_template("/student/feedback.html", instructors=instructors, username=user['username'], accType=user['accType'])

@app.route("/instructor/feedback")
def instructor_feedback():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    instructor_id = user['id']
    feedback = Feedback.query.filter_by(instructor_id=instructor_id).all()
    return render_template("instructor/readfeedback.html", username=user['username'], accType=user['accType'], feedback=feedback)

@app.route("/instructor/readfeedback")
def instructor_readfeedback():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    instructor_id = user['id']
    feedback = Feedback.query.filter_by(instructor_id=instructor_id).all()
    return render_template("instructor/feedback.html", username=user['username'], accType=user['accType'], feedback=feedback)

@app.route("/assignments")
def assignments():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    return render_template("assignments.html", username=user['username'], accType=user['accType'])

@app.route("/course_team")
def course_team():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    return render_template("course_team.html", username=user['username'], accType=user['accType'])

@app.route("/labs")
def labs():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    return render_template("labs.html", username=user['username'], accType=user['accType'])

@app.route("/lecturenotes")
def lecturenotes():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    return render_template("Lecturenotes.html", username=user['username'], accType=user['accType'])

@app.route("/news")
def news():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    return render_template("news.html", username=user['username'], accType=user['accType'])

@app.route("/remark_requests")
def remark_requests():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    username = session.get('user')
    user = Account.query.filter_by(username=username['username']).first()
    if user and user.accType == 'instructor':
        requests = RemarkRequest.query.all()
        return render_template('remark_requests.html', requests=requests)
    else:
        flash("User is not an instructor", "danger")
        return redirect(url_for('homepage'))

@app.route("/change-status", methods=['POST'])
def change_status():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    req = RemarkRequest.query.filter_by(id=request.form['requestId']).first()
    grade = Marks.query.filter_by(id=request.form['gradeId']).first()
    req.status = request.form['new_status']
    grade.request_status = request.form['new_status']
    db.session.commit()
    return jsonify({'result':'success'})

@app.route("/resources")
def resources():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    return render_template("resources.html", username=user['username'], accType=user['accType'])

@app.route("/student_grades")
def student_grades():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    username = session.get('user')
    user = Account.query.filter_by(username=username['username']).first()
    if (user.accType != 'student'):
        flash("User is not an instructor", "danger")
        return redirect(url_for('homepage'))
    grades = Marks.query.filter_by(student_id=user.id).all()
    return render_template('student_grades.html', grades=grades, accType=user.accType)

@app.route("/submit-request", methods=['POST'])
def submit_request():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('index'))
    username = session.get('user')
    user = Account.query.filter_by(username=username['username']).first()
    name = user.firstname + ' ' + user.lastname
    grade = Marks.query.filter_by(id=request.form['gradeId']).first()
    req = RemarkRequest.query.filter_by(grade_id=grade.id).first()
    if req:
        db.session.delete(req)
        db.session.commit()
    new_request = RemarkRequest(student_name=name, assessment=grade.assessment, reason=request.form['reason'], grade_id=grade.id, student_id=user.id)
    db.session.add(new_request)
    db.session.commit()
    grade.request_id = new_request.id
    grade.request_status = new_request.status
    db.session.commit()
    return jsonify({'result':'success', 'gradeId': grade.id})

@app.route("/syllabus")
def syllabus():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    return render_template("syllabus.html", username=user['username'], accType=user['accType'])

@app.route("/tests")
def tests():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    user = session.get('user')
    return render_template("tests.html", username=user['username'], accType=user['accType'])

@app.route("/a1")
def a1():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    return render_template("a1.html")

@app.route("/a2")
def a2():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    return render_template("a2.html")

@app.route("/homepage")
def homepage():
    #check the session first
    if 'user' not in session:
        flash("user not login", "danger")
        return redirect(url_for('index'))
    username = session.get('user')
    user = Account.query.filter_by(username=username['username']).first()
    name = user.firstname + ' ' + user.lastname
    return render_template('homepage.html', username=username['username'], accType=username['accType'], name=name)

@app.route("/read", methods=['GET', 'POST'])        
def read():
    if 'user' not in session:
        flash("User not logged in", "danger")
        return redirect(url_for('login'))
    
    feedback_id = request.form.get('feedback_id')
    feedback = Feedback.query.get(feedback_id)

    if feedback:
        # Toggle the value
        feedback.reviewed = not feedback.reviewed
        db.session.commit()
        flash("Feedback status updated.", "success")

    return redirect(url_for('instructor_feedback'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/')

@app.route("/sending_feedback", methods=['GET', 'POST'])
def sending_feedback():
    if request.method == 'POST':
        instructor_id = request.form.get('instructor_id')
        q1 = request.form.get('question1')
        q2 = request.form.get('question2')
        q3 = request.form.get('question3')
        q4 = request.form.get('question4')
        if not all([q1, q2, q3, q4]):
            flash("Please fill out all the question", "error")
            return redirect(url_for('student_feedback'))
        feedback = Feedback(
            instructor_id=instructor_id,
            question1=q1,
            question2=q2,
            question3=q3,
            question4=q4
        )
        db.session.add(feedback)
        db.session.commit()
        flash("Feedback submitted successfully!", "success")
    return redirect(url_for('student_feedback'))

@app.route("/login")
def login():
    return render_template("login/login.html")

@app.route('/login_in', methods=['GET', 'POST'])
def login_in():
    if request.method == 'GET':
        if 'name' in session:
            flash('You are already logged in!', 'info')
            return redirect(url_for('homepage'))
        return redirect(url_for('login'))
    else:
        username = request.form['username']
        password = request.form['password']
        user = Account.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('index'))
        session['user'] = {
            'id': user.id,
            'username': user.username,
            'accType': user.accType
        }
        if user.accType == 'student':
            flash('Student Login successful!', 'success')
            return redirect(url_for('homepage'))
        else: 
            flash('Instructor Login successful!', 'success')
            return redirect(url_for('homepage')) #check acctype

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('/login/register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        accType = request.form['cbox']

        # Check if user already exists
        if Account.query.filter((Account.username == username) | (Account.email == email)).first():
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Account(username=username, email=email, password=hashed_password, accType = accType, firstname=firstname, lastname=lastname)
        db.session.add(new_user)
        db.session.commit()

        if new_user.accType == 'student':
            a1 = Marks(student_id=new_user.id, assessment='A1', mark=None, request_id=None, request_status=None)
            a2 = Marks(student_id=new_user.id, assessment='A2', mark=None, request_id=None, request_status=None)
            a3 = Marks(student_id=new_user.id, assessment='A3', mark=None, request_id=None, request_status=None)
            labs = Marks(student_id=new_user.id, assessment='Labs', mark=None, request_id=None, request_status=None)
            midterm = Marks(student_id=new_user.id, assessment='Midterm', mark=None, request_id=None, request_status=None)
            final = Marks(student_id=new_user.id, assessment='Final', mark=None, request_id=None, request_status=None)
            db.session.add_all([a1, a2, a3, labs, midterm, final])
            db.session.commit()
        
        flash('Registration successful! Please login now.', 'success')
        return redirect(url_for('login'))

def init_db():
    with app.app_context():
        db.create_all()   

def user_role():
    user = session.get('user')
    if user:
        return {"accType": user.get('accType')}
    return {"accType": None}

@app.route('/instructor_grades')
def instructor_grades():
    students = Account.query.filter_by(accType='student').all()
    student_data = []

    for student in students:
        marks = Marks.query.filter_by(student_id=student.id).all()
        mark_dict = {
            'utorid': student.id,  # or use student.username if that's the UTORid
            'lastname': student.lastname,
            'firstname': student.firstname,
            'A1': None, 'A2': None, 'A3': None,
            'Labs': None, 'Midterm': None, 'Final': None
        }
        for m in marks:
            if m.assessment in mark_dict:
                mark_dict[m.assessment] = m.mark
        student_data.append(mark_dict)

    return render_template('grades.html', students=student_data)  # read-only table


@app.route('/grades_changes')
def grades_changes():
    students = Account.query.filter_by(accType='student').all()
    student_data = []

    for student in students:
        marks = Marks.query.filter_by(student_id=student.id).all()
        mark_dict = {
            'utorid': student.id,
            'lastname': student.lastname,
            'firstname': student.firstname,
            'A1': None, 'A2': None, 'A3': None,
            'Labs': None, 'Midterm': None, 'Final': None
        }
        for m in marks:
            if m.assessment in mark_dict:
                mark_dict[m.assessment] = m.mark
        student_data.append(mark_dict)

    return render_template('grades_changes.html', students=student_data)  # editable table


@app.route('/update_marks', methods=['POST'])
def update_marks():
    students = Account.query.filter_by(accType='student').all()

    for student in students:
        for assessment in ['A1', 'A2', 'A3', 'Labs', 'Midterm', 'Final']:
            form_key = f"{student.id}_{assessment}"
            if form_key in request.form:
                mark_value = request.form[form_key].strip()

                if mark_value == '':
                    continue

                existing_mark = Marks.query.filter_by(student_id=student.id, assessment=assessment).first()

                if existing_mark:
                    # Update existing mark
                    existing_mark.mark = int(mark_value)
                else:
                    # Insert new mark
                    new_mark = Marks(
                        student_id=student.id,
                        assessment=assessment,
                        mark=int(mark_value)
                    )
                    db.session.add(new_mark)

    db.session.commit()
    return redirect(url_for('instructor_grades'))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
 
