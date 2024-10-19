{{ config(materialized='view') }}
SELECT * FROM {{ ref('titanic_data')}} limit 10;