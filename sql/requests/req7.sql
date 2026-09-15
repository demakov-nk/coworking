/*
Найти администратора, 
который никогда не оформлял абонемент, 
через который оплачивалась дополнительная услуга А
*/

SELECT admin_id, surname, name
FROM administrator
WHERE admin_id NOT IN (
    SELECT sub.admin_id
    FROM subscription sub
        JOIN extra_service es 
            ON sub.client_id = es.client_id
                AND es.type_id = 5
                AND es.purchase_date BETWEEN sub.start_date AND sub.end_date
);
