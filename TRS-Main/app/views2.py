import socketio
import eventlet
from app import app,db,login_manager
from flask import render_template, request, redirect, url_for, jsonify,flash
from forms import *
from models import *
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from Req import *
from sqlalchemy.sql import select
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root@localhost/trs', echo=True)

def getCIdValue(cid):
    newId=''
    newId= cid.split('c')
    newID=int(newId[1])+ 1
    return(newID)

def uniqueCID(cid):
    return('c' + str(cid))

def getDIdValue(did):
    newId=''
    newId= did.split('d')
    newID=int(newId[1])+ 1
    return(newID)

def uniqueDID(did):
    return('d' + str(did))

def getOIdValue(oid):
    newId=''
    newId= oid.split('o')
    newID=int(newId[1])+ 1
    return(newID)

def uniqueOID(oid):
    return('o' + str(oid))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error))
@app.route('/')
#@login_required
def home():
    return render_template('home.html')

@app.route('/map/new_request')
@login_required
def new_request():
    if current_user.id[0] == 'd':
            return redirect(url_for('driver_main'))
    return render_template('map.html')

@app.route("/driver/main")
#@login_required
def driver_main():
    if current_user.id[0] == 'o':
            return redirect(url_for('operator_main'))
    if current_user.id[0] == 'c':
            return redirect(url_for('new_request'))
    return render_template('driver_main.html')

@app.route("/operator/main")
@login_required
def operator_main():
    return render_template('operator_main.html')

@app.route('/add-client', methods=['POST','GET'])
def add_client():
    if current_user.is_authenticated:
        if current_user.id[0]=='d':
            return redirect(url_for('driver_main'))
    cform=clientForm()
    if request.method=='POST':
        if cform.validate_on_submit():
            prevID=db.engine.execute('select cValue from idValue')
            for pID in prevID:
                oldID= pID['cValue']
            specialID=uniqueCID(oldID)
            specIdValue=getCIdValue(specialID)
            cfname=cform.cfname.data
            clname=cform.clname.data
            ccontact=cform.ccontact.data
            cemail=cform.cemail.data
            cpassword=cform.cpassword.data
            cadd1=cform.cadd1.data
            cadd2=cform.cadd2.data
            ccity=cform.ccity.data
            cparish=cform.cparish.data
            client= Clientdb(specialID,cfname,clname,ccontact,cemail,cadd1,cadd2,ccity,cparish,cstatus)
            db.session.add(client)
            db.session.commit()
            db.engine.execute('update idValue set cValue=' + str(specIdValue))
            db.session.commit()
            user=Users(specialID,cemail,cpassword,usertype)
            db.session.add(user)
            db.session.commit()
            flash('User added sucessfully','success')
            if current_user.id[0]=='o':
                return redirect(url_for('operator_main'))
            return redirect (url_for('login'))
    flash_errors(cform)
    return render_template('add_client.html',form=cform)

@app.route('/add-driver', methods=['POST','GET'])
#@login_required
def add_driver():
    if current_user.id[0] != 'o':
        if current_user.id[0]=='d':
            return redirect(url_for('driver_main'))
        else:
            if current_user.id[0]=='c':
                return redirect(url_for('new_request'))
            return redirect(url_for('login'))
    dform=driverForm()
    if request.method=='POST':
        if dform.validate_on_submit():
            prevDID=db.engine.execute('select dValue from idValue')
            for pDID in prevDID:
                oldDID= pDID['dValue']
            specialDID=uniqueDID(oldDID)
            specDIdValue=getDIdValue(specialDID)
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
            prevDID=db.engine.execute('select dValue from idValue')
            for pDID in prevDID:
                oldDID= pDID['dValue']
            specialDID=uniqueDID(oldDID)
            specDIdValue=getDIdValue(specialDID)
            driver= Driverdb(specialDID,dtrn,dfname,dlname,dcontact,demail,dadd1,dadd2,dcity,dparish)
            db.session.add(driver)
            db.session.commit()
            db.engine.execute('update idValue set dValue=' + str(specDIdValue))
            db.session.commit()
            user=Users(specialDID,demail,dpassword,usertype)
            db.session.add(user)
            db.session.commit()
            flash('User added sucessfully','success')
            return redirect (url_for('operator_main'))
    flash_errors(dform)
    return render_template('add_driver.html',form=dform)

