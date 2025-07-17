-- создаем последовательности
CREATE SEQUENCE IF NOT EXISTS online_shop.transaction_id_seq
START WITH 000000
INCREMENT BY 1;

CREATE SEQUENCE IF NOT EXISTS online_shop.payments_payment_id_seq
START WITH 16
INCREMENT BY 1;

CREATE SEQUENCE IF NOT EXISTS online_shop.orders_order_id_seq
START WITH 16
INCREMENT BY 1;

-- устанавливаем DEFAULT значение для столбцов
ALTER TABLE online_shop.payments
ALTER COLUMN payment_id
SET DEFAULT nextval('online_shop.payments_payment_id_seq'::regclass),
ALTER COLUMN transaction_id
SET DEFAULT 'PAY-' || lpad(nextval('online_shop.transaction_id_seq')::TEXT, 6, '0');

ALTER TABLE online_shop.orders
ALTER COLUMN order_id
SET DEFAULT nextval('online_shop.orders_order_id_seq'::regclass);

-- процедура для оформления заказа из корзины
CREATE OR REPLACE PROCEDURE create_order_from_cart(p_user_id INT,
       p_payment_method VARCHAR(100),
       p_pickup_point_id INT,
       OUT p_order_id INT
) AS $$
DECLARE
    v_payment_id INT;
    v_total DECIMAL(10,2) := 0;
    v_cart_count INT;
BEGIN
    -- проверяем, есть ли товары в корзине
    SELECT COUNT(*) INTO v_cart_count
    FROM online_shop.cart_items ci
    JOIN online_shop.cart c ON ci.cart_id = c.cart_id
    WHERE c.user_id = p_user_id;

    IF v_cart_count = 0 THEN
        RAISE EXCEPTION 'Корзина пользователя % пуста', p_user_id;
    END IF;

     -- создаем платеж
    INSERT INTO online_shop.payments(payment_method, status)
    VALUES (p_payment_method, 'pending')
    RETURNING payment_id INTO v_payment_id;
    
    -- рассчитываем общую сумму по корзине
    SELECT COALESCE(SUM(ci.quantity * pv.price), 0)
    INTO v_total
    FROM online_shop.cart_items ci
    JOIN online_shop.product_versions pv ON ci.product_id = pv.product_id AND pv.is_current = TRUE
    JOIN online_shop.cart c ON ci.cart_id = c.cart_id
    WHERE c.user_id = p_user_id;

    IF v_total <= 0 THEN
        -- отменяем платеж, если сумма некорректна
        DELETE FROM online_shop.payments WHERE payment_id = v_payment_id;
        RAISE EXCEPTION 'Некорректная сумма заказа: %', v_total;
    END IF;
    
    -- создаем заказ
    INSERT INTO online_shop.orders(user_id, status, total_price, payment_id, pickup_point_id)
    VALUES (p_user_id, 'processing', v_total, v_payment_id, p_pickup_point_id)
    RETURNING order_id INTO p_order_id;
    
    -- переносим товары из корзины в заказ
    INSERT INTO online_shop.order_items(order_id, product_id, version_id, price, quantity)
    SELECT p_order_id,
           ci.product_id,
           pv.version_id,
           pv.price,
           ci.quantity
    FROM online_shop.cart_items ci
    JOIN online_shop.product_versions pv ON ci.product_id = pv.product_id AND pv.is_current = TRUE
    JOIN online_shop.cart c ON ci.cart_id = c.cart_id
    WHERE c.user_id = p_user_id;
    
    -- очищаем корзину
    DELETE FROM online_shop.cart_items WHERE cart_id IN (
        SELECT cart_id FROM online_shop.cart WHERE user_id = p_user_id
    );
END;
$$ LANGUAGE plpgsql;

-- функция для расчета среднего рейтинга товара
CREATE OR REPLACE FUNCTION get_product_avg_rating(p_product_id INT)
RETURNS DECIMAL(3,2) AS $$
DECLARE
    v_avg_rating DECIMAL(3,2);
BEGIN
    SELECT AVG(rating) INTO v_avg_rating
    FROM online_shop.reviews
    WHERE product_id = p_product_id;
    RETURN COALESCE(v_avg_rating, 0);
END;
$$ LANGUAGE plpgsql;

-- функция для получения популярных товаров (по количеству заказов)
CREATE OR REPLACE FUNCTION get_popular_products(p_limit INT)
RETURNS TABLE(
    product_id INT,
    product_name VARCHAR(100),
    order_count BIGINT,
    avg_rating DECIMAL(3,2)) AS $$
BEGIN
    RETURN QUERY
    SELECT p.product_id,
           p.name AS product_name,
           COUNT(oi.order_id) AS order_count,
           get_product_avg_rating(p.product_id) AS avg_rating
    FROM online_shop.products p
    LEFT JOIN online_shop.order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id
    ORDER BY order_count DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;





