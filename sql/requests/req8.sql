/*
Для каждого вида дополнительной услуги
и
администратора 
посчитать число договоров об аренде,
в которых использовалась эта услуга.

Построить 3D-гистограмму
*/

SELECT adm.admin_id, est.type_id, COUNT(agr.agreement_id) AS agr_count
FROM administrator adm CROSS JOIN extra_service_type est
    LEFT JOIN extra_service es 
        ON est.type_id = es.type_id
    LEFT JOIN agreement agr 
            ON adm.admin_id = agr.admin_id
            AND es.purchase_date = agr.conclusion_date
GROUP BY adm.admin_id, est.type_id
