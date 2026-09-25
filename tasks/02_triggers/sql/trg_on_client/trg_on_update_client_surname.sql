-- 3. Изменение фамилии клиента
CREATE OR REPLACE FUNCTION on_update_client_surname()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE client_stats
    SET surname = NEW.surname
    WHERE client_id = NEW.client_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_on_update_client_surname
AFTER UPDATE OF surname ON client
FOR EACH ROW
EXECUTE FUNCTION on_update_client_surname();