/*
Найти рабочие пространства, в которых
было минимальное количество договоров

*** нельзя WITH

*/

-- WITH os_agr_count AS (
--     SELECT os.open_space_id,
--            COUNT(agr.agreement_id) AS agr_count
--     FROM open_space os
--         LEFT JOIN agreement agr ON os.open_space_id = agr.open_space_id
--     GROUP BY os.open_space_id
-- )
-- SELECT open_space_id, agr_count
-- FROM os_agr_count
-- WHERE agr_count = (SELECT MIN(agr_count) FROM os_agr_count)

SELECT os.open_space_id,
       os.area,
       os.capacity,
       COUNT(agr.agreement_id) AS agreements
FROM open_space os
    JOIN agreement agr ON agr.open_space_id = os.open_space_id
GROUP BY os.open_space_id
HAVING COUNT(agr.agreement_id) = (
    SELECT COUNT(agreement_id)
    FROM agreement
    WHERE open_space_id IS NOT NULL
    GROUP BY open_space_id
    ORDER BY COUNT(agreement_id)
    LIMIT 1
);
