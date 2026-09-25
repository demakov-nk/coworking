/*
Для клиента А 
посчитать число абонементов,
в которых оплачивалась дополнительная услуга Б

*** нельзя WITH

*/


-- WITH cli_type_sub AS (
--     SELECT sub.client_id, est.type_id, sub.subscription_id
--     FROM subscription sub 
--         JOIN extra_service es 
--             ON sub.client_id = es.client_id
--                 AND es.client_id = 1580
--                 AND es.type_id = 5
--                 AND es.purchase_date BETWEEN sub.start_date AND sub.end_date
--         JOIN extra_service_type est ON es.type_id = est.type_id
-- )
-- SELECT client_id, type_id, COUNT(subscription_id) AS sub_count
-- FROM cli_type_sub
-- GROUP BY client_id, type_id


SELECT cli.client_id,
       cli.surname, 
       cli.name,
       est.type_name,
       COUNT(sub.subscription_id) AS subs
FROM client cli
    JOIN extra_service es 
        ON es.client_id = cli.client_id
        AND cli.surname = 'Мамонтова'
        AND cli.name = 'Лора'
    JOIN extra_service_type est 
        ON est.type_id = es.type_id
        AND est.type_name = 'капучино'
    JOIN subscription sub
        ON sub.client_id = cli.client_id
        AND es.purchase_date BETWEEN sub.start_date AND sub.end_date
GROUP BY cli.client_id, cli.surname, cli.name, est.type_name;

