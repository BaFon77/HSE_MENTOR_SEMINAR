-- Создание таблиц

CREATE TABLE orders (
                        order_id UInt32,
                        user_id UInt32,
                        order_date DateTime,
                        total_amount Float64,
                        payment_status String
) ENGINE = MergeTree()
ORDER BY order_id;

CREATE TABLE order_items (
                             item_id UInt32,
                             order_id UInt32,
                             product_name String,
                             product_price Float64,
                             quantity UInt32
) ENGINE = MergeTree()
ORDER BY item_id;

-- Заполнение таблиц

INSERT INTO orders
SELECT *
FROM s3(
        'https://storage.yandexcloud.net/hadoopbacket/files/orders.csv',
        'CSVWithNames'
     );

INSERT INTO order_items
SELECT *
FROM s3(
             'https://storage.yandexcloud.net/hadoopbacket/files/order_items.txt',
             'CSVWithNames'
     )
         SETTINGS format_csv_delimiter = ';';

-- 1. Агрегации по статусам оплаты
SELECT payment_status, count(), sum(total_amount), avg(total_amount)
FROM orders GROUP BY payment_status;

-- 2. JOIN агрегации
SELECT sum(quantity), sum(product_price * quantity), avg(product_price)
FROM orders AS o JOIN order_items AS oi ON o.order_id = oi.order_id;

-- 3. Ежедневная статистика
SELECT toDate(order_date) as d, count(), sum(total_amount)
FROM orders GROUP BY d ORDER BY d;

-- 4. Топ активных пользователей
SELECT user_id, count() as orders_cnt, sum(total_amount) as total
FROM orders GROUP BY user_id ORDER BY total DESC;