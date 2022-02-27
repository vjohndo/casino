-- Users Table Generation Code
DROP TABLE users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    password_hash TEXT,
    wallet INTEGER,
    is_admin BOOLEAN,
    last_login DATE
);

-- Password is password_hash
INSERT INTO users (name, email, password_hash, wallet, is_admin) VALUES ('john', 'john@email.com', '$2b$12$7EtmDXgelc5YzS4xQc8mH.QrOhKxK.BXwCZQxCFAu.wiJbpQ6mGy6', 1000, TRUE);

-- Game Instances Table Generation Code
DROP TABLE game_instances;

CREATE TABLE game_instances (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    game_mode_id INTEGER,
    bet_amount INTEGER,
    pickled_game BYTEA,
    game_over BOOLEAN,
    result INTEGER,
    CONSTRAINT fk_player FOREIGN KEY(user_id) REFERENCES users(id),
    CONSTRAINT fk_game_mode FOREIGN KEY(game_mode_id) REFERENCES game_modes(id)
);


-- Game Instance Generation Code
CREATE TABLE game_modes (
    id SERIAL PRIMARY KEY,
    name TEXT
);

INSERT INTO game_modes (name) VALUES ('five_card_poker');
INSERT INTO game_modes (name) VALUES ('blackjack');


-- Tables for future expansion
-- -- Vault
-- CREATE TABLE vault (
--     id SERIAL PRIMARY KEY,
--     cash INTEGER
-- )

-- -- Transaction
-- CREATE TABLE vault (
--     id SERIAL PRIMARY KEY,
--     game_id INTEGER
--     user_id INTEGER,
--     vault_id INTEGER,
--     credit INTEGER
-- )