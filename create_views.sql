-- представление для отображения актуальных товаров с их категориями и поставщиками
CREATE OR REPLACE VIEW current_products_v AS
SELECT p.product_id,
       p.name AS product_name,
       pv.price AS current_price,
       c.name AS category_name,
       s.name AS supplier_name,
       s.contact_person AS supplier_contact
FROM online_shop.products p
JOIN online_shop.product_versions pv ON p.product_id = pv.product_id AND pv.is_current = TRUE
JOIN online_shop.categories c ON p.category_id = c.category_id
JOIN online_shop.suppliers s ON p.supplier_id = s.supplier_id;

SELECT *
FROM current_products_v;

-- представление для отображения заказов с деталями пользователей и пунктов выдачи
CREATE OR REPLACE VIEW order_details_v AS
SELECT o.order_id,
       u.full_name AS customer_name,
       u.email AS customer_email,
       o.order_date,
       o.status AS order_status,
       o.total_price,
       pp.name AS pickup_point_name,
       pp.address AS pickup_address,
       p.payment_method,
       p.status AS payment_status
FROM online_shop.orders o
JOIN online_shop.users u ON o.user_id = u.user_id
JOIN online_shop.pickup_points pp ON o.pickup_point_id = pp.pickup_point_id
JOIN online_shop.payments p ON o.payment_id = p.payment_id;

SELECT *
FROM order_details_v;