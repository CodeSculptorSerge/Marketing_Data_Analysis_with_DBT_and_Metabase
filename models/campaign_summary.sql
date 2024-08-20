WITH base_data AS (
    SELECT 
        campaign_name,
        category,
        SUM(revenue) AS total_revenue,
        SUM(orders) AS total_orders,
        SUM(clicks) AS total_clicks,
        SUM(mark_spent) AS total_spent
    FROM marketing_data
    GROUP BY campaign_name, category
)

SELECT 
    campaign_name,
    category,
    total_revenue,
    total_orders,
    total_clicks,
    total_spent,
    total_revenue / total_orders AS avg_order_value,
    total_spent / total_clicks AS avg_cpc
FROM base_data

