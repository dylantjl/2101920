from flask import Flask, render_template, request, redirect, url_for, escape

app = Flask(__name__)

def is_safe_input(input_value):
    # Here you would implement checks for XSS and SQL Injection
    # For now, we'll just return True to signify safe input
    return True

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_term = request.form['search']
        if is_safe_input(search_term):
            return redirect(url_for('search_results', query=search_term))
        else:
            # Clear input and reload the home page
            return redirect(url_for('home'))
    return render_template('home.html')

@app.route('/results')
def search_results():
    query = request.args.get('query', '')
    # Escape the query to prevent XSS when displaying it
    safe_query = escape(query)
    return render_template('results.html', search_term=safe_query)

if __name__ == '__main__':
    app.run(debug=True)
