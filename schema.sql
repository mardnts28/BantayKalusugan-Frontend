CREATE DATABASE vital_signs_db;

\c vital_signs_db;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vital records table with approval workflow
CREATE TABLE vital_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    heart_rate INTEGER CHECK (heart_rate > 0 AND heart_rate < 300),
    blood_pressure_systolic INTEGER CHECK (blood_pressure_systolic > 50 AND blood_pressure_systolic < 250),
    blood_pressure_diastolic INTEGER CHECK (blood_pressure_diastolic > 30 AND blood_pressure_diastolic < 200),
    temperature DECIMAL(4,1) CHECK (temperature > 30 AND temperature < 45),
    oxygen_saturation INTEGER CHECK (oxygen_saturation >= 0 AND oxygen_saturation <= 100),
    respiratory_rate INTEGER CHECK (respiratory_rate > 0 AND respiratory_rate < 100),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    admin_notes TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    reviewed_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_vital_records_user_id ON vital_records(user_id);
CREATE INDEX idx_vital_records_status ON vital_records(status);
CREATE INDEX idx_users_email ON users(email);
