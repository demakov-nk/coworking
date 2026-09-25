/* 1. Для каждого клиента посчитать число абонементов и число визитов. */
CREATE OR REPLACE VIEW client_stats_view AS
SELECT cli.client_id,
       cli.surname,
       cli.name,
       client_subs.subs,
       client_visits.visits
FROM client cli
    LEFT JOIN (
        SELECT client_id, COUNT(*) AS subs
        FROM subscription
        GROUP BY client_id
    ) client_subs
        ON cli.client_id = client_subs.client_id
    LEFT JOIN (
        SELECT client_id, COUNT(*) AS visits
        FROM visit
        GROUP BY client_id
    ) client_visits
        ON cli.client_id = client_visits.client_id;