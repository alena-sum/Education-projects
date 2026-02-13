--категории с продажами выше среднего
SELECT c.category_id, c.name, SUM(oi.quantity) AS total_sold, AVG(oi.price) AS avg_price
FROM online_shop.order_items oi
JOIN online_shop.products p ON oi.product_id = p.product_id
JOIN online_shop.categories c ON p.category_id = c.category_id
GROUP BY c.category_id, c.name
HAVING SUM(oi.quantity) > (
        SELECT AVG(sq.total_sold)
        FROM (
            SELECT SUM(quantity) AS total_sold
            FROM online_shop.order_items
            GROUP BY product_id
        ) sq
    )
ORDER BY total_sold DESC;