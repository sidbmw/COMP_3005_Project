-- DDL for Health and Fitness Club Management System

-- Adding Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL,
    CHECK (role IN ('member', 'trainer', 'admin'))
);

-- Adding Members Table
CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    fitness_goal VARCHAR(255),
    health_metrics VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Adding Trainers Table
CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Adding Equipment Table
CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    CHECK (status IN ('available', 'maintenance', 'unavailable'))
);

-- Adding Rooms Table
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    capacity INT NOT NULL
);

-- Adding Schedule Table
CREATE TABLE schedule (
    schedule_id SERIAL PRIMARY KEY,
    trainer_id INT NOT NULL,
    member_id INT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Adding Booking Table
CREATE TABLE booking (
    booking_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    room_id INT NOT NULL,
    booking_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    CHECK (start_time < end_time)
);

-- Adding Class Schedule Table
CREATE TABLE class_schedule (
    class_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    trainer_id INT NOT NULL,
    room_id INT NOT NULL,
    class_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    CHECK (start_time < end_time)
);

-- Adding Payment Table
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Adding Feedback Table
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    content TEXT NOT NULL,
    submission_date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Adding Exercise Routines Table
CREATE TABLE exercise_routines (
    routine_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    routine_details TEXT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Adding Fitness Achievements Table
CREATE TABLE fitness_achievements (
    achievement_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    achievement_details TEXT NOT NULL,
    achievement_date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Adding Class Registrations Table
CREATE TABLE class_registrations (
    registration_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    class_id INT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (class_id) REFERENCES class_schedule(class_id)
);

-- Adding Trainer Schedule Table
CREATE TABLE IF NOT EXISTS trainer_schedule (
    schedule_id SERIAL PRIMARY KEY,
    trainer_id INT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id)
);
