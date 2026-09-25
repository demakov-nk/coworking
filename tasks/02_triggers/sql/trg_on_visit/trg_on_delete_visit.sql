-- 8. Удаление визита

CREATE OR REPLACE FUNCTION on_delete_visit()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE client_stats
    SET visits = visits - 1
    WHERE client_id = OLD.client_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_on_delete_visit
AFTER DELETE ON visit
FOR EACH ROW
EXECUTE FUNCTION on_delete_visit();
