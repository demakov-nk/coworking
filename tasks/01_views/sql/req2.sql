/* 2. Вывести всех клиентов, которые приобрели больше 3 абонементов и совершили более 10 визитов. */
SELECT client_id, surname, name
FROM client_stats_view
WHERE subs > 3 AND visits > 10;