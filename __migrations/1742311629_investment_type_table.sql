CREATE TABLE IF NOT EXISTS investment_types(
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  name       VARCHAR(100),
  code       VARCHAR(20),
  color      VARCHAR(6)
);

INSERT INTO investment_types(name, code, color) VALUES
  ('Poupança', 'POUPANÇA', '217ac8'),
  ('Renda Fixa', 'RENDA FIXA', '46ae13'),
  ('Renda Variável', 'VARIÁVEL', 'ec172b'),
  ('Tesouro Direto', 'TESOURO', 'e3a90b'),
  ('Cryptomoeda', 'CRYPTO', 'f47b0f'),
  ('Fundo de investimento', 'FUNDO', '0a0a0a'),
  ('Saldo + CDI', 'SALDO', '21c25e');
