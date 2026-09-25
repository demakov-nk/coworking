-- 6. Удаление абонемента

CREATE OR REPLACE FUNCTION on_delete_sub()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE client_stats
    SET subs = subs - 1
    WHERE client_id = OLD.client_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_on_delete_sub
AFTER DELETE ON subscription
FOR EACH ROW
EXECUTE FUNCTION on_delete_sub();
