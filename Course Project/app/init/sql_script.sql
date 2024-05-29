CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_login VARCHAR(255) UNIQUE,
    user_name VARCHAR(255),
    user_surname VARCHAR(255),
    user_password VARCHAR(255)
);

CREATE INDEX user_id_index ON users (user_id);
CREATE INDEX user_login_index ON users (user_login);
CREATE INDEX user_name_index ON users (user_name);
CREATE INDEX user_surname_index ON users (user_surname);
