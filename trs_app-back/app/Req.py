import math

class Client():
    def __init__(self,seat,vtype,wfactor,cid,driver,pickup,dest,fname,lname,contact):
        self.seat=seat
        self.vtype=vtype
        self.wfactor=wfactor
        self.cid=cid
        self.driver=driver
        self.pickup=pickup
        self.dest=dest
        self.fname=fname
        self.lname=lname
        self.contact=contact

    def dist(self):
        x1= 5#self.pickup[0]
        y1= 3#self.pickup[1]
        x2=0
        y2=0
        val=math.sqrt(((x2-x1)**2)+((y2-y1)**2))
        print "CLASS: "+str(val) + " "+str(self.pickup[0:10]) +" "+str(self.pickup[11:])
        print self.pickup
        return 3

class Driver():
    def __init__(self,name,regnum,make,model,color,loc):
        self.name=name
        self.regnum=regnum
        self.make=make
        self.model=model
        self.color=color
        self.loc=loc

class Job():
    def __init__(self, c,d):
        self.driver=d
        self.client=c

    def drive(self):
        return self.driver.name
