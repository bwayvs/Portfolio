


SELECT   COUNT(*) AS "Rental before count"
FROM     rental;

-- Merge transaction data into rental table.
MERGE INTO rental target
USING ( SELECT DISTINCT
r.rental_id
, c.contact_id
, tu.check_out_date AS check_out_date
, tu.return_date AS return_date
, 1001 AS created_by
, TRUNC(SYSDATE) AS creation_date
, 1001 AS last_updated_by
, TRUNC(SYSDATE) AS last_update_date
FROM member m
INNER JOIN contact c
ON m.member_id = c.member_id
INNER JOIN transaction_upload tu
ON m.account_number = tu.account_number
AND c.first_name = tu.first_name
AND NVL(c.middle_name, 'x') = NVL(tu.middle_name, 'x')
AND c.last_name = tu.last_name
LEFT JOIN rental r
ON c.contact_id = r.customer_id
AND r.check_out_date = tu.check_out_date
AND r.return_date = tu.return_date) source
ON (target.rental_id = source.rental_id)
WHEN MATCHED THEN
UPDATE SET last_updated_by = source.last_updated_by
,          last_update_date = source.last_update_date
WHEN NOT MATCHED THEN
INSERT VALUES
( rental_s1.NEXTVAL
, source.contact_id
, source.check_out_date
, source.return_date
, source.created_by
, source.creation_date
, source.last_updated_by
, source.last_update_date);

-- Count rentals after insert.
SELECT   COUNT(*) AS "Rental after count"
FROM     rental;

-- Count rental items before insert.
SELECT   COUNT(*)
FROM     rental_item;

-- Merge transaction data into rental_item table.
MERGE INTO rental_item target
USING ( 
SELECT ri.rental_item_id
, r.rental_id
, tu.item_id
, r.return_date - r.check_out_date AS rental_item_price
, cl.common_lookup_id AS rental_item_type
, 1001 AS created_by
, TRUNC(SYSDATE) AS creation_date
, 1001 AS last_updated_by
, TRUNC(SYSDATE) AS last_update_date
FROM member m
INNER JOIN contact c
ON m.member_id = c.member_id 
INNER JOIN transaction_upload tu
ON c.first_name = tu.first_name
AND NVL(c.middle_name, 'x') = NVL(tu.middle_name, 'x')
AND c.last_name = tu.last_name
AND tu.account_number = m.account_number
LEFT JOIN rental r
ON c.contact_id = r.customer_id
AND TRUNC(r.check_out_date) = TRUNC(tu.check_out_date)
AND TRUNC(r.return_date) = TRUNC(tu.return_date)
LEFT JOIN rental_item ri
ON r.rental_id = ri.rental_id
INNER JOIN common_lookup cl
ON cl.common_lookup_table = 'RENTAL_ITEM'
AND cl.common_lookup_column = 'RENTAL_ITEM_TYPE'
AND cl.common_lookup_type = tu.rental_item_type) source
ON (target.rental_item_id = source.rental_item_id)
WHEN MATCHED THEN
UPDATE SET last_updated_by = source.last_updated_by
,          last_update_date = source.last_update_date
WHEN NOT MATCHED THEN
INSERT VALUES
( rental_item_s1.nextval
, source.rental_id
, source.item_id
, source.created_by
, source.creation_date
, source.last_updated_by
, source.last_update_date
, source.rental_item_price
, source.rental_item_type);

-- Count rental items after insert.
SELECT   COUNT(*) AS "After Insert"
FROM     rental_item;

-- Count transactions before insert
SELECT   COUNT(*) AS "Before Insert"
FROM     transaction;

