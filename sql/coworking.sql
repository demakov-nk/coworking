----- 1 уровень -----

CREATE TABLE gender (
    gender_id SMALLSERIAL PRIMARY KEY,
    gender VARCHAR(3) NOT NULL UNIQUE
);

CREATE TABLE extra_service_type (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE room_type (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(40) NOT NULL UNIQUE
);

CREATE TABLE open_space_zone_type (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE open_space (
    open_space_id SERIAL PRIMARY KEY,
    area DECIMAL(5, 1) NOT NULL CHECK (area > 0),
    capacity INTEGER NOT NULL CHECK (capacity > 0)
);

----- 2 уровень -----

CREATE TABLE administrator (
    admin_id SERIAL PRIMARY KEY,
    surname VARCHAR(60) NOT NULL,
    name VARCHAR(50) NOT NULL,
    birthday DATE NOT NULL,
    gender SMALLINT NOT NULL REFERENCES gender (gender_id),
    salary DECIMAL(9, 2) NOT NULL CHECK (salary > 0),
    start_working_date DATE NOT NULL
);

CREATE TABLE room (
    room_id SERIAL PRIMARY KEY,
    type_id INTEGER NOT NULL REFERENCES room_type (type_id),
    area DECIMAL(4, 1) NOT NULL CHECK (area > 0),
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    is_busy BOOLEAN DEFAULT FALSE
);
CREATE INDEX idx_room_type_id ON room (type_id);

CREATE TABLE open_space_structure (
    addition_id SERIAL PRIMARY KEY,
    open_space_id INTEGER NOT NULL REFERENCES open_space (open_space_id),
    zone_type_id INTEGER NOT NULL REFERENCES open_space_zone_type (type_id)
);
CREATE INDEX idx_open_space_structure_open_space_id ON open_space_structure (open_space_id);
CREATE INDEX idx_open_space_structure_zone_type_id ON open_space_structure (zone_type_id);

----- 3 уровень -----

CREATE TABLE client (
    client_id SERIAL PRIMARY KEY,
    surname VARCHAR(60) NOT NULL,
    name VARCHAR(50) NOT NULL,
    birthday DATE NOT NULL,
    gender SMALLINT NOT NULL REFERENCES gender (gender_id),
    email VARCHAR(254) NOT NULL UNIQUE,
    phone VARCHAR(13) NOT NULL UNIQUE,
    admin_id INTEGER NOT NULL REFERENCES administrator (admin_id)
);
CREATE INDEX idx_client_admin_id ON client (admin_id);

----- 4 уровень -----

CREATE TABLE subscription (
    subscription_id SERIAL PRIMARY KEY,
    purchase_date DATE NOT NULL,
    cost DECIMAL(8, 2) NOT NULL CHECK (cost > 0),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    admin_id INTEGER NOT NULL REFERENCES administrator (admin_id),
    client_id INTEGER NOT NULL REFERENCES client (client_id),

    CONSTRAINT purchase_before_start_before_end
        CHECK (purchase_date <= start_date
               AND
               start_date <= end_date)
);
CREATE INDEX idx_subscription_admin_id ON subscription (admin_id);
CREATE INDEX idx_subscription_client_id ON subscription (client_id);

CREATE TABLE extra_service (
    extra_service_id SERIAL PRIMARY KEY,
    purchase_date DATE DEFAULT CURRENT_DATE,
    cost DECIMAL(8, 2) NOT NULL CHECK (cost > 0),
    type_id INTEGER NOT NULL REFERENCES extra_service_type (type_id),
    client_id INTEGER NOT NULL REFERENCES client (client_id)
);
CREATE INDEX idx_extra_service_type_id ON extra_service (type_id);
CREATE INDEX idx_extra_service_client_id ON extra_service (client_id);

----- 5 уровень -----

CREATE TABLE agreement (
    agreement_id SERIAL PRIMARY KEY,
    conclusion_date DATE DEFAULT CURRENT_DATE,
    end_time TIMESTAMP NOT NULL,
    cost DECIMAL(8, 2) CHECK (cost > 0),
    admin_id INTEGER NOT NULL REFERENCES administrator (admin_id),
    client_id INTEGER NOT NULL REFERENCES client (client_id),
    room_id INTEGER REFERENCES room (room_id),
    open_space_id INTEGER REFERENCES open_space (open_space_id),
    subscription_id INTEGER REFERENCES subscription (subscription_id),

    CONSTRAINT only_one_space
        CHECK (
            room_id IS NOT NULL AND open_space_id IS NULL
            OR
            room_id IS NULL AND open_space_id IS NOT NULL
        ),
    CONSTRAINT conclusion_before_end
        CHECK (conclusion_date <= end_time)
);
CREATE INDEX idx_agreement_admin_id ON agreement (admin_id);
CREATE INDEX idx_agreement_client_id ON agreement (client_id);
CREATE INDEX idx_agreement_room_id ON agreement (room_id);
CREATE INDEX idx_agreement_open_space_id ON agreement (open_space_id);
CREATE INDEX idx_agreement_subscription_id ON agreement (subscription_id);

----- 6 уровень -----

CREATE TABLE bill (
    bill_id SERIAL PRIMARY KEY,
    cost DECIMAL(8, 2) NOT NULL CHECK (cost > 0),
    invoice_date DATE DEFAULT CURRENT_DATE,
    closing_period INTERVAL DEFAULT '5 days',
    closing_date TIMESTAMP,
    client_id INTEGER NOT NULL REFERENCES client (client_id),
    admin_id INTEGER NOT NULL REFERENCES administrator (admin_id),
    agreement_id INTEGER REFERENCES agreement (agreement_id),
    subscription_id INTEGER REFERENCES subscription (subscription_id),
    extra_service_id INTEGER REFERENCES extra_service (extra_service_id),

    CONSTRAINT only_one_service
        CHECK (
            agreement_id IS NOT NULL AND subscription_id IS NULL AND extra_service_id IS NULL
            OR
            agreement_id IS NULL AND subscription_id IS NOT NULL AND extra_service_id IS NULL
            OR
            agreement_id IS NULL AND subscription_id IS NULL AND extra_service_id IS NOT NULL
        ),
    CONSTRAINT invoice_before_closing
        CHECK (invoice_date <= closing_date)
);
CREATE INDEX idx_bill_client_id ON bill (client_id);
CREATE INDEX idx_bill_admin_id ON bill (admin_id);
CREATE INDEX idx_bill_agreement_id ON bill (agreement_id);
CREATE INDEX idx_bill_subscription_id ON bill (subscription_id);
CREATE INDEX idx_bill_extra_service_id ON bill (extra_service_id);

CREATE TABLE visit (
    visit_id SERIAL PRIMARY KEY,
    activity_status BOOLEAN DEFAULT TRUE,
    entrance_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    exit_time TIMESTAMP,
    client_id INTEGER NOT NULL REFERENCES client (client_id),
    admin_id INTEGER NOT NULL REFERENCES administrator (admin_id),
    agreement_id INTEGER NOT NULL REFERENCES agreement (agreement_id),

    CONSTRAINT exit_after_entrance 
        CHECK (exit_time IS NULL OR exit_time >= entrance_time)
);
CREATE INDEX idx_visit_client_id ON visit (client_id);
CREATE INDEX idx_visit_admin_id ON visit (admin_id);
CREATE INDEX idx_visit_agreement_id ON visit (agreement_id);
