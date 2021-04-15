USE master
GO
CREATE DATABASE Library
GO

USE Library
create table User(
	userId serial primary key,
	userName varchar,
	password varchar, 
	email varchar unique,
	phone integer,
	address varchar,
	public_id varchar
	-- is_admin
);

create table Book (
	bookId serial primary key,
	title varchar,
	author varchar,
	publisher varchar,
	copies Integer
);
create table Borrow (
	borrowId serial primary key,
	userId integer,
		foreign key (userId)
		references user(userId),
	bookId integer,
		foreign key (bookId)
		references book(bookId),
	takeDate timestamp,
	broughtDate timestamp
);

GO

CREATE SCHEMA Lib
GO

CREATE PROC Lib.spInsertBook
@bookID int,
@name varchar(50),
@author varchar(30)
@publisher varchar(30) =NULL
@copies int
AS 
INSERT INTO Books
VALUES (@bookID, @name, @author, @copies, @publisher)

EXEC Lib.spInsertBook 1,'The Lost Tribe','John Smyth',2,'Jungle';
EXEC Lib.spInsertBook 2,'How to Sew Buttons','Jane Do',1,'Singer';
EXEC Lib.spInsertBook 3,'The Terrible Night','Eleanor M
EXEC Lib.spInsertBook 4,'Mindy''s Mittens','Heidi Holly',3,'Newton';
EXEC Lib.spInsertBook 5,'Pizza and Donuts Diet','Chef Jeff',4,'Loyly';
EXEC Lib.spInsertBook 6,'101 Cat House Plans','Bart Brat',1,'Mews';
EXEC Lib.spInsertBook 7,'Self-Help for Dummies','Jen Jones',2,'Dada';
EXEC Lib.spInsertBook 8,'Land of Lemurs','Carol Sims',3,'Barr';
EXEC Lib.spInsertBook 9,'Go For It!','Li Li',4,'Higham';
EXEC Lib.spInsertBook 10,'Farming for Nerds','Dr. Dirt',1,'Ten Ton';
EXEC Lib.spInsertBook 11,'They Are Us','Mantek Klem',2,'Cosmo';
EXEC Lib.spInsertBook 12,'Here We Go!','Kit Townsend',3,'Hello';
EXEC Lib.spInsertBook 13,'Spanish for Nurses','Laura Lloras',4,'ANAA';
EXEC Lib.spInsertBook 14,'Tacos Everyday','Sara Carr',4,'Chance';
EXEC Lib.spInsertBook 15,'One Minute Rule','Jens Kopek',3,'BizBooks';
EXEC Lib.spInsertBook 16,'Apples to Oranges','Jim Jordan',2,'Famous';
EXEC Lib.spInsertBook 17,'Tiger Mountain','Silas Lambert',4,'North';
EXEC Lib.spInsertBook 18,'How Cookies Crumble','Barbara Bull',3,'Bibi';
EXEC Lib.spInsertBook 19,'Bridge to Yesterday','Dan Bland',3,'1999';
EXEC Lib.spInsertBook 20,'The Lemonade Stand','Stephen King',2,'Yaya';
EXEC Lib.spInsertBook 21,'Hello World','A. Nonymous',2,'OOL';
GO

CREATE PROC Lib.spInsertLoans
@BookID int,
@BranchID int,
@CardNo int,
@DateOut date,
@DueDate date
AS
INSERT INTO Loans
VALUES (@BookID,@BranchID,@CardNo,@DateOut,@DueDate)

