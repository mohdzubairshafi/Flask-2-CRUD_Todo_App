from flask import Flask, render_template, request, redirect, url_for
import string
from random import choice

app = Flask(__name__)


notes = []


def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return "".join(
        choice(string.ascii_letters + string.digits) for _ in range(num_of_chars)
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note_text = request.form.get("note")
        note_id = generate_short_id(5)
        status = "In Progress"
        note = {"id": note_id, "text": note_text, "status": status}
        if note:
            notes.append(note)
        return redirect(request.path)
    if request.method == "GET":
        return render_template("home.html", notes=enumerate(notes))


@app.route("/delete/<id>", methods=["GET"])
def deleteNote(id):
    for note in notes:
        if note["id"] == id:
            notes.remove(note)
            break
    return redirect(url_for("index"))


@app.route("/update", methods=["GET"])
def update():
    note_text = request.form.get("note")
    note_id = request.form.get("id")
    for note in notes:
        if note["id"] == note_id:
            note["text"] = note_text
            break


@app.route("/update/<id>", methods=["GET", "POST"])
def updateNote(id):
    myNote = None
    for note in notes:
        if note["id"] == id:
            myNote = note
    if request.method == "POST":
        note_text = request.form.get("note")
        for note in notes:
            if note["id"] == id:
                note["text"] = note_text
                break

        return redirect(url_for("index"))
    return render_template("update.html", notes=enumerate(notes), note=myNote)


@app.route("/finish/<id>", methods=["POST"])
def finishNote(id):
    for note in notes:
        if note["id"] == id:
            note["status"] = "finished"
            break
    return "Note updated successfully"


if __name__ == "__main__":
    app.debug = True
    app.run(use_reloader=True)
