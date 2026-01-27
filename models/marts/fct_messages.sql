SELECT
    message_id,
    channel_name,
    message_timestamp,
    message_text,
    view_count,      
    forward_count,
    has_media,
    -- Add a unique key for the fact table
    md5(message_id || channel_name || message_timestamp) as message_pk
FROM {{ ref('stg_telegram_messages') }}
WHERE is_empty = FALSE