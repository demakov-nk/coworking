-- 1. Добавление нового клиента

CREATE OR REPLACE FUNCTION on_insert_client()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO client_stats (client_id, surname, name, subs, visits)
    VALUES (NEW.client_id, NEW.surname, NEW.name, 0, 0);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trg_on_insert_client
AFTER INSERT ON client
FOR EACH ROW
EXECUTE FUNCTION on_insert_client();