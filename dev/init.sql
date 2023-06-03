CREATE TABLE IF NOT EXISTS product
(
    id SERIAL PRIMARY KEY,
    create_at TIMESTAMP NOT NULL DEFAULT NOW(),
    edit_at TIMESTAMP NOT NULL DEFAULT NOW(),
    product_name CHARACTER VARYING(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS category
(
    id SERIAL PRIMARY KEY,
    create_at TIMESTAMP NOT NULL DEFAULT NOW(),
    edit_at TIMESTAMP NOT NULL DEFAULT NOW(),
    category_name CHARACTER VARYING(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS product_to_category
(
    id SERIAL,
    create_at TIMESTAMP NOT NULL DEFAULT NOW(),
    edit_at TIMESTAMP NOT NULL DEFAULT NOW(),
    product_id INTEGER REFERENCES product (id),
    category_id INTEGER REFERENCES category (id),
    PRIMARY KEY (product_id, category_id)
);

INSERT INTO product (product_name)
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

INSERT INTO category (category_name)
VALUES
('category_1'),
('category_2'),
('category_3'),
('category_4');

INSERT INTO product_to_category (product_id, category_id)
VALUES
(1,1),
(3,1),
(5,1),
(2,2),
(4,2),
(6,2),
(6,3),
(7,3);