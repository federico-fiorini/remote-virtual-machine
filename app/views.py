from app import app

from external import BackEndService

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

    
@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['inputName'] != 'web':
            error = 'Invalid username'
        elif request.form['inputPassword'] != 'app':
            error = 'Invalid password'
        else:
            #session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('applications'))
    return render_template('login.html', error=error)
    

@app.route("/applications", methods=['GET', 'POST'])
def applications():
    # In case of GET request, get the location
    if request.method == 'GET':
        return render_template('location.html')

    # In case of POST request, get list of applications by location
    elif request.method == 'POST':

        # Get location from form
        lat = request.form['lat']
        lon = request.form['lon']
        location = {'lat': lat, 'lon': lon}

        # Back-end call
        service = BackEndService()
        applications = service.get_application_list(location)

        # Render applications.html template
        return render_template('applications.html', applications=applications)

