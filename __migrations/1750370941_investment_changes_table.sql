CREATE TABLE IF NOT EXISTS investment_changes(
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at         TIMESTAMP DEFAULT now(),
  investment_id      UUID NOT NULL,
  change             DECIMAL NOT NULL,

  CONSTRAINT fk_investment
    FOREIGN KEY(investment_id)
      REFERENCES investments(id)
      ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS find_by_investment ON investment_changes(investment_id);