-- Merge transaction data into transaction table.
MERGE INTO transaction target
USING ( 
SELECT t.transaction_id
, tu.payment_account_number AS transaction_account
, cl1.common_lookup_id AS transaction_type
, tu.transaction_date
, (SUM(tu.transaction_amount)/ 1.06) AS transaction_amount
, r.rental_id
, cl2.common_lookup_id AS payment_method_type
, m.credit_card_number AS payment_account_number
, 1001 AS created_by
, TRUNC(SYSDATE) AS creation_date
, 1001 AS last_updated_by
, TRUNC(SYSDATE) AS last_update_date
FROM member m
INNER JOIN contact c
ON m.member_id = c.member_id
INNER JOIN transaction_upload tu
ON c.first_name = tu.first_name
AND NVL(c.middle_name, 'x') = NVL(tu.middle_name, 'x')
AND c.last_name = tu.last_name
AND tu.account_number = m.account_number
INNER JOIN rental r
ON c.contact_id = r.customer_id
AND TRUNC(tu.check_out_date) = TRUNC(r.check_out_date)
AND TRUNC(tu.return_date) = TRUNC(r.return_date)
INNER JOIN common_lookup cl1
ON cl1.common_lookup_table = 'TRANSACTION'
AND cl1.common_lookup_column = 'TRANSACTION_TYPE'
AND cl1.common_lookup_type = tu.transaction_type
INNER JOIN common_lookup cl2
ON cl2.common_lookup_table = 'TRANSACTION'
AND cl2.common_lookup_column = 'TRANSACTION_TYPE'
AND cl2.common_lookup_type = tu.transaction_type
LEFT JOIN transaction t
ON t.transaction_account = tu.payment_account_number
AND t.transaction_type = cl1.common_lookup_id
AND t.transaction_date = tu.transaction_date
AND t.transaction_amount = tu.transaction_amount
AND t.payment_method_type = cl2.common_lookup_id
AND t.payment_account_number = tu.payment_account_number
GROUP BY t.transaction_id
, tu.payment_account_number
, cl1.common_lookup_id
, tu.transaction_date
, r.rental_id
, cl2.common_lookup_id
, m.credit_card_number
, 1001
, TRUNC(SYSDATE)
, 1001
, TRUNC(SYSDATE)) source
ON (target.transaction_id = source.transaction_id)
WHEN MATCHED THEN
UPDATE SET last_updated_by = source.last_updated_by
,          last_update_date = source.last_update_date
WHEN NOT MATCHED THEN
INSERT VALUES
( transaction_s1.nextval
, source.transaction_account
, source.transaction_type
, source.transaction_date
, source.transaction_amount
, source.rental_id
, source.payment_method_type
, source.payment_account_number
, source.created_by
, source.creation_date
, source.last_updated_by
, source.last_update_date);

-- Count transactions after insert
SELECT   COUNT(*)
FROM     transaction;

