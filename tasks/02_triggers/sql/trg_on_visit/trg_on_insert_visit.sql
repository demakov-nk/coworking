-- 7. Добавление визита

CREATE OR REPLACE FUNCTION on_insert_visit()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE client_stats
    SET visits = visits + 1
    WHERE client_id = NEW.client_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_on_insert_visit
AFTER INSERT ON visit
FOR EACH ROW
EXECUTE FUNCTION on_insert_visit();
