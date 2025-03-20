CREATE TABLE IF NOT EXISTS investment_rentabilities(
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  name       VARCHAR(20) NOT NULL
);

INSERT INTO investment_rentabilities(name) VALUES
  ('IPCA'),
  ('IPCA + %% a.a'),
  ('SELIC'),
  ('SELIC + %% a.a'),
  ('%% a.a'),
  ('CDI');
