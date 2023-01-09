CREATE DATABASE AutomobileCompany;

USE AutomobileCompany;

CREATE TABLE Brand (
    BID VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    PRIMARY KEY (BID)
);

CREATE TABLE Model (
    MID VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    body_style VARCHAR(20) NOT NULL,
    BID VARCHAR(20) NOT NULL,
    PRIMARY KEY (MID),
    FOREIGN KEY (BID) REFERENCES Brand(BID)
);

CREATE TABLE Option (
    MID VARCHAR(20) NOT NULL,
    color VARCHAR(20) NOT NULL,
    engine VARCHAR(20) NOT NULL,
    transmission VARCHAR(20) NOT NULL,
    PRIMARY KEY (MID, color, engine, transmission),
    FOREIGN KEY (MID) REFERENCES Model(MID)
);

CREATE TABLE Part (
    model VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    info VARCHAR(20),
    PRIMARY KEY (model)
);

CREATE TABLE Supplier (
    supplier_name VARCHAR(20) NOT NULL,
    country VARCHAR(20),
    city VARCHAR(20),
    street VARCHAR(20),
    PRIMARY KEY (supplier_name)
);

CREATE TABLE Plant (
    plant_name VARCHAR(20) NOT NULL,
    work_type VARCHAR(20) NOT NULL,
    country VARCHAR(20),
    city VARCHAR(20),
    street VARCHAR(20),
    PRIMARY KEY (plant_name)
);

CREATE TABLE Vehicle (
    VIN VARCHAR(20) NOT NULL,
    price INT NOT NULL,
    plant_name VARCHAR(20) NOT NULL,
    assembly_year INT NOT NULL,
    assembly_month INT NOT NULL,
    assembly_day INT NOT NULL,
    MID VARCHAR(20) NOT NULL,
    color VARCHAR(20) NOT NULL,
    engine VARCHAR(20) NOT NULL,
    transmission VARCHAR(20) NOT NULL,
    PRIMARY KEY (VIN),
    FOREIGN KEY (plant_name) REFERENCES Plant(plant_name),
    FOREIGN KEY (MID, color, engine, transmission) REFERENCES Option(MID, color, engine, transmission)
);

CREATE TABLE Dealer (
    DID VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    country VARCHAR(20),
    city VARCHAR(20),
    PRIMARY KEY (DID)
);

CREATE TABLE Customer (
    CID VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    country VARCHAR(20),
    city VARCHAR(20),
    street VARCHAR(20),
    gender VARCHAR(20),
    annual_income INT,
    PRIMARY KEY (CID)
);

CREATE TABLE customer_phone (
    CID VARCHAR(20) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    PRIMARY KEY (CID, phone),
    FOREIGN KEY (CID) REFERENCES Customer(CID)
);

CREATE TABLE requires (
    MID VARCHAR(20) NOT NULL,
    part_model VARCHAR(20) NOT NULL,
    PRIMARY KEY (MID, part_model),
    FOREIGN KEY (MID) REFERENCES Model(MID),
    FOREIGN KEY (part_model) REFERENCES Part(model)
);

CREATE TABLE supplies (
    supplier_name VARCHAR(20) NOT NULL,
    part_model VARCHAR(20) NOT NULL,
    PRIMARY KEY (supplier_name, part_model),
    FOREIGN KEY (supplier_name) REFERENCES Supplier(supplier_name),
    FOREIGN KEY (part_model) REFERENCES Part(model)
);

CREATE TABLE manufactures (
    plant_name VARCHAR(20) NOT NULL,
    part_model VARCHAR(20) NOT NULL,
    PRIMARY KEY (plant_name, part_model),
    FOREIGN KEY (plant_name) REFERENCES Plant(plant_name),
    FOREIGN KEY (part_model) REFERENCES Part(model)
);
CREATE TABLE inventory (
    VIN VARCHAR(20) NOT NULL,
    DID VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    is_sold INT NOT NULL,
    PRIMARY KEY (VIN),
    FOREIGN KEY (VIN) REFERENCES Vehicle(VIN),
    FOREIGN KEY (DID) REFERENCES Dealer(DID)
);

CREATE TABLE sales(
    BID VARCHAR(20) NOT NULL,
    MID VARCHAR(20) NOT NULL,
    color VARCHAR(20) NOT NULL,
    DID VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (BID, MID, color, DID, year, month, day),
    FOREIGN KEY (BID) REFERENCES Brand(BID),
    FOREIGN KEY (MID, color) REFERENCES Option(MID, color),
    FOREIGN KEY (DID) REFERENCES Dealer(DID)
);

CREATE TABLE sells (
    VIN VARCHAR(20) NOT NULL,
    DID VARCHAR(20) NOT NULL,
    CID VARCHAR(20) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    PRIMARY KEY (VIN),
    FOREIGN KEY (VIN, DID) REFERENCES inventory(VIN, DID),
    FOREIGN KEY (CID) REFERENCES Customer(CID)
);