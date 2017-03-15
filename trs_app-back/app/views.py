from app import app,db,login_manager
from flask import render_template, request, redirect, url_for, jsonify,flash
from forms import clientForm, RequestForm, driverForm, operatorForm, vehicleForm,LoginForm
from models import Clientdb, Driver, Operator, Vehicle
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from Req import Client,Driver,Job

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@app.route('/')
# @login_required
def home():
    rform=RequestForm()
    return render_template('map.html',form=rform)


# @app.route('/save-coord', methods=['GET', 'POST'])
# def save_coord():
#     x = request.form['x']
#     y = request.form['y']
#     return jsonify(xcoord=x,ycoord=y)

@app.route('/add-client', methods=['POST','GET'])
def add_client():
    cform=clientForm()

    if request.method=='POST':
        if cform.validate_on_submit():
            cfname=cform.cfname.data
            clname=cform.clname.data
            ccontact=cform.ccontact.data
            cemail=cform.cemail.data
            cpassword=cform.cpassword.data
            cadd1=cform.cadd1.data
            cadd2=cform.cadd2.data
            ccity=cform.ccity.data
            cparish=cform.cparish.data

            client= Client(cfname,clname,ccontact,cemail,cpassword,cadd1,cadd2,ccity,cparish)
            db.session.add(client)
            db.session.commit()

            flash('User added sucessfully','success')
            return redirect (url_for('home'))
    flash_errors(cform)
    return render_template('add_client.html',form=cform)

@app.route('/add-driver', methods=['POST','GET'])
def add_driver():
    dform=driverForm()

    if request.method=='POST':
        if dform.validate_on_submit():
            dfname=dform.dfname.data
            dlname=dform.dlname.data
            dcontact=dform.dcontact.data
            demail=dform.demail.data
            dpassword=dform.dpassword.data
            dadd1=dform.dadd1.data
            dadd2=dform.dadd2.data
            dcity=dform.dcity.data
            dparish=dform.dparish.data
            dtrn=dform.dtrn.data

            driver= Driver(dfname,dlname,dcontact,demail,dpassword,dadd1,dadd2,dcity,dparish,dtrn)
            db.session.add(driver)
            db.session.commit()

            flash('User added sucessfully','success')
            return redirect (url_for('home'))
    flash_errors(dform)
    return render_template('add_driver.html',form=dform)

@app.route('/add-operator', methods=['POST','GET'])
def add_operator():
    oform=operatorForm()

    if request.method=='POST':
        if oform.validate_on_submit():
            ofname=oform.ofname.data
            olname=oform.olname.data
            oadd1=oform.oadd1.data
            oadd2=oform.oadd2.data
            ocity=oform.ocity.data
            oparish=oform.oparish.data
            otrn=oform.otrn.data
            operator= Operator(ofname,olname,oadd1,oadd2,ocity,oparish,otrn)
            db.session.add(operator)
            db.session.commit()

            flash('User added sucessfully','success')
            return redirect (url_for('home'))
    flash_errors(oform)
    return render_template('add_operator.html',form=oform)

@app.route('/add-vehicle', methods=['POST','GET'])
def add_vehicle():
    vform=vehicleForm()

    if request.method=='POST':
        if vform.validate_on_submit():
            platenum=vform.platenum.data
            vmodel=vform.vmodel.data
            vmake=vform.vmake.data
            vcolour=vform.vcolour.data
            seat_cap=vform.seat_cap.data
            vclass=vform.vclass.data

            vehicle= Vehicle(platenum,vmodel,vmake,vcolour,seat_cap,vclass)
            db.session.add(vehicle)
            db.session.commit()

            flash('User added sucessfully','success')
            return redirect (url_for('home'))
    flash_errors(vform)
    return render_template('add_vehicle.html',form=vform)

@app.route('/login',methods=['POST','GET'])
def login():
    lform=LoginForm()
    if request.method=='POST':
        if lform.validate_on_submit():
            un = lform.username.data
            pw = lform.password.data
            print pw;
            userr = Clientdb.query.filter_by(cemail=un,cpassword = pw).first()
            print userr;
            login_user(userr)
            return redirect(url_for ('home'))
            print "Loged In"
            # next=request.args.get('next')
            # if not is_safe_url(next):
            #     return abort(400)
            # return redirect(next or url_for('home'))
        else:
            print 'FAIL'
    return render_template('login.html',form=lform)

@login_manager.user_loader
def load_user(id):
    return Clientdb.query.get(int(id))

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('login'))

@app.route('/request',methods=['POST','GET'])
def request_cab():
    if request.method=="POST":
        seat = request.form['seat']
        vtype= request.form['vehicle']
        wfactor= request.form['wfac']
        driver= request.form['dname']
        cid = 5#current_user.id
        pickup= request.form['pickup']
        dest= request.form['dest']
        fname=  db.engine.execute('select cfname from client where cfname=joice')
        lname='mayer'#query using cid {Zaavi}
        name= fname+" "+ lname
        contact=1235647890 #query using cid{zaavi}
        creq=Client(seat,vtype,wfactor,cid,driver,pickup,dest,name,contact)
        print "SEAT: "+ str(creq.seat)
        print "TYPE: "+ creq.vtype
        print "FACTOR: "+creq.wfactor
        print "ID: "+ str(creq.cid)
        print "DRIVER: "+creq.driver
        print "PICK UP: "+creq.pickup
        print "DEST:"+creq.dest
        print "NAME: "+ str(creq.name)
        print "CONTACT: "+ str(creq.contact)
        print "DIST: "+ str(creq.dist())
        return "success"
        # getDriver(seat,vtype,driver)
        # return creq.dest() #consider making a global variable and pass to function responsible for p.queue

def getDriver(seat,vtype,driver):
    driverss=[]
    i=0
    j=0
    if driver != '':
        print driver #driver= Put query here using driver(return name,platereg,make,model and color of vchl){Zaavan}
    #drivers=  #query name,loc, v.color,v.model,v.make,v.regnum where seat>seatCap,vtype=vtype
    for driver in drivers:
            driverss.append(driver.name,driver.regnum,driver.model,driver.make,driver.color, driver.loc)
    while (i < len(driverss)):
        name=driverss[i][0]
        regnum=driverss[i][1]
        model=driverss[i][2]
        make=make[i][3]
        color=driverss[i][4]
        loc=driverss[i][5]
    pdriver=Driver(name,regnum,make,model,color,loc)
    return pdriver.dest() #Consider passing to another function where the priority list will be populated.


@app.route('/save-coord', methods=['GET', 'POST'])
def save_coord():
    pickup=request.form['pickUpLoc']
    dest=request.form['destLoc']
    print  "PICKUP: "+pickup+", "+"DEST: "+ dest
