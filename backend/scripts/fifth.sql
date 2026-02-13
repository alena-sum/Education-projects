--самые активные пользователи
SELECT u.user_id, u.full_name, COUNT(o.order_id) AS orders_count
FROM online_shop.users u
JOIN online_shop.orders o ON u.user_id = o.user_id
WHERE EXISTS (
        SELECT 1
        FROM online_shop.reviews r
        WHERE r.user_id = u.user_id
    )
GROUP BY u.user_id, u.full_name
ORDER BY orders_count DESC
LIMIT 10;