@app.route('/add-operator', methods=['POST','GET'])
#@login_required
def add_operator():
    if current_user.id[0] != 'o':
        if current_user.id[0]=='d':
            return redirect(url_for('driver_main'))
        else:
            if current_user.id[0]=='c':
                return redirect(url_for('new_request'))
            return redirect(url_for('login'))
    oform=operatorForm()
    if request.method=='POST':
        if oform.validate_on_submit():
            ofname=oform.ofname.data
            olname=oform.olname.data
            oadd1=oform.oadd1.data
            oadd2=oform.oadd2.data
            ocity=oform.ocity.data
            oparish=oform.oparish.data
            oemail=oform.oemail.data
            opassword=oform.opassword.data
            otrn=oform.otrn.data
            prevOID=db.engine.execute('select oValue from idValue')
            for pOID in prevOID:
                oldOID= pOID['oValue']
            specialOID=uniqueOID(oldOID)
            specOIdValue=getOIdValue(specialOID)
            operator= Operatordb(specialOID,ofname,olname,oadd1,oadd2,ocity,oparish,otrn)
            db.session.add(operator)
            db.session.commit()
            db.engine.execute('update idValue set oValue=' + str(specOIdValue))
            db.session.commit()
            user=Users(specialOID,oemail,opassword,usertype)
            db.session.add(user)
            db.session.commit()
            flash('User added sucessfully','success')
            return redirect (url_for('operator_main'))
    flash_errors(oform)
    return render_template('add_operator.html',form=oform)

@app.route('/add-vehicle', methods=['POST','GET'])
#@login_required
def add_vehicle():
    if current_user.id[0] != 'o':
        if current_user.id[0]=='d':
            return redirect(url_for('driver_main'))
        else:
            if current_user.id[0]=='c':
                return redirect(url_for('new_request'))
            return redirect(url_for('login'))
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
            return redirect (url_for('operator_main'))
    flash_errors(vform)
    return render_template('add_vehicle.html',form=vform)

@app.route('/login',methods=['POST','GET'])
def login():
    lform=LoginForm()
    if request.method=='POST':
        if lform.validate_on_submit():
            un = lform.username.data
            pw = lform.password.data
            print un
            print pw;
            userr = Users.query.filter_by(email=un,password = pw).first()
            print userr;
            login_user(userr)
            if current_user.id[0]=="c":
                return redirect(url_for ('new_request'))
            if current_user.id[0]=="d":
                return redirect(url_for('driver_main'))
            if current_user.id[0]=="o":
                return redirect(url_for('operator_main'))
            next=request.args.get('next')
        else:
            print 'FAIL'
    return render_template('login.html',form=lform)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('login'))

@app.route("/request", methods=["POST","GET"])
@login_required
def request_cab():
    # if current_user.id[0] != 'c' or  current_user.id[0] != 'o':
    #     if current_user.id[0]=='d':
    #         return redirect(url_for('driver_main'))
    #     else:
    #         return redirect(url_for('login'))
    if request.method=="POST":
        seat = request.form['seat']
        vtype= request.form['vehicle']
        wfactor= request.form['wfac']
        driver= request.form['dname']
        cid = current_user.id
        global pickup
        pickup= request.form['pickup']
        global dest
        dest= request.form['dest']
        fNResult= db.engine.execute("select cfname from client where userCID= %s" % cid)
        lNResult= db.engine.execute('select clname from client where userCID= %s' % cid)
        cResult= db.engine.execute('select ccontact from client where userCID= %s' % cid)
        for fname in fNResult:
            fname = fname['cfname']
        for lname in lNResult:
            lname = lname['clname']
        for contact in cResult:
            contact = contact['ccontact']
        global creq
        creq=Client(seat,vtype,wfactor,cid,driver,pickup,dest,fname,lname,contact)
        cdist=creq.dist()
        alist=getDrivers(seat,vtype,driver,cdist)
        # print "REQUEST ROUTE"
        print alist
        return alist
        # return creq.dest() #consider making a global variable and pass to function responsible for p.queue