-- Create a procedure to wrap the transformation of import to normalized tables.
CREATE OR REPLACE PROCEDURE upload_transactions IS
BEGIN
  -- Set save point for an all or nothing transaction.
  SAVEPOINT starting_point;

  -- Insert or update the table, which makes this rerunnable when the file hasn't been updated.
  MERGE INTO rental target
  USING ( 
  SELECT DISTINCT
  r.rental_id
  , c.contact_id
  , tu.check_out_date AS check_out_date
  , tu.return_date AS return_date
  , 1001 AS created_by
  , TRUNC(SYSDATE) AS creation_date
  , 1001 AS last_updated_by
  , TRUNC(SYSDATE) AS last_update_date
  FROM member m
  INNER JOIN conact c
  ON m.member_id = c.member_id
  INNER JOIN transaction_upload tu
  ON m.account_number tu.account_number
  AND c.first_name = tu.first_name
  AND NVL(c.middle_name, 'x') = NVL(tu.middle_name, 'x')
  AND c.last_name = tu.last_name
  LEFT JOIN rental r
  ON c.contact_id = r.customer_id
  AND r.check_out_date = tu.check_out_date
  AND r.return_date = tu.return_date) source
  ON (target.rental_id = source.rental_id)
  WHEN MATCHED THEN
  UPDATE SET last_updated_by = source.last_updated_by
  ,          last_update_date = source.last_update_date
  WHEN NOT MATCHED THEN
  INSERT VALUES
  ( rental_s1.NEXTVAL
  , source.contact_id
  , source.check_out_date
  , source.return_date
  , source.created_by
  , source.creation_date
  , source.last_updated_by
  , source.last_update_date);
  

  -- Insert or update the table, which makes this rerunnable when the file hasn't been updated.
  MERGE INTO rental_item target
  USING ( 
  SELECT ri.rental_item_id
  , r.rental_id
  , tu.item_id
  , r.return_date - r.check_out_date AS rental_item_price
  , cl1.common_lookup_id AS rental_item_type
  , 1001 AS created_by
  , TRUNC(SYSDATE) AS creation_date
  , 1001 AS last_updated_by
  , TRUNC(SYSDATE) AS last_update_date
  FROM member m
  INNER JOIN contact c
  ON m.member_id = c.member_id
  INNER JOIN transaction_upload tu
  ON c.first_name = tu.first_name
  AND NVL(c.middle_name, 'x') = NVL(tu.middle_name, 'x')
  AND c.last_name = tu.last_name
  AND tu.account_number = m.account_number
  LEFT JOIN rental r
  ON c.contact_id = r.customer_id
  AND TRUNC(r.check_out_date) = TRUNC(tu.check_out_date)
  AND TRUNC(r.return_date) = TRUNC(tu.return_date)
  LEFT JOIN rental_item ri
  ON r.rental_id = ri.rental_id
  INNER JOIN common_lookup cl
  ON cl.common_lookup_table = 'RENTAL_ITEM'
  AND cl.common_lookup_column = 'RENTAL_ITEM_TYPE'
  AND cl.common_lookup_type = tu.rental_item_id) source
  ON (target.rental_item_id = source.rental_item_id)
  WHEN MATCHED THEN
  UPDATE SET last_updated_by = source.last_updated_by
  ,          last_update_date = source.last_update_date
  WHEN NOT MATCHED THEN
  INSERT VALUES
  ( rental_item_s1.nextval
  , source.rental_id
  , source.item_id
  , source.created_by
  , source.creation_date
  , source.last_updated_by
  , source.last_update_date
  , source.rental_item_price
  , source.rental_item_type);
  
  -- Insert or update the table, which makes this rerunnable when the file hasn't been updated.
  MERGE INTO transaction target
  USING ( 
  SELECT t.transaction_id
  , tu_payment_account_number AS transaction_account
  , cl1.common_lookup_id AS transaction_type
  , tu.transaction_date
  , (SUM(tu.transaction_amount)/1.06) AS transaction_amount
  , r.rental_id
  , cl2.common_lookup_id AS payment_method_type
  , m.credit_card_number AS payment_account_number
  , 1001 AS last_updated_by
  , TRUNC(SYSDATE) AS creation_date
  , 1001 AS last_updated_by
  , TRUNC(SYSDATE) AS last_update_date
  FROM member m 
  INNER JOIN contact c
  ON m.member_id = c.member_id 
  INNER JOIN transaction_upload tu
  ON c.first_name = tu.first_name
  AND NVL(c.middle_name, 'x') = NVL(tu.middle_name, 'x')
  AND c.last_name = tu.last_name
  AND tu.account_number = m.account_number
  INNER JOIN rental r
  ON c.contact_id = r.customer_id
  AND TRUNC(tu.check_out_date) = TRUNC(r.check_out_date)
  AND TRUNC(tu.return_date) = TRUNC(r.return_date)
  INNER JOIN common_lookup cl1
  ON cl1.common_lookup_table = 'TRANSACTION'
  AND cl1.common_lookup_column = 'TRANSACTION_TYPE'
  AND cl1.common_lookup_type = tu.transaction_type
  INNER JOIN common_lookup cl2
  ON cl2.common_lookup_table = 'TRANSACTION'
  AND cl2.common_lookup_column = 'TRANSACTION_TYPE'
  AND cl2.common_lookup_type = tu.transaction_type
  LEFT JOIN transaction t
  ON t.transaction_account = tu.payment_account_number
AND t.transaction_type = cl1.common_lookup_id
AND t.transaction_date = tu.transaction_date
AND t.transaction_amount = tu.transaction_amount
AND t.payment_method_type = cl2.common_lookup_id
AND t.payment_account_number = tu.payment_account_number
GROUP BY t.transaction_id
, tu.payment_account_number
, cl1.common_lookup_id
, tu.transaction_date
, r.rental_id
, cl2.common_lookup_id
, m.credit_card_number
, 1001
, TRUNC(SYSDATE)
, 1001
, TRUNC(SYSDATE)) source
  ON (target.transaction_id = source.transaction_id)
  WHEN MATCHED THEN
  UPDATE SET last_updated_by = source.last_updated_by
  ,          last_update_date = source.last_update_date
  WHEN NOT MATCHED THEN
  INSERT VALUES
  ( transaction_s1.nextval
, source.transaction_account
, source.transaction_type
, source.transaction_date
, source.transaction_amount
, source.rental_id
, source.payment_method_type
, source.payment_account_number
, source.created_by
, source.creation_date
, source.last_updated_by
, source.last_update_date);

  -- Save the changes.
  COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK TO starting_point;
    RETURN;
