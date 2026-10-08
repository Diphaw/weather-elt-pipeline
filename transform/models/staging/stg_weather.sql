WITH source_data AS (
    SELECT
        id,
        city,
        payload,
        extracted_at
    FROM {{ source('raw_weather', 'weather_data') }}
)

SELECT
    id AS raw_id,
    city,
    -- Parsing JSONB OpenWeather payload
    (payload->'coord'->>'lat')::NUMERIC AS latitude,
    (payload->'coord'->>'lon')::NUMERIC AS longitude,
    (payload->'main'->>'temp')::NUMERIC AS temperature_celsius,
    (payload->'main'->>'feels_like')::NUMERIC AS feels_like_celsius,
    (payload->'main'->>'temp_min')::NUMERIC AS temp_min_celsius,
    (payload->'main'->>'temp_max')::NUMERIC AS temp_max_celsius,
    (payload->'main'->>'pressure')::INT AS pressure_hpa,
    (payload->'main'->>'humidity')::INT AS humidity_pct,
    (payload->'wind'->>'speed')::NUMERIC AS wind_speed_mps,
    (payload->'clouds'->>'all')::INT AS cloudiness_pct,
    payload->'weather'->0->>'main' AS weather_condition,
    payload->'weather'->0->>'description' AS weather_description,
    TO_TIMESTAMP((payload->>'dt')::BIGINT) AS observed_at,
    extracted_at
FROM source_data
