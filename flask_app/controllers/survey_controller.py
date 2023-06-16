from flask_app import app
from flask_app.models import survey_model
from flask import render_template, request, redirect, session
app.secret_key = 'secret_number'

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/process', methods=['post'])
def process_data():
    print(request.form)
    if not survey_model.Dojos.validate_dojo(request.form):
        return redirect('/')
    id = survey_model.Dojos.save(request.form)
    
    #remove this later - held for reference for now
    # session['name']=request.form['name']
    # session['location']=request.form['location']
    # session['fav_language']=request.form['fav_language']
    # session['league'] = request.form.getlist('roles')
    # if session['league'] == []:
    #     session['league'] = "Maybe doesn't play league?"
    # session['comment']=request.form['comment']
    # if session['comment'] is '':
    #     session['comment'] = 'No comment'
    
    return redirect(f'/result/{id}')


@app.route('/result/<int:id>')
def result_page(id):
    dojo = survey_model.Dojos.get_one(id)
    return render_template('result.html', dojo = dojo)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')