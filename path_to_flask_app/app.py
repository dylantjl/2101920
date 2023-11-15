from flask import Flask, request, redirect, url_for, escape, render_template
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_term = request.form['search']
        sanitized_input = sanitize_input(search_term)
        if is_sql_injection(sanitized_input):
            # Redirect to home if SQL injection is detected
            return redirect(url_for('home'))
        else:
            # Go to results page if input is safe
            return render_template('results.html', search_term=sanitized_input)
    return render_template('home.html')

def sanitize_input(data):
    data = data.strip()  # Equivalent to PHP's trim
    # stripslashes is not needed in Python as backslashes are not automatically added to quotes
    data = escape(data)  # Equivalent to PHP's htmlspecialchars
    return data

def is_sql_injection(input_str):
    # A basic check for some SQL keywords
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "UNION", "WHERE", "OR", "AND"]
    pattern = '|'.join(sql_keywords)  # Creates a regex pattern like 'SELECT|INSERT|UPDATE|...'
    if re.search(pattern, input_str, re.IGNORECASE):
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
