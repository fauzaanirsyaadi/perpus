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
EXEC Lib.spInsertBook 3,'The Terrible Night','Eleanor M';
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
