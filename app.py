# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:44:50 2019

@author: Vinay Valson
"""

from flask import Flask,render_template,url_for,request,redirect,flash,session
from flask_bootstrap import Bootstrap
import matplotlib.pyplot as plt
import os
from werkzeug import secure_filename
import urllib
from mongoconnect import Database



db = Database()
application = app = Flask(__name__)
Bootstrap(app)




@app.route("/query")
def query():
	print(request.query_string)
	return "no query received",200

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	label = 0
	if request.method == 'POST':
		usertype=request.form['usertype']
		username=request.form['username']
		password=request.form['password']
		print(usertype)
		if usertype=='hospital':
			mydoc = db.login_check_hospital(username,password)
		else:
			mydoc = db.login_check(username,password)
		for x in mydoc:
			label=1
			session['login_in'] = True
			if usertype=='hospital':
				return redirect(url_for('location',username=username))
			else:
				return redirect(url_for('personal', username=username))
		if label==0:
			if usertype == 'hospital':
				error = 'Invalid Credentials. Please try again. Please contact Locodonor to register hospital.'
			else:
				error = 'Invalid Credentials. Please try again.'
	return render_template('login.html', error=error)

@app.route('/donorathospital',methods=['GET', 'POST'])
def donorathospital():
	if request.method == 'POST':
		username=request.form['username']
		password=request.form['password']
		donordate=request.form['donordate']
		donorhospital=request.form['donorhospital']
		donorlocation=request.form['donorlocation']
		inserted =  db.existence(username)
		if inserted:
			message='Username does not exists'
			flash(message)
			return render_template('donorathospital.html')
		db.add_donation(username, donordate, donorlocation, donorhospital)
		db.add_donation_hospital(donorhospital,donordate,donorlocation,username)
		return redirect(url_for('location',username=donorhospital))
	return render_template('donorathospital.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location/<username>')
def location(username):
	info = db.personal_info_hospital(username)
	details = []
	for i in info:
		details = i
	print(details)
	dons = details['donations']
	print(dons)
	if details == []:
		details = {'name':'', 'age':'', 'phone':'', 'b_g':'', 'Gender':'', 'address':''}
	return render_template('location.html', dons=dons)

@app.route('/personal/<username>')
def personal(username):
	info = db.personal_info(username)
	details = []
	for i in info:
		details = i
	print(details)
	dons = details['donations']
	print(dons)
	if details == []:
		details = {'name':'', 'age':'', 'phone':'', 'b_g':'', 'Gender':'', 'address':''}
	return render_template('personal.html',posts=details, dons=dons)

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog2')
def blog2():
    return render_template('blog2.html')

@app.route('/registry',methods=["GET","POST"])
def registry():
    return render_template('registry.html')


@app.route('/locate',methods=["GET","POST"])
def locate():
	if request.method=='POST':
		fplace = request.form['fplace']
		fbg = request.form['fbg']
		post = db.locate(fplace,fbg)
		return  render_template('locate.html',posts=post)
	return render_template('locate.html')

@app.route('/doctor',methods=["GET","POST"])
def doctor():
	if request.method=='POST':
		hname = request.form['hname']
		hadd = request.form['hadd']
		hcity = request.form['hcity']
		hstate = request.form['hstate']
		db.insert_doctor(hname,hadd,hcity,hstate)
		return redirect(url_for('registry'))
	return render_template('doctor.html')

@app.route('/hospital',methods=["GET","POST"])
def hospital():
	if request.method=='POST':
		hname = request.form['hname']
		husername = request.form['husername']
		hpassword = request.form['hpassword']
		hadd = request.form['hadd']
		hcity = request.form['hcity']
		hstate = request.form['hstate']
		inserted = db.insert_hospital(hname, husername, hpassword, hadd, hcity, hstate)
		if not inserted:
			message='Try another username'
			flash(message)
			return render_template('hospital.html')
		return redirect(url_for('index'))
	return render_template('hospital.html')

@app.route('/donorform',methods=["GET","POST"])
def donorform():
	if request.method=='POST':
		fn = request.form['fn']
		username = request.form['username']
		password = request.form['password']
		fage = request.form['fage']
		fphone = request.form['fphone']
		fw = request.form['fw']
		fh = request.form['fh']
		faddress = request.form['faddress']
		focc = request.form['focc']
		finfo = request.form['finfo']
		fbg = request.form['fbg']
		fgen = request.form['fgen']
		inserted = db.insert_donor(fn, username, password, fage, fphone, fw,fh,faddress, focc, finfo, fbg, fgen)
		if not inserted:
			message='Try another username'
			flash(message)
			return render_template('donorform.html')
		return redirect(url_for('registry'))
	return render_template('donorform.html')

if __name__ == '__main__':
	app.debug = True
	app.secret_key='12345'
	app.run()
