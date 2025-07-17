--пользователи, потратившие больше всего денег
SELECT u.user_id, u.full_name, SUM(o.total_price) AS total_spent
FROM online_shop.users u
JOIN online_shop.orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.full_name
HAVING SUM(o.total_price) > 5000
ORDER BY total_spent DESC;