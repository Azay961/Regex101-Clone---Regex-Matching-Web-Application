from flask import Flask, render_template, request, session
import re

app = Flask(__name__)
app.secret_key = "ajay"


@app.route('/')
def index():
    # Clear session data on each request
    session.pop('regex_pattern', None)
    session.pop('test_string', None)
    session.pop('matches', None)
    return render_template('index.html')

@app.route('/results', methods=["POST"])
def results():
    regex_pattern = session.get('regex_pattern', '')
    test_string = session.get('test_string', '')
    matches = session.get('matches', None)

    if request.method == 'POST':
        regex_pattern = request.form['regex_pattern']
        test_string = request.form['test_string']

        try:
            matches = re.findall(regex_pattern, test_string)
        except re.error:
            matches = None

        session['regex_pattern'] = regex_pattern
        session['test_string'] = test_string
        session['matches'] = matches
    
    return render_template('index.html', matches=matches, regex_pattern=regex_pattern, test_string=test_string)





@app.route('/mail_validity', methods=["GET", "POST"])
def check_mail():
    if request.method == "POST":
        email = request.form['username']
        try:
            match = re.findall(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", email)
        except re.error:
            match = None
    return render_template('validate_mail.html', match=match)
if __name__ == '__main__':
    app.run(debug=True)
