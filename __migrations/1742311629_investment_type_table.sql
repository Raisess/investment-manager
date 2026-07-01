CREATE TABLE IF NOT EXISTS investment_types(
  id         VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  name       VARCHAR(100),
  code       VARCHAR(20),
  color      VARCHAR(6)
);

INSERT INTO investment_types(id, name, code, color) VALUES
  ('e5cb0352-7eef-4b55-b6f6-afae5e6d0170', 'Poupança', 'POUPANÇA', '217ac8'),
  ('33e7977f-da62-4752-8de6-63fc925bf0c4', 'Renda Fixa', 'RENDA FIXA', '46ae13'),
  ('6dd45eff-bc10-4dbe-8bed-eaa9d273ad86', 'Renda Variável', 'VARIÁVEL', 'ec172b'),
  ('1d4e58cf-6405-48a7-ac4f-d666438c55cc', 'Tesouro Direto', 'TESOURO', 'e3a90b'),
  ('548fd3bc-e20c-4741-bf48-29e4f6497755', 'Cryptomoeda', 'CRYPTO', 'f47b0f'),
  ('67c5d522-89e4-49cb-aa84-6fa67f107390', 'Fundo de investimento', 'FUNDO', '0a0a0a'),
  ('43c0e1d3-d9fd-4b7b-8897-36eb55816b87', 'Saldo + CDI', 'SALDO', '21c25e');
