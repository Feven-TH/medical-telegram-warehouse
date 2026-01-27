SELECT
    DISTINCT channel_name,
    COUNT(message_id) as total_messages_scraped,
    MIN(message_timestamp) as first_message_date
FROM {{ ref('stg_telegram_messages') }}
GROUP BY 1