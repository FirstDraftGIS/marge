# Marge
**M**odel **A**rtificially **R**esolving **G**eographic **E**ntities 

# Training Data
Marge trains on data in tsv format with the following columns

| name                         | type    | description | example  |
| ---------------------------- | ------- | ----------- | ---------|
| country_code                 | text    | 2-Letter Country Code | FR |
| country_rank                 | integer |Rank of country in order by most popular | 27 |
| edit distance                | integer | Number of changes to get correct name | 0 |
| geonames_feature_class       | text    | | |
| geonames_feature_code        | text    | | LKI |
| has_highest_population       | boolean | Has highest pouplation relative to other options | 1 |
| has_lowest_admin_level       | boolean | Is lowest admin level among other possibilities | 0 |
| has_shape                    | boolean | Does polygon or multi-polygon exist for this feature? | 1 |
| has_pcode                    | boolean | PCODE exists for this place | 1 |
| importance                   | float   | Importance from OSMNames | 0.54 |
| important                    | boolean | Is importance greater than a threshold | 1 |
| matches_topic                | boolean | Does it match topic of source | 0 |
| median_distance              | float   | Median Distance from all other options for all places in map | 0.123 |
| most_important_in_timezone   | boolean | Does it have highest importance among options in same timezone? | 1 |
| notable                      | boolean | Does it appear in Wikipedia | 1 |
| place_type                   | string  | Place type from Unum | B |
| popularity                   | integer | | How many times have people made maps of this place? | 123 |
| correct                      | boolean | | Is this the correct option? This is the label. | 1 |
