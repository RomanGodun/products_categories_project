CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE IF NOT EXISTS product
(
    id UUID DEFAULT uuid_generate_v4() NOT NULL,
    create_at TIMESTAMP DEFAULT NOW() NOT NULL,
    edit_at TIMESTAMP DEFAULT NOW() NOT NULL,
    title CHARACTER VARYING(100) NOT NULL,
    flammable BOOLEAN NOT NULL,
    price INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS category
(
    id UUID DEFAULT uuid_generate_v4() NOT NULL,
    create_at TIMESTAMP DEFAULT NOW() NOT NULL,
    edit_at TIMESTAMP DEFAULT NOW() NOT NULL,
    title CHARACTER VARYING(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS product_to_category
(
    id UUID DEFAULT uuid_generate_v4() NOT NULL,
    create_at TIMESTAMP DEFAULT NOW() NOT NULL,
    edit_at TIMESTAMP DEFAULT NOW() NOT NULL,
    product_id UUID REFERENCES product (id),
    category_id UUID REFERENCES category (id),
    PRIMARY KEY (product_id, category_id)
);

INSERT INTO product (title, flammable, price)
VALUES
('product_1', True, 50),
('product_2', False, 50),
('product_3', True, 51),
('product_4', True, 52),
('product_5', False, 53),
('product_6', False, 54),
('product_7', True, 55),
('product_8', False, 51),
('product_9', False, 50);

INSERT INTO category (title)
VALUES
('category_1'),
('category_2'),
('category_3'),
('category_4');