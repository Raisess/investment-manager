CREATE TABLE IF NOT EXISTS investment_types(
  id         VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  name       VARCHAR(100),
  code       VARCHAR(20),
  color      VARCHAR(6)
);

INSERT INTO investment_types(id, name, code, color) VALUES
  ('22704dcd-c8c9-4b1d-9e90-79d0d4d0f407', 'Poupança', 'POUPANÇA', '217ac8'),
  ('e1606bfc-c0a1-424f-a3c1-7192697a89d3', 'Renda Fixa', 'RENDA FIXA', '46ae13'),
  ('6dd45eff-bc10-4dbe-8bed-eaa9d273ad86', 'Renda Variável', 'VARIÁVEL', 'ec172b'),
  ('4738627d-a846-4373-95ea-cf2562b74b0a', 'Tesouro Direto', 'TESOURO', 'e3a90b'),
  ('548fd3bc-e20c-4741-bf48-29e4f6497755', 'Cryptomoeda', 'CRYPTO', 'f47b0f'),
  ('67c5d522-89e4-49cb-aa84-6fa67f107390', 'Fundo de investimento', 'FUNDO', '0a0a0a'),
  ('43c0e1d3-d9fd-4b7b-8897-36eb55816b87', 'Saldo + CDI', 'SALDO', '21c25e');
