/*
Посчитать число абонементов
с
одинаковым количеством счетов.

Построить 2D-гистограмму

*** нельзя WITH

*/

WITH sub_bills AS (
    SELECT subscription_id, COUNT(bill_id) AS bill_count
    FROM bill
    WHERE subscription_id IS NOT NULL
    GROUP BY subscription_id
)
SELECT bill_count, COUNT(*) AS subscription_count
FROM sub_bills
GROUP BY bill_count
ORDER BY bill_count
