SELECT
    c_date,
    SUM(revenue) AS total_revenue,
    SUM(orders) AS total_orders,
    SUM(clicks) AS total_clicks,
    SUM(mark_spent) AS total_spent
FROM marketing_data
GROUP BY c_date
ORDER BY c_date

