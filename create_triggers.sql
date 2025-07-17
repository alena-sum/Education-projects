-- триггер для обновления цены в products при изменении актуальной версии
CREATE OR REPLACE FUNCTION update_product_price()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_current = TRUE THEN
        UPDATE online_shop.products
        SET price = NEW.price
        WHERE product_id = NEW.product_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_product_price_trg
AFTER INSERT OR UPDATE ON online_shop.product_versions
FOR EACH ROW
EXECUTE FUNCTION update_product_price();

-- триггер для проверки, что у товара только одна актуальная версия
CREATE OR REPLACE FUNCTION ensure_single_current_version()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_current = TRUE THEN
        UPDATE online_shop.product_versions
        SET is_current = FALSE
        WHERE product_id = NEW.product_id
        AND version_id != NEW.version_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER ensure_single_current_version_trg
BEFORE INSERT OR UPDATE ON online_shop.product_versions
FOR EACH ROW
EXECUTE FUNCTION ensure_single_current_version();

-- триггер для автоматического обновления времени в Cart при изменении
CREATE OR REPLACE FUNCTION update_cart_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_cart_timestamp_trg
BEFORE UPDATE ON online_shop.cart
FOR EACH ROW
EXECUTE FUNCTION update_cart_timestamp();