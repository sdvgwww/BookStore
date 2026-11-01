CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE publishers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    cover_path VARCHAR(500),
    rating NUMERIC(3,2) DEFAULT 0,
    cost NUMERIC(10,2) NOT NULL CHECK (cost >= 0),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    publish_date DATE NOT NULL,
    is_ebook BOOLEAN DEFAULT FALSE,
    genre_id INTEGER REFERENCES genres(id),
    publisher_id INTEGER REFERENCES publishers(id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('guest','seller','manager','admin'))
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    delivery_date DATE NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'новый',
    manager_id INTEGER REFERENCES users(id)
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE RESTRICT,
    qty INTEGER NOT NULL CHECK (qty > 0),
    price NUMERIC(10,2) NOT NULL
);