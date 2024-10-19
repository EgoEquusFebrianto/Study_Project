{{ config(
    materialized='table',
    schema=generate_schema_name('testing')
) }}

WITH source_data as (
    SELECT * FROM {{ source('engineering', 'titanic_dataset') }} limit 100
),
final as (
    select
        part.ticket as ticket,
        part.name as name,
        part.sex as sex,
        part.age as age,
        part.survived as survived,
        part.embarked as embarked,
        part.cabin as cabin
    from source_data as part
)
select * from final