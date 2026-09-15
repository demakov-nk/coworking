/* 3. Вывести всех администраторов, которые заключали договор об аренде с клиентом, который совершил более 8 визитов. */
SELECT DISTINCT agr.admin_id,
                adm.surname,
                adm.name
FROM client_subs_visits csv
    JOIN agreement agr
        ON csv.client_id = agr.client_id
    JOIN administrator adm
        ON adm.admin_id = agr.admin_id
WHERE csv.visits > 8;
