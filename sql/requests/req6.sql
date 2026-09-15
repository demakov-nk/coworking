/*
Найти клиентов, которые приобрели
больше абонементов, чем
клиент А

*** нельзя WITH

*/

-- WITH cli_sub_count AS (
--     SELECT client_id, COUNT(subscription_id) AS sub_count
--     FROM subscription
--     GROUP BY client_id
-- )
-- SELECT client_id, sub_count
-- FROM cli_sub_count
-- WHERE sub_count > (
--     SELECT csc.sub_count
--     FROM cli_sub_count csc
--     WHERE client_id = 1003
-- );

SELECT cli.client_id,
       cli.surname, 
       cli.name,
       COUNT(sub.subscription_id) AS subs
FROM client cli
    JOIN subscription sub ON sub.client_id = cli.client_id
GROUP BY cli.client_id, cli.surname, cli.name
HAVING COUNT(sub.subscription_id) > (
    SELECT COUNT(sub.subscription_id)
    FROM client cli
        JOIN subscription sub 
        ON sub.client_id = cli.client_id
        AND cli.surname = 'Самсонова'
        AND cli.name = 'Анна'
    GROUP BY cli.client_id
);

-- SELECT cli.client_id, cli.surname, cli.name, COUNT(sub.subscription_id) AS subs
-- FROM subscription sub
-- JOIN client cli ON sub.client_id = cli.client_id AND cli.client_id = 1003
-- GROUP BY cli.client_id, cli.surname, cli.name
