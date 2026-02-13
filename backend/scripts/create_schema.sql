CREATE SCHEMA IF NOT EXISTS online_shop;

CREATE TABLE IF NOT EXISTS online_shop.users (
    user_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    address TEXT,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS online_shop.cart (
    cart_id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES online_shop.users(user_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS online_shop.categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INT REFERENCES online_shop.categories(category_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS online_shop.suppliers (
    supplier_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS online_shop.products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INT NOT NULL REFERENCES online_shop.categories(category_id),
    supplier_id INT NOT NULL REFERENCES online_shop.suppliers(supplier_id)
);

CREATE TABLE IF NOT EXISTS online_shop.product_versions (
    version_id INT PRIMARY KEY,
    product_id INT NOT NULL REFERENCES online_shop.products(product_id),
    price DECIMAL(10,2) NOT NULL,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    valid_from TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP
);

CREATE TABLE IF NOT EXISTS online_shop.pickup_points (
    pickup_point_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    working_hours VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS online_shop.cart_items (
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (cart_id, product_id),
    FOREIGN KEY (cart_id) REFERENCES online_shop.users(user_id),
    FOREIGN KEY (product_id) REFERENCES online_shop.products(product_id)
);

CREATE TABLE IF NOT EXISTS online_shop.reviews (
    review_id INT PRIMARY KEY,
    product_id INT NOT NULL REFERENCES online_shop.products(product_id),
    user_id INT NOT NULL REFERENCES online_shop.users(user_id),
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS online_shop.payments (
    payment_id INT PRIMARY KEY,
    payment_method VARCHAR(100) NOT NULL,
    status VARCHAR(100) NOT NULL DEFAULT 'pending',
    payment_date TIMESTAMP,
    transaction_id VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS online_shop.orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES online_shop.users(user_id),
    status VARCHAR(100) NOT NULL DEFAULT 'processing',
    total_price DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    pickup_point_id INT NOT NULL REFERENCES online_shop.pickup_points(pickup_point_id),
    payment_id INT NOT NULL REFERENCES online_shop.payments(payment_id)
);


CREATE TABLE IF NOT EXISTS online_shop.order_items (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES online_shop.orders(order_id),
    FOREIGN KEY (product_id) REFERENCES online_shop.products(product_id),
    version_id INT NOT NULL REFERENCES online_shop.product_versions(version_id),
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0)
                                                   );
