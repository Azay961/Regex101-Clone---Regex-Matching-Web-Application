from flask import Flask, render_template, request, session
import re

app = Flask(__name__)
app.secret_key = "ajay_1240153"

user_data = {
    'user@gmail.com': {'password': 'password1', 'patterns': ['pattern1', 'pattern1a']},
    'user2': {'password': 'password2', 'patterns': ['pattern2', 'pattern2a']},
    'user3': {'password': 'password3', 'patterns': ['pattern3', 'pattern3a']},
}
current_user = ''
current_pattern =''
@app.route('/')
def index():

    return render_template('index.html', username=None)

@app.route('/results', methods=["POST"])
def results():
    global current_pattern
    regex_pattern = session.get('regex_pattern', '')
    test_string = session.get('test_string', '')
    matches = session.get('matches', None)

    if request.method == 'POST':
        regex_pattern = request.form['regex_pattern']
        test_string = request.form['test_string']
        current_pattern = regex_pattern

        try:
            matches = re.findall(regex_pattern, test_string)
        except re.error:
            matches = None

        session['regex_pattern'] = regex_pattern
        session['test_string'] = test_string
        session['matches'] = matches
    return render_template('index.html', matches=matches, regex_pattern=regex_pattern, test_string=test_string, username=current_user)




@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home', methods=["GET", "POST"])
def home():
    global user_data
    global current_user
    

    action = request.form.get('action')
    if action == "Login":
        username = request.form['username']
        password = request.form['password']

        if username in user_data:
            if user_data[username]["password"] == password:
                current_user = username
                return render_template("index.html", username=username, msg="Login successfull")
            else:
                return render_template("login.html", msg="Incorrect password")
            
    elif action == "Signup":
        username = request.form['email']
        password = request.form['password']
        if username not in user_data:
            new_user = {
                "password": password,
                "patterns": []
            }
            user_data[username] = new_user
            session['current_user'] = username
            return render_template("login.html", username=current_user, msg="Signup successfull")
        else:
            return render_template("signup.html", msg="Username already exists. Please choose a different one.")


@app.route('/mail_validity', methods=["GET", "POST"])
def check_mail():
    if request.method == "POST":
        email = request.form['username']
        try:
            match = re.findall(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", email)
        except re.error:
            match = None
    return render_template('validate_mail.html', match=match)

@app.route('/save', methods=["GET", "POST"])
def save_pattern():
    if current_pattern:
        user_data[current_user]['patterns'].append(current_pattern)
        return "Saved successfully"
    else:
        return "Enter pattern first"

@app.route('/view', methods=["GET", "POST"])
def view():
    return render_template("view.html", patterns=user_data[current_user]["patterns"])
if __name__ == '__main__':
    app.run(debug=True)
