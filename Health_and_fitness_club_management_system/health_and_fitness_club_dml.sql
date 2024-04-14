
-- DML for Health and Fitness Club Management System

-- Inserting sample users
INSERT INTO users (username, password, email, role) VALUES
('john_doe', 'password123', 'john@example.com', 'member'),
('jane_doe', 'password123', 'jane@example.com', 'trainer'),
('admin_user', 'adminpass', 'admin@example.com', 'admin');

-- Inserting sample members
INSERT INTO members (user_id, name, fitness_goal, health_metrics) VALUES
(1, 'John Doe', 'Lose 10kg in 12 weeks', 'BMI: 25, Body Fat: 20%'),
(2, 'Jane Smith', 'Run 5km in under 30 minutes', 'BMI: 22, Body Fat: 18%');

-- Inserting sample trainers
INSERT INTO trainers (user_id, name, specialty) VALUES
(2, 'Jane Doe', 'Cardio and Strength Training');

-- Inserting sample equipment
INSERT INTO equipment (name, status) VALUES
('Treadmill', 'available'),
('Elliptical', 'available'),
('Dumbbells', 'maintenance');

-- Inserting sample schedule for personal training sessions
INSERT INTO schedule (trainer_id, member_id, start_time, end_time) VALUES
(1, 1, '2024-03-15 09:00:00', '2024-03-15 10:00:00'),
(1, 2, '2024-03-16 10:00:00', '2024-03-16 11:00:00');

-- Inserting sample room bookings for group fitness classes
INSERT INTO booking (member_id, room_id, booking_date, start_time, end_time) VALUES
(1, 1, '2024-03-20', '09:00', '10:00'),
(2, 1, '2024-03-20', '10:00', '11:00');

-- Inserting sample rooms
INSERT INTO rooms (name, capacity) VALUES
('Yoga Studio', 20),
('Spin Room', 15);

-- Inserting sample class schedules for group fitness classes
INSERT INTO class_schedule (name, trainer_id, room_id, class_date, start_time, end_time) VALUES
('Morning Yoga', 1, 1, '2024-03-20', '09:00', '10:00'),
('Spin Class', 1, 2, '2024-03-20', '10:00', '11:00');

-- Inserting sample payments
INSERT INTO payment (member_id, amount, payment_date) VALUES
(1, 50.00, '2024-03-01'),
(2, 75.00, '2024-03-01');

-- Inserting sample feedback
INSERT INTO feedback (member_id, content, submission_date) VALUES
(1, 'Loved the Morning Yoga class!', '2024-03-21'),
(2, 'The Spin Class was intense but rewarding.', '2024-03-21');

-- Ensure sample data covers all aspects of the application's functionality
