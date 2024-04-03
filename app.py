from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

# Aggiungi le tue domande al database
@app.before_first_request
def setup():
    db.create_all()
    if Question.query.count() == 0:
        q1 = Question(question_text='Qual è il capitale del Giappone?', option1='Tokyo', option2='Pechino', option3='Seul', correct_option=1)
        q2 = Question(question_text='Quanti stati compongono gli Stati Uniti d\'America?', option1='49', option2='50', option3='51', correct_option=2)
        db.session.add_all([q1, q2])
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        score = 0
        for i in range(1, 3):  # Numero totale di domande
            selected_option = int(request.form[f'q{i}'])
            question = Question.query.get(i)
            if selected_option == question.correct_option:
                score += 1
        return render_template('result.html', score=score)
    else:
        questions = Question.query.all()
        return render_template('quiz.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
