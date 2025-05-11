---------------------------------------------Look-Up Tables--------------------------------------------
CREATE DATABASE Freelance;
USE Freelance;

CREATE TABLE User_Roles(
	Role_ID INT IDENTITY(1,1) PRIMARY KEY,
	Role_Name VARCHAR(50) NOT NULL UNIQUE);
CREATE TABLE Project_Status (
    Project_Status_ID INT IDENTITY(1,1) PRIMARY KEY,
    Project_Status_Name VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE Proposal_Status (
    Proposal_Status_ID INT IDENTITY(1,1) PRIMARY KEY,
    Proposal_Status_Name VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE Contract_Status (
    Contract_Status_ID INT IDENTITY(1,1) PRIMARY KEY,
    Contract_Status_Name VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE Payment_Status (
    Payment_Status_ID INT IDENTITY(1,1) PRIMARY KEY,
    Payment_Status_Name VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE User_Status (
    Status_ID INT IDENTITY(1,1) PRIMARY KEY,
    Status_Name VARCHAR(50) NOT NULL UNIQUE
);
---------------------------------------------Main Tables---------------------------------------------
CREATE TABLE Users (
    User_ID INT IDENTITY(1,1) PRIMARY KEY,
    User_Name VARCHAR(100) NOT NULL,
    User_Email VARCHAR(100) NOT NULL UNIQUE,
    User_Phone VARCHAR(15) NOT NULL UNIQUE,
    Role_ID INT NOT NULL,  
    User_Password VARCHAR(255) NOT NULL,
    User_Profile_Description TEXT,
	Status_ID INT NOT NULL DEFAULT 1,
    FOREIGN KEY (Role_ID) REFERENCES User_Roles(Role_ID),
	FOREIGN KEY (Status_ID) REFERENCES User_Status(Status_ID)
);
CREATE TABLE Projects (
    Project_ID INT IDENTITY(1,1) PRIMARY KEY,
    Client_ID INT NOT NULL,  
    Project_Title VARCHAR(255) NOT NULL,
    Project_Description TEXT NOT NULL,
    Project_Budget DECIMAL(10,2) NOT NULL,
    Project_Deadline DATE NOT NULL,
    Project_Status_ID INT NOT NULL,  
    FOREIGN KEY (Client_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Project_Status_ID) REFERENCES Project_Status(Project_Status_ID)
);
CREATE TABLE Proposals(
    Proposal_ID INT IDENTITY(1,1) PRIMARY KEY,
    Freelancer_ID INT NOT NULL,  
    Project_ID INT NOT NULL,  
    Proposal_Bid_Amount DECIMAL(10,2) NOT NULL,
    Proposal_Description TEXT NOT NULL,
    Proposal_Status_ID INT NOT NULL, 
    FOREIGN KEY (Freelancer_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Project_ID) REFERENCES Projects(Project_ID),
    FOREIGN KEY (Proposal_Status_ID) REFERENCES Proposal_Status(Proposal_Status_ID)
);
CREATE TABLE Contracts (
    Contract_ID INT IDENTITY(1,1) PRIMARY KEY,
    Project_ID INT NOT NULL,  
    Freelancer_ID INT NOT NULL, 
    Client_ID INT NOT NULL,  
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    Contract_Status_ID INT NOT NULL,  
    FOREIGN KEY (Project_ID) REFERENCES Projects(Project_ID),
    FOREIGN KEY (Freelancer_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Client_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Contract_Status_ID) REFERENCES Contract_Status(Contract_Status_ID)
);
CREATE TABLE Payments (
    Payment_ID INT IDENTITY(1,1) PRIMARY KEY,
    Contract_ID INT NOT NULL,  
    Amount DECIMAL(10,2) NOT NULL,
    Payment_Method VARCHAR(50) NOT NULL,
    Payment_Date DATE NOT NULL,
    Payment_Status_ID INT NOT NULL,  
    FOREIGN KEY (Contract_ID) REFERENCES Contracts(Contract_ID),
    FOREIGN KEY (Payment_Status_ID) REFERENCES Payment_Status(Payment_Status_ID)
);
CREATE TABLE Messages (
    Message_ID INT IDENTITY(1,1) PRIMARY KEY,
    Sender_ID INT NOT NULL,  
    Receiver_ID INT NOT NULL,  
    Message_Content TEXT NOT NULL,
    Timestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (Sender_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES Users(User_ID)
);SELECT * FROM Users

CREATE TABLE Reviews (
    Review_ID INT IDENTITY(1,1) PRIMARY KEY,
    Reviewer_ID INT NOT NULL,  
    Reviewed_User_ID INT NOT NULL,  -- 
    Project_ID INT NOT NULL,  
    Rating INT CHECK (Rating BETWEEN 1 AND 5),  
    Comment TEXT,
    Review_Date DATE DEFAULT GETDATE(),
    FOREIGN KEY (Reviewer_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Reviewed_User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Project_ID) REFERENCES Projects(Project_ID)
);
CREATE TABLE Skills (
    Skill_ID INT IDENTITY(1,1) PRIMARY KEY,
    Skill_Name VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE User_Skills (
    User_ID INT NOT NULL,  -- FK from Users
    Skill_ID INT NOT NULL,  -- FK from Skills
    PRIMARY KEY (User_ID, Skill_ID),  -- Composite Key
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Skill_ID) REFERENCES Skills(Skill_ID) 
);
--------------------------------------------Insertion------------------------------------------
INSERT INTO User_Roles (Role_Name) 
VALUES ('Freelancer'), ('Client'), ('Both');
INSERT INTO Project_Status (Project_Status_Name) 
VALUES ('Open'), ('In Progress'), ('Completed'), ('Closed') ;
INSERT INTO Proposal_Status (Proposal_Status_Name) 
VALUES ('Pending'), ('Accepted'), ('Rejected');
INSERT INTO Contract_Status (Contract_Status_Name) 
VALUES ('Active'), ('Completed'), ('Terminated');
INSERT INTO Payment_Status (Payment_Status_Name) 
VALUES ('Pending'), ('Paid'), ('Failed');
INSERT INTO User_Status (Status_Name) 
VALUES ('Active'), ('Inactive'), ('Suspended');
INSERT INTO Skills (Skill_Name) 
VALUES 
('App Development'), 
('Cloud Computing'), 
('Content Writing'), 
('Cybersecurity'), 
('Data Analysis'), 
('Database Design'), 
('Digital Marketing'), 
('Graphic Design'), 
('Python'), 
('SEO'), 
('UI/UX'), 
('Video Editing'), 
('Web Development');


