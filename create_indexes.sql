-- индекс для ускорения поиска текущих версий товаров
CREATE INDEX product_version_current_idx ON online_shop.product_versions(product_id, is_current)
WHERE is_current = TRUE;

-- индекс для ускорения поиска товаров в корзине пользователя
CREATE INDEX cart_item_cart_idx ON online_shop.cart_items(cart_id);