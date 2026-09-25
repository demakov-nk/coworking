-- 2. Изменение имени клиента

CREATE OR REPLACE FUNCTION on_update_client_name()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE client_stats
    SET name = NEW.name
    WHERE client_id = NEW.client_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_on_update_client_name
AFTER UPDATE OF name ON client
FOR EACH ROW
EXECUTE FUNCTION on_update_client_name();