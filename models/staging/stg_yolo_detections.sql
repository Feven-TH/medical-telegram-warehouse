{{ config(materialized='view') }}

WITH raw_detections AS (
    SELECT * FROM {{ source('yolo_data', 'detections') }}
)

SELECT
    id AS detection_id,
    message_id,  -- This links to the image filename
    channel_name,
    object_detected,
    confidence,
    -- Create a flag for high-priority medical items
    CASE 
        WHEN object_detected IN ('bottle', 'refrigerator') THEN TRUE 
        ELSE FALSE 
    END AS is_medical_relevant
FROM raw_detections
WHERE confidence > 0.4  -- Filter out noise