CREATE TABLE IF NOT EXISTS users(
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  name       VARCHAR(150) NOT NULL,
  email      VARCHAR(150) NOT NULL,
  picture    VARCHAR(255) NOT NULL,
  status     SMALLINT DEFAULT 1
);
