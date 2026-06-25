CREATE TABLE IF NOT EXISTS investment_sources(
  id         VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  name       VARCHAR(100) NOT NULL,
  code       VARCHAR(10) NOT NULL,
  logo       VARCHAR(255)
);

INSERT INTO investment_sources(id, name, code, logo) VALUES
  ('69914d7b-3c78-42e9-9227-b7d53bd5555f', 'Banco do Brasil', 'BB', 'banco-do-brasil.png'),
  ('f41fb090-5fc4-4dbc-bd5e-8b19619446fa', 'Caixa EconÃ´mica Federal', 'CAIXA', 'caixa.png'),
  ('d2c60con-7a19-4b77-83a1-8ef213736bae', 'Banco Inter', 'Inter', 'banco-inter.png'),
  ('f5e63648-3f32-40b3-afe4-2d4a2b6e72b7', 'ItaÃº Unibanco', 'ItaÃº', 'itau.png'),
  ('5fb88215-eb40-4606-842c-236d686eda9f', 'XP Investimentos', 'XP', 'xp.png'),
  ('22b8c861-cca0-4037-9188-3b0a1a0eec74', 'BTG Pactual', 'BTG', 'btg.png'),
  ('1c6e5db1-fcd2-4c20-a324-00de8aa2939b', 'Nubank', 'Nu', 'nubank.png'),
  ('bc27c0a6-dbe9-41d5-abea-75489a273adc', 'PicPay', 'PicPay', 'picpay.png'),
  ('e39fda7c-4320-4dfc-96e3-6a18c9f0e19d', 'Binance', 'Binance', 'binance.png'),
  ('56fbb26c-0ef2-482c-a4be-dfed13a803ea', 'Ripio', 'Ripio', 'ripio.jpg');