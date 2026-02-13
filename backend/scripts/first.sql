--5 самых популярных товаров
SELECT p.product_id, p.name, COUNT(oi.product_id) AS order_count, SUM(oi.quantity) AS total_quantity_sold
FROM online_shop.order_items oi
JOIN online_shop.products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY order_count DESC
LIMIT 5;