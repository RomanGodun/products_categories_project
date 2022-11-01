CREATE TABLE IF NOT EXISTS products
(
    id SERIAL PRIMARY KEY,
    product_name CHARACTER VARYING(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS categories
(
    id SERIAL PRIMARY KEY,
    category_name CHARACTER VARYING(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS products_categories
(
    id SERIAL PRIMARY KEY,
    product_id integer REFERENCES products (id) NOT NULL,
    category_id integer REFERENCES categories (id) NOT NULL
);

INSERT INTO products (product_name)
VALUES
('product_1'),
('product_2'),
('product_3'),
('product_4'),
('product_5'),
('product_6'),
('product_7'),
('product_8'),
('product_9');

INSERT INTO categories (category_name)
VALUES
('category_1'),
('category_2'),
('category_3'),
('category_4');

INSERT INTO products_categories (product_id, category_id)
VALUES
(1,1),
(3,1),
(5,1),
(2,2),
(4,2),
(6,2),
(6,3),
(7,3);