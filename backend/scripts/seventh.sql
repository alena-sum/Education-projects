--товары, которые никогда не заказывали с ценой выше среднего
SELECT p.product_id, p.name, p.price
FROM online_shop.products p
LEFT JOIN online_shop.order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL AND p.price > (SELECT AVG(price) FROM online_shop.products);