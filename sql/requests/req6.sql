/*
Найти клиентов, которые приобрели
больше абонементов, чем
клиент А

*** нельзя WITH

*/

WITH cli_sub_count AS (
    SELECT client_id, COUNT(subscription_id) AS sub_count
    FROM subscription
    GROUP BY client_id
)
SELECT client_id, sub_count
FROM cli_sub_count
WHERE sub_count > (
    SELECT csc.sub_count
    FROM cli_sub_count csc
    WHERE client_id = 1003
);

SELECT client_id, COUNT(subscription_id) AS sub_count
FROM subscription
WHERE client_id = 1003
GROUP BY client_id
