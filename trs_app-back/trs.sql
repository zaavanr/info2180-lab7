/*-------Creating the Database-----*/
create Database trs;
use trs;

/*----Creating the Tables----*/
create table client(
		id int not null AUTO_INCREMENT,
		cfname varchar(20),
		clname varchar(20),
		ccontact int(11),
    	cemail varchar(17),
    	cpassword varchar (20),
    	cadd1 varchar (30),
    	cadd2 varchar(30),
		city varchar(25),
		parish varchar(12),
		primary key(id)
		);
create table driver(
		dtrn int(9) not null,
		dfname varchar(20),
		dlname varchar(20),
    	dcontact varchar(10),
    	demail varchar (15),
    	dpassword varchar(20),
    	daddr1 varchar(20),
    	daddr2 varchar(20),
		dcity varchar(20),
		dparish varchar(12),
		primary key(dtrn)
		);
create table operator(
		opID int not null AUTO_INCREMENT,
		ofname varchar(20),
		olname varchar(20),
		otrn int(10),
    	oadd1 varchar(20),
    	oadd2 varchar(20),
    	ocity varchar(20),
		oparish varchar(12),
		primary key(opID)
		);
create table vehicle(
		plateNum varchar(8) not null,
		vmodel varchar(10),
		vmake varchar(15),
		vcolour varchar(10),
		seat_cap int(1),
		class varchar(10),
		primary key(plateNum)
);
create table view(
	dtrn int(9),
	id int not null,
	opID int not null,
	plateNum varchar(6),
	job_date date,
	job_time time,
	job_status varchar(9),
	primary key(dtrn,id,opID,plateNum),
	foreign key (dtrn) references driver(dtrn) on delete cascade on update cascade,
	foreign key (id) references client(id) on delete cascade on update cascade,
	foreign key (opID) references operator(opID) on delete cascade on update cascade,
	foreign key (plateNum) references vehicle(plateNum) on delete cascade on update cascade
);
create table carry(
	id int(12),
	dtrn int(9),
	plateNum varchar(6),
	primary key(dtrn,id,plateNum),
	foreign key (dtrn) references driver(dtrn) on update cascade on delete cascade,
	foreign key (id) references client(id) on update cascade on delete cascade,
	foreign key (plateNum) references vehicle(plateNum) on update cascade on delete cascade
);
create table operates(
	dtrn int(9),
	plateNum varchar(6),
	primary key(dtrn,plateNum),
	foreign key (dtrn) references driver(dtrn) on update cascade on delete cascade,
	foreign key (plateNum) references vehicle(plateNum) on update cascade on delete cascade
);
