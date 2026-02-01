-- dbt tests pass if the query returns ZERO rows.
-- This test ensures no message has a negative view count.
SELECT
    message_id,
    view_count
FROM {{ ref('fct_messages') }}
WHERE view_count < 0