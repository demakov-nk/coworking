-- 4. Удаление клиента

CREATE OR REPLACE FUNCTION on_delete_client()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM client_stats WHERE client_id = OLD.client_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_on_delete_client
AFTER DELETE ON client
FOR EACH ROW
EXECUTE FUNCTION on_delete_client();