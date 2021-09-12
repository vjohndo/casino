-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    password_hash TEXT,
    wallet INTEGER,
    is_admin BOOLEAN,
    last_login DATE
);


INSERT INTO users (name, email, password_hash, wallet, is_admin) VALUES ('john', 'john@email.com', 'password_hash', 1000, TRUE);
INSERT INTO users (name, email, password_hash, wallet, is_admin) VALUES ('testperson', 'testperson@email.com', 'password_hash', 1000, FALSE);

-- Played_games
CREATE TABLE played_games (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    game_id INTEGER,
    bet_amount INTEGER,
    pickled_game BYTEA,
    game_over BOOLEAN,
    result INTEGER
);



-- Vault
CREATE TABLE vault (
    id SERIAL PRIMARY KEY,
    cash INTEGER
)



-- Transaction
CREATE TABLE vault (
    id SERIAL PRIMARY KEY,
    game_id INTEGER
    user_id INTEGER,
    vault_id INTEGER,
    credit INTEGER
)



-- Game_types... chucking 
CREATE TABLE game_types (
    id SERIAL PRIMARY KEY,
    name = TEXT
)


