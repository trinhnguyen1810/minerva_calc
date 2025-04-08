from flask import Flask, render_template, request, session, redirect, url_for, flash
from budget.calculator import BudgetCalculator
import json
import os

app = Flask(__name__)
app.secret_key = 'dev_secret_key_123'  # Fixed key for development

def check_previous_answers(*required_keys):
    """Check if previous questions have been answered."""
    if not all(key in session for key in required_keys):
        missing = [key for key in required_keys if key not in session]
        flash(f'Please complete previous questions first.')
        if 'time_preference' not in session:
            return redirect(url_for('question1'))
        elif 'income' not in session:
            return redirect(url_for('question2'))
        elif 'savings_goal' not in session:
            return redirect(url_for('question3'))
        elif 'spending_preferences' not in session:
            return redirect(url_for('question4'))
        elif 'fixed_expenses' not in session:
            return redirect(url_for('question5'))
        else:
            return redirect(url_for('question1'))
    return None

@app.route('/')
def welcome():
    """Welcome page route."""
    return render_template('welcome.html')

@app.route('/reset')
def reset():
    """Reset session and return to welcome page."""
    session.clear()
    return redirect(url_for('welcome'))

@app.route('/question1', methods=['GET', 'POST'])
def question1():
    """Time preference selection route."""
    if request.method == 'POST':
        recommender = request.form.get('recommender')
        if recommender in ['weekly', 'monthly']:
            session['time_preference'] = recommender
            return redirect(url_for('question2'))
        flash('Please select a valid time preference')
    return render_template('question1.html')

@app.route('/question2', methods=['GET', 'POST'])
def question2():
    """Income input route."""
    check = check_previous_answers('time_preference')
    if check:
        return check
        
    if request.method == 'POST':
        try:
            work_study = float(request.form.get('workStudyIncome', 0))
            external = float(request.form.get('externalResource', 0))
            
            if work_study < 0 or external < 0:
                flash('Income amounts cannot be negative')
                return render_template('question2.html')
                
            session['income'] = {
                'work_study': work_study,
                'external': external
            }
            return redirect(url_for('question3'))
        except ValueError:
            flash('Please enter valid numbers for income')
    return render_template('question2.html')

@app.route('/question3', methods=['GET', 'POST'])
def question3():
    """Savings goal route."""
    check = check_previous_answers('time_preference', 'income')
    if check:
        return check
        
    if request.method == 'POST':
        try:
            savings = float(request.form.get('savings', 0))
            if 0 <= savings <= 50:
                session['savings_goal'] = savings
                return redirect(url_for('question4'))
            flash('Savings percentage must be between 0 and 50%')
        except ValueError:
            flash('Please enter a valid savings percentage')
    return render_template('question3.html')

@app.route('/question4', methods=['GET', 'POST'])
def question4():
    """Spending preferences route."""
    check = check_previous_answers('time_preference', 'income', 'savings_goal')
    if check:
        return check
        
    if request.method == 'POST':
        try:
            preferences = {
                'food': int(request.form.get('groceries', 2)),
                'transportation': int(request.form.get('transportation', 2)),
                'entertainment': int(request.form.get('entertainment', 2)),
                'personal': int(request.form.get('miscellaneous', 2)),
                'gym': int(request.form.get('healthFitness', 2))
            }
            
            if all(1 <= pref <= 3 for pref in preferences.values()):
                session['spending_preferences'] = preferences
                return redirect(url_for('question5'))
            flash('Please rate all categories from 1 to 3')
        except ValueError:
            flash('Invalid preference values')
    return render_template('question4.html')

@app.route('/question5', methods=['GET', 'POST'])
def question5():
    """Fixed expenses route."""
    check = check_previous_answers('time_preference', 'income', 'savings_goal', 'spending_preferences')
    if check:
        return check
        
    if request.method == 'POST':
        try:
            loans = float(request.form.get('loansPayments', 0))
            other = float(request.form.get('otherExpensesPayments', 0))
            
            if loans < 0 or other < 0:
                flash('Expenses cannot be negative')
                return render_template('question5.html')
                
            session['fixed_expenses'] = {
                'loans': loans,
                'other': other
            }
            return redirect(url_for('question6'))
        except ValueError:
            flash('Please enter valid numbers for expenses')
    return render_template('question5.html')

@app.route('/question6', methods=['GET', 'POST'])
def question6():
    """Location selection route."""
    check = check_previous_answers('time_preference', 'income', 'savings_goal', 
                                 'spending_preferences', 'fixed_expenses')
    if check:
        return check
        
    print("Entering question6 route")
    print("Current session data:", dict(session))
    
    if request.method == 'POST':
        location = request.form.get('location')
        print("Received location:", location)
        valid_locations = ['San Francisco', 'Berlin', 'Taipei', 
                         'Hyderabad', 'Seoul', 'Buenos Aires']
        
        if location in valid_locations:
            session['location'] = location
            print("Updated session data:", dict(session))
            return redirect(url_for('recommendations'))
        flash('Please select a valid location')
    return render_template('question6.html')

@app.route('/recommendations')
def recommendations():
    """Budget recommendations route."""
    print("\nEntering recommendations route")
    print("Session data at start:", dict(session))
    
    # Check if all required data is in session
    required_keys = ['income', 'savings_goal', 'spending_preferences', 
                    'fixed_expenses', 'location']
    
    missing_keys = [key for key in required_keys if key not in session]
    print("Missing keys:", missing_keys)
    
    if missing_keys:
        flash(f'Please complete all questions first. Missing data: {", ".join(missing_keys)}')
        return redirect(url_for('welcome'))
    
    try:
        print("All required data present, calculating recommendations...")
        calculator = BudgetCalculator()
        user_data = {
            'income': session['income'],
            'savings_goal': session['savings_goal'],
            'spending_preferences': session['spending_preferences'],
            'fixed_expenses': session['fixed_expenses'],
            'location': session['location']
        }
        
        recommendations = calculator.calculate_recommendations(user_data)
        
        # Verify totals
        total_income = sum(session['income'].values())
        total_allocated = sum(recommendations.values())
        
        if abs(total_income - total_allocated) > 0.01:  # Allow for small floating point differences
            flash('Warning: Budget calculations may be incorrect')
        
        # Prepare chart data
        chart_data = {
            'labels': list(recommendations.keys()),
            'values': list(recommendations.values())
        }
        
        return render_template(
            'recommendations.html',
            recommendations=recommendations,
            chart_data=json.dumps(chart_data),
            time_preference=session.get('time_preference', 'monthly'),
            total_income=total_income,
            total_allocated=total_allocated
        )
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('welcome'))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    # Skip error handling completely for static files
    if request.path.startswith('/static/'):
        return None  # This will prevent Flask from showing any error
    flash('Page not found')
    return redirect(url_for('welcome'))

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    # Skip error handling completely for static files
    if request.path.startswith('/static/'):
        return None  # This will prevent Flask from showing any error
    flash('An internal server error occurred')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)