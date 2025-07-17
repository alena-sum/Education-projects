SELECT
    CASE
        WHEN total_price < 3000 THEN 'Малый (<3000₽)'
        WHEN total_price BETWEEN 3000 AND 10000 THEN 'Средний (3000-10000₽)'
        ELSE 'Крупный (>10000₽)'
    END AS order_size,
    COUNT(*) AS count
FROM online_shop.orders
GROUP BY order_size
ORDER BY count DESC;