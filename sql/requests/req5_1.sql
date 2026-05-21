/*
Найти рабочие пространства, в которых
было максимальное количество договоров

*** нельзя WITH

*/

WITH os_agr_count AS (
    SELECT os.open_space_id,
           COUNT(agr.agreement_id) AS agr_count
    FROM open_space os
        JOIN agreement agr ON os.open_space_id = agr.open_space_id
    GROUP BY os.open_space_id
)
SELECT open_space_id, agr_count
FROM os_agr_count
WHERE agr_count = (SELECT MAX(agr_count) FROM os_agr_count);


