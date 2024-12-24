from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
# Secret key needed to encrypt the cookies
app.secret_key = 'thisisnotmyrealsecretkeyiusesomethingelse'


# Configuring session and setting some 'rules'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/timer", methods=["GET"])
def timer():
    return render_template('timer.html')


@app.route("/todolist", methods=["GET", "POST"])
def todolist():
    # Using sessions we can save each time something is added to the user's to-do list without needing to use a database.
    # The emtpy brackets essentially mean that if the session items doesn't exist - initialize it to an empty array instead.
    items = session.get('items', [])
    if request.method == "POST":
        task = request.form.get("listinput")
        try:
            buttonPressed = int(request.form.get("counter"))
        except ValueError:
            buttonPressed = 0
        #items = session.get('items', [])
        if buttonPressed != 0:
            items.pop(buttonPressed-1)
        else:
            items.append(task)
        session['items'] = items
        buttonPressed = 0
        return render_template('list.html', entries=items)
    else:
        return render_template('list.html', entries=items)

@app.route("/flashcards", methods=["GET", "POST"])
def flashcards():
    flashcard = session.get('flashcard', [])
    if request.method == "POST":
        title = request.form.get("flashcardtitle")
        body = request.form.get("flashcardbody")
        clear = request.form.get("clearButton1")
        # If the button has been clicked we make the session and the flashcard variable equal to an empty array, so it essentially clears everything
        if clear == 'true':
            session['flashcard'] = []
            flashcard = []
            return render_template('flashcards.html', entries=flashcard)
        else:
            # The session is a list, but we append a dictionary so we have access to each title and prompt easily.
            new_entry = {'title': title, 'body': body}
            flashcard.append(new_entry)
            session['flashcard'] = flashcard
        clear = ""
        return render_template('flashcards.html', entries=flashcard)
    else:
        return render_template('flashcards.html', entries=flashcard)
