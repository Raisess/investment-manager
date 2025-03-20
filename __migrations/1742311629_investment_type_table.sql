CREATE TABLE IF NOT EXISTS investment_types(
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  name       VARCHAR(100),
  code       VARCHAR(20),
  color      VARCHAR(6)
);

INSERT INTO investment_types(name, code, color) VALUES
  ('Poupança', 'POP', '217ac8'),
  ('Certificado de Depósito Bancário', 'CDB', 'a2428e'),
  ('Letra de Crédito', 'LCI/LCA/LCD', '46ae13'),
  ('Tesouro Direto', 'TESOURO', 'e3a90b'),
  ('Ações', 'VAR', 'ec172b'),
  ('Cryptomoeda', 'CRYPTO', '0bb1e3'),
  ('Fundo de investimento', 'FUNDO', '0a0a0a');
