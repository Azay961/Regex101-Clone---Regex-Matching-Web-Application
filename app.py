from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Sample data to store user patterns (in a real-world scenario, this should be stored in a database)
saved_patterns = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        regex_pattern = request.form['regex_pattern']
        input_text = request.form['input_text']
        
        # Perform regex matching
        try:
            matches = re.finditer(regex_pattern, input_text)
            match_positions = [(match.start(), match.end()) for match in matches]
        except re.error:
            match_positions = None
        
        return render_template('index.html', match_positions=match_positions, regex_pattern=regex_pattern, input_text=input_text)
    
    return render_template('index.html')

@app.route('/save_pattern', methods=['POST'])
def save_pattern():
    regex_pattern = request.form['regex_pattern']
    pattern_name = request.form['pattern_name']
    
    saved_patterns[pattern_name] = regex_pattern
    
    return 'Pattern saved successfully!'

if __name__ == '__main__':
    app.run(debug=True)
