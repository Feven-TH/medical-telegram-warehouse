{{ config(materialized='table') }}

SELECT
    m.message_id,
    m.channel_name,
    m.message_text,
    m.message_timestamp,
    d.object_detected,
    d.confidence
FROM {{ ref('fct_messages') }} m
JOIN {{ ref('stg_yolo_detections') }} d 
    ON m.channel_name = d.channel_name
    AND m.message_timestamp::text LIKE '%' || SUBSTRING(d.message_id FROM 7 FOR 10) || '%'
WHERE d.is_medical_relevant = TRUE