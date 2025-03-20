CREATE TABLE IF NOT EXISTS investment_sources(
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now(),
  name       VARCHAR(100) NOT NULL,
  code       VARCHAR(10) NOT NULL,
  logo       VARCHAR(255)
);

INSERT INTO investment_sources(name, code, logo) VALUES
  ('Banco do Brasil', 'BB', 'banco-do-brasil.png'),
  ('Caixa Econômica Federal', 'CAIXA', 'caixa.png'),
  ('Banco Inter', 'Inter', 'banco-inter.png'),
  ('Itaú Unibanco', 'Itaú', 'itau.png'),
  ('XP Investimentos', 'XP', 'xp.png'),
  ('BTG Pactual', 'BTG', 'btg.png'),
  ('Nubank', 'Nu', 'nubank.png'),
  ('PicPay', 'PicPay', 'picpay.png'),
  ('Binance', 'Binance', 'binance.png'),
  ('Ripio', 'Ripio', 'ripio.jpg');
