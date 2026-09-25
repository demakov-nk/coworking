/*
Для помещения А переписать
договоры 
администратора Б
на 
администратора В
*/

-- SELECT agreement_id, admin_id, room_id
-- FROM agreement
-- WHERE admin_id = 67 AND room_id = 97;

-- SELECT agreement_id, admin_id, room_id
-- FROM agreement
-- WHERE admin_id = 147 AND room_id = 97;

UPDATE agreement
SET admin_id = 147
WHERE admin_id = 67 AND room_id = 97;

-- SELECT agreement_id, admin_id, room_id
-- FROM agreement
-- WHERE admin_id = 147 AND room_id = 97;

-- SELECT agreement_id, admin_id, room_id
-- FROM agreement
-- WHERE admin_id = 67 AND room_id = 97;