def getDrivers(seat,vtype,driver,cdist):
    drivers=[]
    pdrivers=[]
    i=0
    j=0
    if driver != '':
        print driver #driver= Put query here using driver(return name,platereg,make,model and color of vchl){Zaavan}
        db.engine.execute("select userDID,pos, lat, longi from driver join driver_location join operates join vehicle on driver.userDID=driver_location.userDID and driver.userDID=operates.userDID and operates.plateNum=vehicle.plateNum where driver= %s" % driver)
        drivers.append([userD['userDID'],dPos['pos'],[ dlat['lat'],dlong['longi'] ] ])
    #driver=  #query name,loc, v.color,v.model,v.make,v.regnum where seat>seatCap,vtype=vtype
        for driver in driver:
            driver.append(driver.dfname,driver.dlname,driver.regnum,driver.model,driver.make,driver.color, driver.loc)

        #return and write to DB
    driversq=  db.engine.execute("select userDID,pos, lat, longi from driver_location join operates join vehicle on driver_location.userDID=operates.userDID and operates.plateNum=vehicle.plateNum where seat_cap= %s seat and class= %s" % seat, vtype)
    if len(driversq)==0:
        return str(["No Drivers Found"])
    for driver in driversq:
        drivers.append([userD['userDID'],dPos['pos'],[ dlat['lat'],dlong['longi'] ] ])

    #drivers=[[123,6],[456,10],[789,7.5],[3412,7],[345,7.67],[678,1],[901,4],[234,5],[567,3],[890,2],[4794,15],[54536,11],[5773,14],[47789,12],[7540,13]] #List produced by database query

    sdrivers=sorted(drivers,key=getKey)
    print sdrivers
    cpos=binary_search(sdrivers, cdist, 0, len(sdrivers)-1)
    # cpos=5 #stub
    print "CPOS"
    print cpos
    j=cpos
    x=cpos+1
    while j > (cpos-5) and j != 0:
        pdrivers.append(sdrivers[j])
        j-=1

    while x < (cpos+6) and x != len(sdrivers):
        pdrivers.append(sdrivers[x])
        x+=1
    print "PDRIVERS"
    print pdrivers

    # loc=[ [18.024583,-76.761250],[18.030585,-76.765521],[18.030801,-76.773276],[18.031141,-76.761521],[18.019688,-76.765046],[18.026336,-76.757449],[18.026572,-76.771523],[18.020625,-76.774054],[18.017870,-76.757470],[18.030816,-76.765507] ]
    i=0
    while (i < len(pdrivers)):
        pdrivers[i].append(loc[i])
        i+=1
    print "loc"
    print pdrivers
    print "GET DRIVERS"
    return str(pdrivers)

@app.route('/report', methods=["GET"])
@login_required
def report():
    if current_user.id[0] != 'o':
        if current_user.id[0]=='d':
            return redirect(url_for('driver_main'))
        else:
            if current_user.id[0]=='c':
                return redirect(url_for('new_request'))
            return redirect(url_for('login'))
    # store all vehicles from database in this variable vehiclesss=
    return render_template("report.html")

@app.route('/view_driver', methods=["GET"])
#@login_required
def view_driver():
    if current_user.id[0] != 'o':
        if current_user.id[0]=='d':
            return redirect(url_for('driver_main'))
        else:
            if current_user.id[0]=='c':
                return redirect(url_for('new_request'))
            return redirect(url_for('login'))
    # store all drivers from database in this variable 
    driversss= db.engine.execute('select dfname, dlname from driver');
    for allD in driversss:
        dfn= allD['dfname']
    for allD in driversss:
        dln= allD['dlname']
    return render_template("view_driver.html")

