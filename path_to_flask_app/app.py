from flask import Flask, render_template, request, redirect, url_for, flash, escape

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to check for XSS attacks
def is_xss_attack(input_value):
    xss_patterns = ['<script>', '</script>', 'javascript:', 'onerror', 'onload']
    return any(pattern in input_value for pattern in xss_patterns)

# Function to check for SQL injection attempts
def is_sql_injection(input_value):
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', 'WHERE', 'OR', 'AND']
    return any(keyword.lower() in input_value.lower() for keyword in sql_keywords)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_term = request.form['search']
        if is_xss_attack(search_term) or is_sql_injection(search_term):
            flash('Invalid input detected. Please try again.')  # Optionally flash a message to the user
            return redirect(url_for('home'))
        else:
            # Redirect to the results page with sanitized search term
            safe_search_term = escape(search_term)
            return redirect(url_for('results', search_term=safe_search_term))
    return render_template('home.html')

@app.route('/results')
def results():
    # The search_term is sanitized before passing to the template
    search_term = request.args.get('search_term', '')
    return render_template('results.html', search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)
