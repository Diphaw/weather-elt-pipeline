WITH staged_data AS (
    SELECT * FROM {{ ref('stg_weather') }}
)

SELECT
    city,
    DATE(observed_at) AS observation_date,
    ROUND(AVG(temperature_celsius), 2) AS avg_temp_celsius,
    ROUND(MIN(temp_min_celsius), 2) AS min_temp_celsius,
    ROUND(MAX(temp_max_celsius), 2) AS max_temp_celsius,
    ROUND(AVG(humidity_pct), 1) AS avg_humidity_pct,
    ROUND(AVG(wind_speed_mps), 2) AS avg_wind_speed_mps,
    COUNT(*) AS total_observations,
    MAX(extracted_at) AS last_updated_at
FROM staged_data
GROUP BY 
    city, 
    DATE(observed_at)
