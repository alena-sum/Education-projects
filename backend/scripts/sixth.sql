--распределение продаж по месяцам и категориям
SELECT
    EXTRACT(MONTH FROM o.order_date) AS month,
    c.name AS category,
    SUM(oi.quantity) AS total_sold,
    ROUND(SUM(oi.price * oi.quantity), 2) AS total_revenue
FROM online_shop.order_items oi
JOIN online_shop.orders o ON oi.order_id = o.order_id
JOIN online_shop.products p ON oi.product_id = p.product_id
JOIN online_shop.categories c ON p.category_id = c.category_id
GROUP BY EXTRACT(MONTH FROM o.order_date), c.name
ORDER BY month, total_sold DESC;