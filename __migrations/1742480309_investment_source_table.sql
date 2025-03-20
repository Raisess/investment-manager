CREATE TABLE IF NOT EXISTS investment_sources(
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  name       VARCHAR(100) NOT NULL,
  code       VARCHAR(10) NOT NULL,
  logo       VARCHAR(255)
);

INSERT INTO investment_sources(name, code, logo) VALUES
  ('Banco Inter', 'Inter', 'banco-inter.png'),
  ('Banco do Brasil', 'BB', 'banco-do-brasil.png'),
  ('Caixa Econômica Federal', 'CAIXA', 'caixa.png'),
  ('Ripio', 'Ripio', 'ripio.jpg');