@app.route('/view_vehicle', methods=["GET"])
#@login_required
def view_vehicles():
    if current_user.id[0] != 'o':
        if current_user.id[0]=='d':
            return redirect(url_for('driver_main'))
        else:
            if current_user.id[0]=='c':
                return redirect(url_for('new_request'))
            return redirect(url_for('login'))
    # store all vehicles from database in this variable vehiclesss=
    return render_template("view_vehicles.html")

@app.route('/view_clients', methods=["GET"])
#@login_required
def view_clients():
    if current_user.id[0] != 'o':
        if current_user.id[0]=='d':
            return redirect(url_for('driver_main'))
        else:
            if current_user.id[0]=='c':
                return redirect(url_for('new_request'))
            return redirect(url_for('login'))
    # store all clients from database in this variable 
    clientss= db.engine.execute('select cfname, clname from client');
    for allC in clientss:
        cfn= allC['cfname']
    for allC in clientss:
        cln= allC['clname']
    return render_template("view_clients.html")

@app.route("/dloc-update", methods=['POST','GET'])
@login_required
def dloc_update():
    if request.method=='POST':
        driverID=current_user.id
        lat=request.form['dlat']
        lng=request.form['dlng']
        db.engine.execute('update lat from driver_location set lat= %s', lat)
        db.engine.execute('update lat from driver_location set longi= %s', lng)
        db.session.commit()

        #update driver location
    return "success"
@app.route("/suggested_drivers",methods=["POST","GET"])
def suggested_drivers():
    if request.method=="POST":
        suggestedDrivers=request.form['suggDrivers']
        for n in suggestedDrivers:
            driId= suggestedDrivers[0]
            driPos= suggestedDrivers[1]
            driLat= suggestedDrivers[2][0]
            driLong= suggestedDrivers[2][1]
            driEta= suggestedDrivers[3]
            db.engine.execute('insert into driver_pool values('+ driId,driPos,driLat,driLong,driEta +')') #query to write list of suggested drivers to db

@app.route("/chosen", methods=["POST","GET"])
def chosen():
    driverId=form['dID']
    name="Spep Marley"
    regnum="7462PP"
    make="Toyoto"
    model="Camery"
    color="red"
    loc=[123,456]
    CDriver= Driver(name,regnum,make,model,color,loc)

    return "success"

@app.route("/job", methods=["POST","GET"])
def job():
    Client =creq
    job= Job(creq, CDriver)

    return "success"

# sio= socketio.Server()
# @sio.on('connect')
# def connect(sid, environ):
#     print('connect ', sid)
#
# @sio.on('my message')
# def message(sid, data):
#     print('message ', data)
#
# @sio.on('disconnect')
# def disconnect(sid):
#     print('disconnect ', sid)

# if __name__ == '__main__':
#     # wrap Flask application with socketio's middleware
#     app = socketio.Middleware(sio, app)
@app.route("/operator", methods=["GET"])
@login_required
def opp_main():
    return render_template("operator_main.html")

@app.route("/operates", methods=["POST","GET"])
@login_required
def operates():
    opform=OperatesForm()
    if request.method=="POST":
        if opform.validate_on_submit():
            #Add queries to check if plate number and trn are already in database
            return render_template("operator_main.html")
    return render_template('operates.html',form=opform)


@app.route("/customer_notification", methods=["GET"])
def customer_notification():
    dfname= "" #received from database
    dlname= ""
    vcolour= ""
    platenum= ""
    eta_driver= ""
    d_loc= ""
    eta= ""
    return render_template("customer_notif.html", dfname=dfname,dlname=dlname, vcolour=vcolour, platenum=platenum, eta_driver=eta_driver, d_loc=d_loc, eta=eta )
