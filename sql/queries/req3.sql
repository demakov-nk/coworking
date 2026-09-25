/*
Для каждого вида дополнительной услуги 
посчитать число дополнительных услуг
и
количество счетов, которые оплачивают эту услугу.

Построить 2D-гистограмму
*/

SELECT est.type_id, 
       COUNT(DISTINCT es.extra_service_id) AS extra_services, 
       COUNT(bill.bill_id) AS bills
FROM extra_service_type est
    LEFT JOIN extra_service es ON est.type_id = es.type_id
    LEFT JOIN bill ON es.extra_service_id = bill.extra_service_id
GROUP BY est.type_id;

-- SELECT est.type_id,
--        (SELECT COUNT(*) FROM extra_service WHERE type_id = est.type_id) AS extra_services,
--        COUNT(bill.bill_id) AS bills
-- FROM extra_service_type est
--      LEFT JOIN extra_service es ON est.type_id = es.type_id
--      LEFT JOIN bill ON es.extra_service_id = bill.extra_service_id
-- GROUP BY est.type_id
-- ORDER BY est.type_id

-- WITH service_stats AS (
--     SELECT type_id, COUNT(*) AS extra_services
--     FROM extra_service
--     GROUP BY type_id
-- ),
-- bill_stats AS (
--     SELECT es.type_id, COUNT(b.bill_id) AS bills
--     FROM extra_service es
--     JOIN bill b ON es.extra_service_id = b.extra_service_id
--     GROUP BY es.type_id
-- )
-- SELECT 
--     est.type_id,
--     COALESCE(ss.extra_services, 0) AS extra_services,
--     COALESCE(bs.bills, 0) AS bills
-- FROM extra_service_type est
--     LEFT JOIN service_stats ss ON est.type_id = ss.type_id
--     LEFT JOIN bill_stats bs ON est.type_id = bs.type_id
-- ORDER BY est.type_id;
