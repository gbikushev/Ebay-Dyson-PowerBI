-- Schema for Azure SQL (T-SQL)

DROP TABLE IF EXISTS seller_item_performance;
DROP TABLE IF EXISTS sellers;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS conditions;
DROP TABLE IF EXISTS categories;

-- Categories Table
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name NVARCHAR(MAX) NOT NULL
);

-- Conditions Table
CREATE TABLE conditions (
    condition_id INT PRIMARY KEY,
    condition_name NVARCHAR(MAX) NOT NULL
);

-- Countries Table
CREATE TABLE countries (
    country_id NVARCHAR(10) PRIMARY KEY,
    country_name NVARCHAR(MAX) NOT NULL
);

-- Items Table
CREATE TABLE items (
    item_id NVARCHAR(50) PRIMARY KEY,
    title NVARCHAR(MAX) NOT NULL,
    brand NVARCHAR(MAX) NOT NULL,
    url NVARCHAR(MAX) NOT NULL,
    category_id INT NOT NULL,
    condition_id INT NOT NULL,
    item_location_country_id NVARCHAR(10) NOT NULL,
    item_location_city NVARCHAR(MAX),
    marketplace_id NVARCHAR(50) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (condition_id) REFERENCES conditions(condition_id),
    FOREIGN KEY (item_location_country_id) REFERENCES countries(country_id)
);

-- Prices Table
CREATE TABLE prices (
    item_id NVARCHAR(50) NOT NULL,
    price_usd DECIMAL(18, 2) NOT NULL,
    original_price_usd DECIMAL(18, 2),
    discount_percentage DECIMAL(5, 2),
    discount_amount_usd DECIMAL(18, 2),
    shipping_cost_usd DECIMAL(18, 2),
    date_time DATETIME2 NOT NULL,
    PRIMARY KEY (item_id, date_time),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- Reviews Table
CREATE TABLE reviews (
    review_id INT PRIMARY KEY IDENTITY(1,1),
    item_id NVARCHAR(50) NOT NULL,
    reviewer_name NVARCHAR(MAX) NOT NULL,
    reviewer_score INT,
    review_text NVARCHAR(MAX) NOT NULL,
    review_date DATETIME2 NOT NULL,
    review_type NVARCHAR(10) CHECK (review_type IN ('Positive', 'Negative', 'Neutral')),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- Sellers Table
CREATE TABLE sellers (
    seller_id INT PRIMARY KEY IDENTITY(1,1),
    seller_username NVARCHAR(MAX) NOT NULL,
    seller_feedback_score INT NOT NULL,
    seller_positive_feedback_percentage DECIMAL(5, 2) NOT NULL
);

-- Seller Item Performance Table
CREATE TABLE seller_item_performance (
    item_id NVARCHAR(50) NOT NULL,
    seller_id INT NOT NULL,
    number_sold INT NOT NULL,
    number_available INT,
    reviews_num INT NOT NULL,
    item_positive_feedback_percentage DECIMAL(5, 2),
    date_time DATETIME2 NOT NULL,
    PRIMARY KEY (item_id, seller_id, date_time),
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
