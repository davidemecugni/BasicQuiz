# Davide Mecugni for KodLand Interview
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    def __init__(self, question_text, option1, option2, option3, correct_option):
        self.question_text = question_text
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.correct_option = correct_option
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    def __init__(self, username, score, date):
        self.username = username
        self.score = score
        self.date = date

# Lista di domande e risposte
questions = [
    Question(question_text='Qual è un framework molto usato per l\'intelligenza artificiale in python?', option1='Pytorch', option2='Word', option3="Steam", correct_option=1),
    Question(question_text='In cosa si può usare l\'intelligenza artificiale', option1='Guidare le auto', option2='Cambiare il clima', option3="Diventare terminator", correct_option=1),
    Question(question_text='Cosa significa l\'acronimo "AI"?', option1='Artificial Intelligence', option2='Automated Interaction', option3='Advanced Interface', correct_option=1),
    Question(question_text='Qual è l\'algoritmo più comune utilizzato per addestrare reti neurali profonde?', option1='K-means', option2='Support Vector Machine', option3='Backpropagation', correct_option=3),
    Question(question_text='Cos\'è la visione artificiale?', option1='Una tecnologia per migliorare l\'acuità visiva umana', option2='Un campo dell\'IA che si occupa dell\'analisi e interpretazione di immagini e video', option3='Una disciplina per la creazione di arte digitale', correct_option=2),
    Question(question_text='Cos\'è il NLP (Natural Language Processing)?', option1='Un metodo per la creazione di linguaggi di programmazione naturali', option2='Un\'area dell\'IA che si occupa dell\'interazione tra computer e linguaggio umano', option3='Una tecnica per la traduzione automatica di testi in lingue diverse', correct_option=2),
    Question(question_text='Qual è il compito principale di un modello di lingua nel NLP?', option1='Riconoscimento di entità nominative', option2='Generazione di testo', option3='Classificazione di documenti', correct_option=2),
    Question(question_text='Cosa è un Chatbot?', option1='Un programma per la chat online tra utenti umani', option2='Un algoritmo per l\'analisi della struttura sintattica delle frasi', option3='Un\'agente virtuale che può conversare con gli utenti tramite testo o voce', correct_option=3),
    Question(question_text='Cosa si intende per "Deep Learning"?', option1='Una tecnica di apprendimento automatico che utilizza alberi decisionali profondi', option2='Un sottoinsieme di tecniche di IA che si concentrano su reti neurali profonde', option3='Un tipo di intelligenza artificiale che utilizza reti neurali superficiali', correct_option=2),
    Question(question_text='Cosa rappresenta l\'analisi di sentimenti nel NLP?', option1='La capacità di interpretare il significato delle frasi', option2='L\'identificazione e classificazione delle opinioni espresse in un testo', option3='L\'analisi della struttura sintattica del testo', correct_option=2),
]

@app.before_request
def setup():
    db.create_all()
    if Question.query.count() == 0 or Question.query.count() != len(questions):
        Question.query.delete()
        db.session.add_all(questions)
        db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = Question.query.all()
    if request.method == "POST":
        score = 0
        username = request.form.get('username')
        for i in range(1, len(questions)):  # Numero totale di domande
            selected_option = int(request.form[f"q{i}"])
            question = Question.query.get(i)
            if question and selected_option == question.correct_option:
                score += 1
        db.session.add(Score(username=username, score=score, date=datetime.now()))
        db.session.commit()
        if score == 0:
            result = "non hai risposto correttamente a nessuna domanda. Riprova!"
        elif score < len(questions) * 0.6:
            result = "hai risposto correttamente solo a poche domande. Prova a studiare di più o chiedi una mano!"
        elif score >= len(questions) * 0.6:
            result = "complimenti! Hai risposto correttamente a molte domande! Sei molto bravo, continua così!"
        elif score == len(questions):
            result = "complimenti! Hai risposto correttamente a tutte le domande! Complimento, sei un vero esperto!"

        top_score = Score.query.filter_by(username=username).order_by(Score.score.desc()).first() # type: ignore
        top_score = top_score.score if top_score else 0
        return render_template("result.html", username=username, score=score, result=result, total=len(questions), top_score=top_score)
    else:
        return render_template("quiz.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
