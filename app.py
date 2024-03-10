from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/question1', methods=['GET', 'POST'])
def question1():
    if request.method == 'POST':
        #budget_type = request.form['budget_type']
        return redirect(url_for('question2'))
    return render_template('question1.html')

@app.route('/question2', methods=['GET', 'POST'])
def question2():
    #if request.method == 'POST':
        #income_sources = request.form['income_sources']
        #return redirect(url_for('question3'))
    return render_template('question2.html')

app.route('/question3', methods=['GET', 'POST'])
def question3():
    #if request.method == 'POST':
        #savings = request.form['savings']
        #return redirect(url_for('question4'))
    return render_template('question3.html')

@app.route('/question4', methods=['GET', 'POST'])
def question4():
    #if request.method == 'POST':
        #return redirect(url_for('question5'))
    return render_template('question4.html')

@app.route('/question5', methods=['GET', 'POST'])
def question5():
    #if request.method == 'POST':
        #return redirect(url_for('question6'))
    return render_template('question5.html')

@app.route('/question6', methods=['GET', 'POST'])
def question6():
    #if request.method == 'POST':
        #return redirect(url_for('recommendations'))
    return render_template('question6.html')

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/recommendations')
def recommendations():
    budget_type = request.args.get('budget_type')
    income_sources = request.args.get('income_sources')
    work_study_money = request.args.get('work_study_money')
    external_source = request.args.get('external_source')

    return render_template('recommendations.html', budget_type=budget_type, income_sources=income_sources, work_study_money=work_study_money, external_source=external_source)

if __name__ == '__main__':
    app.run(debug=True)

