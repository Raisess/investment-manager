CREATE TABLE IF NOT EXISTS investment_rentabilities(
  id         VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  name       VARCHAR(20) NOT NULL
);

INSERT INTO investment_rentabilities(id, name) VALUES
  ('bed67de6-a427-4d42-8970-85ccfc7da932', 'IPCA'),
  ('22101414-68b6-4d23-a8bb-7b9c72f44843', 'IPCA + %% a.a'),
  ('d95b6f39-8c8a-4ab7-af58-4b742553971b', 'SELIC'),
  ('5d87ade2-2cd6-476d-aaeb-0c51eb58a20a', 'SELIC + %% a.a'),
  ('37d9a84f-7c64-4568-b87e-7c1b4a7c28fd', '%% a.a'),
  ('741de8f4-0d2e-44cb-a445-bdf931d993fc', 'CDI');
