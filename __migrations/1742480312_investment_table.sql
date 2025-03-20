CREATE TABLE IF NOT EXISTS investments(
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at         TIMESTAMP DEFAULT now(),
  updated_at         TIMESTAMP DEFAULT now(),
  user_id            UUID NOT NULL,
  source_id          UUID NOT NULL,
  type_id            UUID NOT NULL,
  name               VARCHAR(50) NOT NULL,
  invested           DECIMAL NOT NULL,
  total              DECIMAL NOT NULL,
  maturity           DATE,
  rentability_id     UUID,
  rentability_number DECIMAL,

  CONSTRAINT fk_user
    FOREIGN KEY(user_id)
      REFERENCES users(id)
      ON DELETE CASCADE,

  CONSTRAINT fk_source
    FOREIGN KEY(source_id)
      REFERENCES investment_sources(id)
      ON DELETE CASCADE,

  CONSTRAINT fk_type
    FOREIGN KEY(type_id)
      REFERENCES investment_types(id)
      ON DELETE CASCADE,

  CONSTRAINT fk_rentability
    FOREIGN KEY(rentability_id)
      REFERENCES investment_rentabilities(id)
      ON DELETE CASCADE
);

CREATE INDEX get_by_user_id ON investments(user_id);
