-- CREATE DATABASE IF NOT EXISTS hms;

-- USE hms;

CREATE TABLE IF NOT EXISTS Staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,
    sex TEXT CHECK(sex IN ("M", "F")) NOT NULL,
    monthly_salary REAL NOT NULL,
    days_available VARCHAR(7) NOT NULL, -- bitmask: 1 for yes, 0 for no, starting Monday
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL, -- time format: HH*60 + MM
    address_id INTEGER,
    phone VARCHAR(24),
    FOREIGN KEY (address_id) REFERENCES Address(address_id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Patient (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,
    sex TEXT CHECK(sex IN ("M", "F")) NOT NULL,
    AMKA VARCHAR(11) NOT NULL,
    address_id INTEGER,
    phone VARCHAR(24),
    doctor_id INTEGER,
    symptoms TEXT DEFAULT NULL,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Doctor (
    doctor_id INTEGER PRIMARY KEY,
    speciality VARCHAR(255) NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES Staff(staff_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Secretary (
    secretary_id INTEGER PRIMARY KEY,
    office_number VARCHAR(24) NOT NULL,
    FOREIGN KEY (secretary_id) REFERENCES Staff(staff_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS LabUser (
    labuser_id INTEGER PRIMARY KEY,
    speciality VARCHAR(255) NOT NULL,
    FOREIGN KEY (labuser_id) REFERENCES Staff(staff_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ExecutiveUser(
    executiveuser_id INTEGER PRIMARY KEY,
    -- more columns?
    FOREIGN KEY (executiveUser_id) REFERENCES Staff(staff_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Appointment (
    visit_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_time DATETIME NOT NULL,
    notes TEXT DEFAULT NULL,
    completed TEXT CHECK(completed IN (("True", "False", "Cancelled"))) NOT NULL DEFAULT 'False',
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Address (
    address_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    street_name VARCHAR(20) NOT NULL,
    street_number INTEGER NOT NULL,
    postal_code INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS StaffNotification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    message TEXT NOT NULL,
    notification_type TEXT CHECK(notification_type IN ("AppointmentRequest"))) NOT NULL,
    -- For appointment request notifications
    patient_id INTEGER DEFAULT NULL,
    speciality VARCHAR(255) DEFAULT NULL,
    appointment_date DATE DEFAULT NULL,
    appointment_info TEXT DEFAULT NULL,
    -- --
    staff_id INTEGER NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PatientNotification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    message TEXT NOT NULL,
    patient_id INTEGER NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS Medicine (
    medicine_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT DEFAULT NULL,
    route_of_administration TEXT CHECK(route_of_administration IN ("Oral", "Topical", "Intravenous")) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS Prescription (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS PrescriptionToMedicine (
    prescription_id INTEGER NOT NULL,
    medicine_id INTEGER NOT NULL,
    amount_mg REAL NOT NULL,
    PRIMARY KEY (prescription_id, medicine_id),
    FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES Medicine(medicine_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Sample (
    sample_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    labuser_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    sample_date TIMESTAMP NOT NULL,
    result TEXT NOT NULL,
    FOREIGN KEY (labuser_id) REFERENCES labUser(labuser_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON UPDATE CASCADE ON DELETE CASCADE
);