END;
/

-- Show errors if any.
SHOW ERRORS

-- Verify and execute procedure.
COLUMN rental_count      FORMAT 99,999 HEADING "Rental|Count"
COLUMN rental_item_count FORMAT 99,999 HEADING "Rental|Item|Count"
COLUMN transaction_count FORMAT 99,999 HEADING "Transaction|Count"

SELECT   rental_count
,        rental_item_count
,        transaction_count
FROM    (SELECT COUNT(*) AS rental_count FROM rental) CROSS JOIN
        (SELECT COUNT(*) AS rental_item_count FROM rental_item) CROSS JOIN
        (SELECT COUNT(*) AS transaction_count FROM transaction);

-- Transform import source into normalized tables.
EXECUTE upload_transactions;


SELECT   rental_count
,        rental_item_count
,        transaction_count
FROM    (SELECT COUNT(*) AS rental_count FROM rental) CROSS JOIN
        (SELECT COUNT(*) AS rental_item_count FROM rental_item) CROSS JOIN
        (SELECT COUNT(*) AS transaction_count FROM transaction);

-- Transform import source into normalized tables.
EXECUTE upload_transactions;

SELECT   rental_count
,        rental_item_count
,        transaction_count
FROM    (SELECT COUNT(*) AS rental_count FROM rental) CROSS JOIN
        (SELECT COUNT(*) AS rental_item_count FROM rental_item) CROSS JOIN
        (SELECT COUNT(*) AS transaction_count FROM transaction);


-- Expand line length in environment.
SET LINESIZE 200
COLUMN month FORMAT A10 HEADING "MONTH"
COLUMN base_revenue FORMAT A14 HEADING "BASE_REVENUE"
COLUMN ten_plus FORMAT A12 HEADING "10_PLUS"
COLUMN twenty_plus FORMAT A12 HEADING "20_PLUS"
COLUMN ten_plus_less_b FORMAT A18 HEADING "10_PLUS_LESS_B"
COLUMN twenty_plus_less_b FORMAT A18 HEADING "20_PLUS_LESS_B"
SELECT il.month
, il.base_revenue
, il.ten_plus AS "10_PLUS"
, il.twenty_plus AS "20_PLUS"
, il.ten_plus_less_b AS "10_PLUS_LESS_B"
, il.twenty_plus_less_b AS "20_PLUS_LESS_B"
FROM (
SELECT CONCAT(TO_CHAR(t.transaction_date, 'MON')
, CONCAT('-', EXTRACT(YEAR FROM t.transaction_date))) AS MONTH
, EXTRACT(MONTH FROM TRUNC(t.transaction_date)) AS sortkey
, TO_CHAR(SUM(t.transaction_amount), '$9,999,999.00') AS BASE_REVENUE
, TO_CHAR(SUM(t.transaction_amount + (t.transaction_amount * .1)), '$9,999,999.00') AS ten_plus
, TO_CHAR(SUM(t.transaction_amount + (t.transaction_amount * .2)), '$9,999,999.00') AS twenty_plus
, TO_CHAR(SUM(t.transaction_amount + (t.transaction_amount * .1)) - SUM(t.transaction_amount), '$9,999,999.00') AS ten_plus_less_b
, TO_CHAR(SUM(t.transaction_amount + (t.transaction_amount * .2)) - SUM(t.transaction_amount), '$9,999,999.00') AS twenty_plus_less_b 
FROM transaction t
WHERE EXTRACT(YEAR FROM TRUNC(t.transaction_date)) = 2009
GROUP BY CONCAT(TO_CHAR(t.transaction_date, 'MON')
, CONCAT('-', EXTRACT(YEAR FROM t.transaction_date)))
, EXTRACT(MONTH FROM TRUNC(t.transaction_date))) il
ORDER BY il.sortkey;
