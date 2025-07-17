--анализ продаж по поставщикам
SELECT
    s.supplier_id,
    s.name,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.price * oi.quantity) AS total_revenue,
    SUM(oi.price * oi.quantity) / SUM(SUM(oi.price * oi.quantity)) OVER () * 100 AS revenue_percent
FROM online_shop.order_items oi
JOIN online_shop.products p ON oi.product_id = p.product_id
JOIN online_shop.suppliers s ON p.supplier_id = s.supplier_id
GROUP BY s.supplier_id, s.name
ORDER BY total_revenue DESC;