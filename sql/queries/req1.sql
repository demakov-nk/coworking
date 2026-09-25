/*
Вывести всех администраторов, которые заключали
договоры об аренде
рабочего пространства А
с
клиентом Б

*** искать не по индексу, а по значению 

*/

-- SELECT DISTINCT adm.admin_id, adm.surname, adm.name
-- FROM open_space os
--     JOIN agreement agr 
--         ON os.open_space_id = agr.open_space_id AND os.open_space_id = 80
--     JOIN administrator adm 
--         ON agr.admin_id = adm.admin_id AND agr.client_id = 1894


SELECT DISTINCT adm.admin_id, adm.surname, adm.name
FROM open_space os
    JOIN agreement agr
        ON os.open_space_id = agr.open_space_id AND os.open_space_id = 80
    JOIN administrator adm
        ON agr.admin_id = adm.admin_id
    JOIN client cli
        ON agr.client_id = cli.client_id 
        AND cli.surname = 'Куликов'
        AND cli.name = 'Аристарх';
