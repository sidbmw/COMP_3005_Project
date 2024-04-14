-- DML for Health and Fitness Club Management System

-- Inserting sample users
INSERT INTO users (username, password, email, role) VALUES
('john_doe', 'password123', 'john@example.com', 'member'),
('jane_doe', 'password123', 'jane@example.com', 'member'),
('admin_user', 'adminpass', 'admin@example.com', 'admin'),
('Siddharth_Natamai', 'test', 'siddharth@example.com', 'member'),
('Alex_Smith', 'password123', 'alex@example.com', 'member'),
('Mia_Wong', 'password123', 'mia@example.com', 'member'),
('Carlos_Ray', 'password123', 'carlos@example.com', 'member'),
('Elena_Rodriguez', 'password123', 'elena@example.com', 'trainer'),
('Michael_Chen', 'password123', 'michael@example.com', 'trainer'),
('Linda_Kim', 'password123', 'linda@example.com', 'trainer');

-- Inserting sample members
INSERT INTO members (user_id, name, fitness_goal, health_metrics) VALUES
(1, 'John Doe', 'Lose 10kg in 12 weeks', 'BMI: 25, Body Fat: 20%'),
(2, 'Jane Doe', 'Run 5km in under 30 minutes', 'BMI: 22, Body Fat: 18%'),
(3, 'Admin User', 'Increase muscle mass', 'BMI: 24, Body Fat: 15%'),
(4, 'Siddharth Natamai', 'Complete a marathon', 'BMI: 23, Body Fat: 15%'),
(5, 'Alex Smith', 'Gain 5kg of muscle', 'BMI: 21, Body Fat: 12%'),
(6, 'Mia Wong', 'Run a half marathon', 'BMI: 20, Body Fat: 18%'),
(7, 'Carlos Ray', 'Lose 15kg', 'BMI: 30, Body Fat: 25%');


-- Inserting sample trainers
INSERT INTO trainers (user_id, name, specialty) VALUES
(8, 'Elena Rodriguez', 'Yoga and Pilates'),
(9, 'Michael Chen', 'Weightlifting'),
(10, 'Linda Kim', 'Cardio Fitness');

-- Inserting sample equipment
INSERT INTO equipment (name, status) VALUES
('Treadmill', 'available'),
('Elliptical', 'available'),
('Dumbbells', 'maintenance'),
('Yoga Mats', 'available'),
('Stationary Bike', 'maintenance'),
('Kettlebells', 'available');

-- Corrected Inserting sample schedule for personal training sessions
INSERT INTO schedule (trainer_id, member_id, start_time, end_time) VALUES
(2, 1, '2024-03-15 09:00:00', '2024-03-15 10:00:00'),
(3, 2, '2024-03-16 10:00:00', '2024-03-16 11:00:00'),
(1, 4, '2024-03-17 09:00:00', '2024-03-17 10:00:00');

-- Inserting sample rooms
INSERT INTO rooms (name, capacity) VALUES
('Yoga Studio', 20),
('Spin Room', 15);

-- Inserting sample room bookings for group fitness classes
INSERT INTO booking (member_id, room_id, booking_date, start_time, end_time) VALUES
(1, 1, '2024-03-20', '09:00', '10:00'),
(2, 2, '2024-03-20', '10:00', '11:00');

-- Inserting sample class schedules for group fitness classes
INSERT INTO class_schedule (name, trainer_id, room_id, class_date, start_time, end_time) VALUES
('Morning Yoga', 1, 1, '2024-03-20', '09:00', '10:00'),
('Spin Class', 2, 2, '2024-03-20', '10:00', '11:00'),
('Evening Pilates', 1, 1, '2024-03-25', '18:00', '19:00'),
('Morning Weightlifting', 2, 2, '2024-03-26', '07:00', '08:00');

-- Inserting sample payments
INSERT INTO payment (member_id, amount, payment_date) VALUES
(1, 50.00, '2024-03-01'),
(2, 75.00, '2024-03-01'),
(3, 60.00, '2024-03-02'),
(4, 80.00, '2024-03-02');

-- Inserting sample feedback
INSERT INTO feedback (member_id, content, submission_date) VALUES
(1, 'Loved the Morning Yoga class!', '2024-03-21'),
(2, 'The Spin Class was intense but rewarding.', '2024-03-21'),
(3, 'The Evening Pilates class was so relaxing and rejuvenating.', '2024-03-22'),
(4, 'Loved the intensity of the Morning Weightlifting session!', '2024-03-22');

-- Adding sample data for exercise routines
INSERT INTO exercise_routines (member_id, routine_details) VALUES
(1, 'Cardio: 30 minutes treadmill, Strength: 20 minutes weight lifting'),
(2, 'Yoga: 45 minutes morning session, Cardio: 15 minutes cycling'),
(4, 'Running: 10km daily, Strength: 30 minutes circuit training');

-- Adding sample data for fitness achievements
INSERT INTO fitness_achievements (member_id, achievement_details, achievement_date) VALUES
(1, 'Completed 10km run in 50 minutes', '2024-03-10'),
(2, 'Achieved goal of 5 pull-ups in a row', '2024-03-15'),
(4, 'Finished half-marathon in 1 hour 45 minutes', '2024-04-05');
