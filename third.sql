--изменение цен
WITH price_history AS (
    SELECT
        product_id,
        price,
        valid_from,
        LAG(price) OVER (PARTITION BY product_id ORDER BY valid_from) AS prev_price
    FROM online_shop.product_versions
)
SELECT
    p.product_id,
    p.name,
    ph.price AS current_price,
    ph.prev_price AS previous_price,
    ROUND((ph.price - ph.prev_price) / ph.prev_price * 100, 2) AS price_change_percent
FROM online_shop.products p
JOIN price_history ph ON p.product_id = ph.product_id
WHERE
    ph.prev_price IS NOT NULL
    AND NOT EXISTS (
        SELECT 1
        FROM online_shop.product_versions pv2
        WHERE pv2.product_id = ph.product_id
        AND pv2.valid_from > ph.valid_from
    );