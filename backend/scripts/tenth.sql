--изменение среднего чека по месяцам
SELECT
    EXTRACT(MONTH FROM o.order_date) AS month,
    COUNT(o.order_id) AS orders_count,
    AVG(o.total_price) AS avg_check,
    AVG(o.total_price) - LAG(AVG(o.total_price), 1) OVER (ORDER BY EXTRACT(MONTH FROM o.order_date)) AS avg_check_change
FROM online_shop.orders o
GROUP BY EXTRACT(MONTH FROM o.order_date)
ORDER BY month;