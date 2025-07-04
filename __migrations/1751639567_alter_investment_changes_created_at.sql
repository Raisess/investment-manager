ALTER TABLE public.investment_changes ALTER COLUMN created_at TYPE date USING created_at::date;
