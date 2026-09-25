-- 5. Добавление абонемента

CREATE OR REPLACE FUNCTION on_insert_sub()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE client_stats
    SET subs = subs + 1
    WHERE client_id = NEW.client_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_on_insert_sub
AFTER INSERT ON subscription
FOR EACH ROW
EXECUTE FUNCTION on_insert_sub();
