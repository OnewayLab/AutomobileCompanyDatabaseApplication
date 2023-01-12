INSERT INTO Brand (BID, name)
VALUES ('B1', 'Toyota'),
       ('B2', 'Honda'),
       ('B3', 'Ford'),
       ('B4', 'Chevrolet'),
       ('B5', 'Nissan');

INSERT INTO Model (MID, name, body_style, BID)
VALUES ('M1', 'Camry', 'Sedan', 'B1'),
       ('M2', 'Civic', 'Sedan', 'B2'),
       ('M3', 'Mustang', 'Coupe', 'B3'),
       ('M4', 'Cruze', 'Sedan', 'B4'),
       ('M5', 'Altima', 'Sedan', 'B5');

INSERT INTO Option (MID, color, engine, transmission)
VALUES ('M1', 'Black', 'V6', 'Automatic'),
       ('M1', 'White', 'V4', 'Manual'),
       ('M2', 'Blue', 'V4', 'Automatic'),
       ('M2', 'Red', 'V4', 'Manual'),
       ('M3', 'Red', 'V8', 'Manual'),
       ('M3', 'Yellow', 'V8', 'Automatic'),
       ('M4', 'Silver', 'V6', 'Manual'),
       ('M4', 'Gray', 'V4', 'Automatic'),
       ('M5', 'Black', 'V4', 'Manual'),
       ('M5', 'White', 'V6', 'Automatic');

INSERT INTO Part (model, name, info)
VALUES ('P1', 'Tire', '195/65/15'),
       ('P2', 'Battery', '12V'),
       ('P3', 'Brake Pad', 'Front'),
       ('P4', 'Air Filter', 'Cabin'),
       ('P5', 'Spark Plug', 'Iridium'),
       ('P6', 'Fuel Filter', 'In-line');

INSERT INTO Supplier (supplier_name, country, city, street)
VALUES ('S1', 'Japan', 'Tokyo', 'Sakura St'),
       ('S2', 'USA', 'New York', 'Broadway'),
       ('S3', 'Germany', 'Berlin', 'Alexanderplatz'),
       ('S4', 'Korea', 'Seoul', 'Gangnam-gu'),
       ('S5', 'China', 'Shanghai', 'Pudong');

INSERT INTO Plant (plant_name, work_type, country, city, street)
VALUES ('Pl1', 'Assembly', 'Japan', 'Toyota', 'Aichi'),
       ('Pl2', 'Assembly', 'USA', 'Marysville', 'Ohio'),
       ('Pl3', 'Assembly', 'Germany', 'Cologne', 'Merheimer'),
       ('Pl4', 'Assembly', 'Korea', 'Seoul', 'Gwangju'),
       ('Pl5', 'Assembly', 'China', 'Shanghai', 'Pudong');

INSERT INTO Vehicle (VIN, price, plant_name, assembly_year, assembly_month, assembly_day, MID, color, engine, transmission)
VALUES ('V1', '25000', 'Pl1', '2022', '01', '01', 'M1', 'Black', 'V6', 'Automatic'),
('V2', '23000', 'Pl2', '2022', '01', '01', 'M1', 'White', 'V4', 'Manual'),
('V3', '30000', 'Pl3', '2022', '01', '01', 'M3', 'Red', 'V8', 'Manual'),
('V4', '28000', 'Pl4', '2022', '02', '01', 'M4', 'Silver', 'V6', 'Manual'),
('V5', '32000', 'Pl5', '2022', '03', '01', 'M5', 'Black', 'V4', 'Manual'),
('V6', '35000', 'Pl1', '2022', '04', '01', 'M2', 'Red', 'V4', 'Manual'),
('V7', '38000', 'Pl2', '2022', '05', '01', 'M3', 'Yellow', 'V8', 'Automatic'),
('V8', '40000', 'Pl3', '2022', '06', '01', 'M4', 'Gray', 'V4', 'Automatic'),
('V9', '42000', 'Pl4', '2022', '07', '01', 'M5', 'White', 'V6', 'Automatic'),
('V10', '45000', 'Pl5', '2022', '08', '01', 'M1', 'Black', 'V6', 'Automatic');

INSERT INTO Dealer (DID, name, country, city)
VALUES ('D1', 'ABC', 'USA', 'Los Angeles'),
('D2', 'DEF', 'Germany', 'Berlin'),
('D3', 'GHI', 'Japan', 'Tokyo'),
('D4', 'JKL', 'Korea', 'Seoul'),
('D5', 'MNO', 'China', 'Shanghai');

INSERT INTO Customer (CID, name, country, city, street, gender, annual_income)
VALUES ('C1', 'John Doe', 'USA', 'Los Angeles', 'Hollywood', 'Male', '70000'),
('C2', 'Jane Smith', 'Germany', 'Berlin', 'Mitte', 'Female', '60000'),
('C3', 'Michael Johnson', 'Japan', 'Tokyo', 'Shibuya', 'Male', '80000'),
('C4', 'Sara Lee', 'Korea', 'Seoul', 'Gangnam-gu', 'Female', '75000'),
('C5', 'David Kim', 'China', 'Shanghai', 'Pudong', 'Male', '90000');

INSERT INTO customer_phone (CID, phone)
VALUES ('C1', '555-555-1234'),
('C1', '555-555-5678'),
('C2', '555-555-4321'),
('C2', '555-555-8765'),
('C3', '555-555-2468'),
('C4', '555-555-1357'),
('C4', '555-555-9876'),
('C5', '555-555-6543'),
('C5', '555-555-2109');

INSERT INTO requires (MID, part_model)
VALUES ('M1', 'P1'),
('M1', 'P2'),
('M1', 'P3'),
('M2', 'P4'),
('M2', 'P5'),
('M3', 'P6'),
('M4', 'P1'),
('M4', 'P2'),
('M5', 'P3'),
('M5', 'P4');

INSERT INTO supplies (supplier_name, part_model)
VALUES ('S1', 'P1'),
('S1', 'P2'),
('S2', 'P3'),
('S2', 'P4'),
('S3', 'P5'),
('S3', 'P6'),
('S4', 'P1'),
('S4', 'P2'),
('S5', 'P3'),
('S5', 'P4');

INSERT INTO manufactures (plant_name, MID)
VALUES ('Pl1', 'M1'),
('Pl1', 'M2'),
('Pl2', 'M3'),
('Pl2', 'M4'),
('Pl3', 'M5'),
('Pl4', 'M1'),
('Pl4', 'M2'),
('Pl5', 'M3'),
('Pl5', 'M4');