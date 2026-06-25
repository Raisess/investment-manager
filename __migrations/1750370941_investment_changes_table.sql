CREATE TABLE IF NOT EXISTS investment_changes(
  id                 VARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  created_at         DATE DEFAULT CURRENT_TIMESTAMP,
  investment_id      VARCHAR(36) NOT NULL,
  change             DECIMAL NOT NULL,

  CONSTRAINT fk_investment
    FOREIGN KEY(investment_id)
      REFERENCES investments(id)
      ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS find_by_investment ON investment_changes(investment_id);
