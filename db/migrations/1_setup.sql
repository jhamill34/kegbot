CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  rfid VARCHAR UNIQUE,
  name VARCHAR,
  tokens INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE kegs (
  id SERIAL PRIMARY KEY,
  name VARCHAR UNIQUE,
  pints DECIMAL,
  starting_pints DECIMAL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP
);
