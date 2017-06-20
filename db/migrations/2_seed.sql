INSERT INTO users (rfid, name, tokens, created_at, updated_at)
VALUES
  ('123,456,789,098', 'Josh', 5, now(), now()),
  ('234,567,890,987', 'Ty', 3, now(), now()),
  ('345,678,909,876', 'Robert', 1, now(), now());

INSERT INTO kegs (name, pints, starting_pints, created_at, updated_at)
VALUES
  ('Old Porter', 43.0, 50.0, now(), now()),
  ('IPA', 21.0, 50.0, now(), now()),
  ('Amber Ale', 33.0, 50.0, now(), now());
