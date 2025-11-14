-- ============================================================================
-- Query 1: Full Order Report
-- ============================================================================
-- Returns: user_name, order_id, order_date, list_of_products (group_concat), 
--          total_qty, order_total, payment_status
-- ORDER BY order_date DESC
-- LIMIT 200

SELECT 
    u.name AS user_name,
    o.order_id,
    o.order_date,
    GROUP_CONCAT(p.name, ', ') AS list_of_products,
    SUM(oi.quantity) AS total_qty,
    o.total_amount AS order_total,
    pay.status AS payment_status
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN payments pay ON o.order_id = pay.order_id
GROUP BY o.order_id, u.name, o.order_date, o.total_amount, pay.status
ORDER BY o.order_date DESC
LIMIT 200;

-- ============================================================================
-- Query 2: Top 10 Best Selling Products
-- ============================================================================
-- Columns: product_id, name, category, total_quantity_sold, total_revenue

SELECT 
    p.product_id,
    p.name,
    p.category,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY total_quantity_sold DESC
LIMIT 10;

-- ============================================================================
-- Query 3: Monthly Sales Summary
-- ============================================================================
-- Columns: month(YYYY-MM), total_orders, total_revenue, avg_order_value
-- ORDER BY month DESC
-- LIMIT 24

SELECT 
    strftime('%Y-%m', o.order_date) AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM orders o
GROUP BY strftime('%Y-%m', o.order_date)
ORDER BY month DESC
LIMIT 24;

