CREATE TABLE IF NOT EXISTS investment_rentabilities(
  id         VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  name       VARCHAR(20) NOT NULL
);

INSERT INTO investment_rentabilities(id, name) VALUES
  ('bed67de6-a427-4d42-8970-85ccfc7da932', 'IPCA'),
  ('b7ec23d6-1318-4510-a884-984f866ea2f1', 'IPCA + %% a.a'),
  ('d95b6f39-8c8a-4ab7-af58-4b742553971b', 'SELIC'),
  ('4eae2572-2741-47db-89ed-17e81cc2286a', 'SELIC + %% a.a'),
  ('37d9a84f-7c64-4568-b87e-7c1b4a7c28fd', '%% a.a'),
  ('8eccbbb1-004b-4953-a516-31f8264dd8ab', 'CDI');
