from flask import Flask, render_template, request, redirect
from models import db, Tarefa
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        tarefas = Tarefa.query.all()
        return render_template("index.html", tarefas=tarefas)

    @app.route("/add", methods=["POST"])
    def add():
        titulo = request.form.get("titulo")
        if titulo:
            nova = Tarefa(titulo=titulo)
            db.session.add(nova)
            db.session.commit()
        return redirect("/")

    @app.route("/delete/<int:id>")
    def delete(id):
        tarefa = Tarefa.query.get(id)
        db.session.delete(tarefa)
        db.session.commit()
        return redirect("/")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
