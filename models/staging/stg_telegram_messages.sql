WITH raw_data AS (
    SELECT * FROM {{ source('raw', 'telegram_messages') }}
),

ranked_data AS (
    SELECT
        message_id,
        channel_name,
        message_date::TIMESTAMP as message_timestamp,
        message_text,
        -- PostgreSQL Logic: Check if text is null OR just an empty string
        (message_text IS NULL OR message_text = '') as is_empty,
        COALESCE(views, 0) as view_count,
        COALESCE(forwards, 0) as forward_count,
        has_media,
        image_path,
        -- Identify the latest version of a message
        ROW_NUMBER() OVER (
            PARTITION BY message_id, channel_name 
            ORDER BY message_date DESC
        ) as row_num
    FROM raw_data
)

SELECT
    message_id,
    channel_name,
    message_timestamp,
    message_text,
    is_empty,         -- Now this column is available for fct_messages!
    view_count,
    forward_count,
    has_media,
    image_path
FROM ranked_data
WHERE row_num = 1