EXEC Lib.spInsertLoans 1,1,4,'2016-08-19','2016-09-19';
EXEC Lib.spInsertLoans 2,2,4,'2016-08-19','2016-09-19';
EXEC Lib.spInsertLoans 3,3,4,'2016-08-19','2016-09-19';
EXEC Lib.spInsertLoans 4,4,4,'2016-08-19','2016-09-19';
EXEC Lib.spInsertLoans 5,1,4,'2016-08-19','2016-09-19';
EXEC Lib.spInsertLoans 6,2,2,'2016-09-18','2016-10-18';
EXEC Lib.spInsertLoans 7,3,2,'2016-09-18','2016-10-18';
EXEC Lib.spInsertLoans 8,4,2,'2016-09-18','2016-10-18';
EXEC Lib.spInsertLoans 9,1,2,'2016-09-18','2016-10-18';
EXEC Lib.spInsertLoans 10,2,2,'2016-09-18','2016-10-18';
EXEC Lib.spInsertLoans 11,3,5,'2016-09-11','2016-10-11';
EXEC Lib.spInsertLoans 12,4,5,'2016-09-11','2016-10-11';
EXEC Lib.spInsertLoans 13,1,5,'2016-09-11','2016-10-11';
EXEC Lib.spInsertLoans 14,2,3,'2016-09-13','2016-10-13';
EXEC Lib.spInsertLoans 15,3,9,'2016-09-11','2016-10-11';
EXEC Lib.spInsertLoans 16,4,1,'2016-05-12','2016-06-12';
EXEC Lib.spInsertLoans 17,1,6,'2016-09-13','2016-10-13';
EXEC Lib.spInsertLoans 18,2,6,'2016-09-13','2016-10-13';
EXEC Lib.spInsertLoans 19,3,6,'2016-09-13','2016-10-13';
EXEC Lib.spInsertLoans 20,4,7,'2016-09-12','2016-10-12';
EXEC Lib.spInsertLoans 21,1,7,'2016-09-13','2016-10-13';
EXEC Lib.spInsertLoans 1,2,7,'2016-09-13','2016-10-13';
EXEC Lib.spInsertLoans 2,3,7,'2016-09-13','2016-10-13';
EXEC Lib.spInsertLoans 4,4,9,'2016-09-09','2016-10-09';
EXEC Lib.spInsertLoans 5,1,9,'2016-09-09','2016-10-09';
EXEC Lib.spInsertLoans 6,2,9,'2016-09-09','2016-10-09';
EXEC Lib.spInsertLoans 7,3,8,'2016-09-10','2016-10-10';
EXEC Lib.spInsertLoans 8,4,8,'2016-09-10','2016-10-10';
EXEC Lib.spInsertLoans 9,1,4,'2016-09-08','2016-10-08';
EXEC Lib.spInsertLoans 10,2,4,'2016-09-08','2016-10-08';
EXEC Lib.spInsertLoans 11,3,4,'2016-09-08','2016-10-08';
EXEC Lib.spInsertLoans 12,4,4,'2016-09-08','2016-10-08';
EXEC Lib.spInsertLoans 13,1,3,'2016-09-07','2016-10-07';
EXEC Lib.spInsertLoans 14,2,3,'2016-09-07','2016-10-07';
EXEC Lib.spInsertLoans 15,3,3,'2016-09-07','2016-10-07';
EXEC Lib.spInsertLoans 16,4,2,'2016-09-05','2016-10-05';
EXEC Lib.spInsertLoans 17,1,2,'2016-09-05','2016-10-05';
EXEC Lib.spInsertLoans 18,2,2,'2016-09-05','2016-10-05';
EXEC Lib.spInsertLoans 19,3,5,'2016-09-04','2016-10-04';
EXEC Lib.spInsertLoans 20,4,5,'2016-09-04','2016-10-04';
EXEC Lib.spInsertLoans 21,1,5,'2016-09-04','2016-10-04';
EXEC Lib.spInsertLoans 22,2,5,'2016-09-04','2016-10-04';
EXEC Lib.spInsertLoans 23,3,5,'2016-09-04','2016-10-04';
EXEC Lib.spInsertLoans 24,4,8,'2016-09-03','2016-10-03';
EXEC Lib.spInsertLoans 25,1,8,'2016-09-03','2016-10-03';
EXEC Lib.spInsertLoans 26,2,8,'2016-09-03','2016-10-03';
EXEC Lib.spInsertLoans 27,3,1,'2016-05-12','2016-06-12';
EXEC Lib.spInsertLoans 28,4,1,'2016-05-12','2016-06-12';
EXEC Lib.spInsertLoans 29,1,1,'2016-05-12','2016-06-12';
EXEC Lib.spInsertLoans 30,2,1,'2016-05-12','2016-06-12'
GO

CREATE PROC Lib.spInsertBorrower
@CardNo int,
@Name varchar(50),
@Address varchar(50),
@Phone varchar(10)=NULL
AS 
INSERT INTO Borrower
VALUES (@CardNo,@Name,@Address,@Phone)

EXEC Lib.spInsertBorrower 1,'Charlie Brown','27 Main St','555-5123';
EXEC Lib.spInsertBorrower 2,'Rachel Rigby','101 Hwy 22','688-7711';
EXEC Lib.spInsertBorrower 3,'Nancy Drew','5678 Oak St','555-3467';
EXEC Lib.spInsertBorrower 4,'Derek Jones','6789 Ritmo Cir','222-1234';
EXEC Lib.spInsertBorrower 5,'Howie Han','111 First Ave','234-5678';
EXEC Lib.spInsertBorrower 6,'Tim Tegulpas','432 Nebraska Ave','987-6543';
EXEC Lib.spInsertBorrower 7,'Sam Semel','7688 Hedge Ct','777-9898';
EXEC Lib.spInsertBorrower 8,'Evan Mann','4545 Court St','899-9090';
EXEC Lib.spInsertBorrower 9,'Sally Short','323 Remington St','767-8991'
EXEC Lib.spInsertBorrower 10,'Bob Biggs','227 South St'
GO


CREATE PROC Lib.spInsertBranch
@BranchID int,
@BranchName varchar(30),
@Address varchar(50)
AS
INSERT INTO Branch
VALUES (@BranchID,@BranchName,@Address)

EXEC Lib.spInsertBranch 1,'Central','10 Main St';
EXEC Lib.spInsertBranch 2,'Sharpstown','25 Pine St';
EXEC Lib.spInsertBranch 3,'River','333 River Rd';
EXEC Lib.spInsertBranch 4,'Field','45 Field St'
GO