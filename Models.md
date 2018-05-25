# Models
This document describe the various models used by **MARGE** to make predictions.
**MARGE** makes multiple passes over the data in the same way that a human would make multiple drafts.

### First Pass
This is the data that **MARGE** looks at during the first pass.

| name                           | type    | description                    | example |
| ------------------------------ | ------- | ------------------------------ | --------|
| has_enwiki_title               | boolean | Matched with Wikidata          | 1       |
| has_population_between_1_and_1_thousand  | boolean |                      | 0       |
| has_population_between_1_thousand_and_1_million | boolean |               | 1       |
| has_population_between_one_milion_and_ten_million  | boolean |            | 0       |
| has_population_over_ten_million  | boolean |                              | 0       |
| importance                     | float   | Importance from OSMNames       | 0.54    |
| population_is_zero             | boolean | Population is zero in the db   |         |

### Second Pass
| name                           | type    | description                       | example  |
| ------------------------------ | ------- | ------------------------------------- | ---- |
| median_cooccurrence            | integer | how likely co-occurs with other places | .43 |
| score                          | float   | score from the previous pass       | 1.123   |

### Third Pass (under development)
In this model, MARGE evaluates whether a word should be resolved to a place or not.  For example, the model will evaluate that 'Obama' is usually meant as the president and not the place in Japan.  In other words, it decides whether a place should be resolved for the originating word at all.
| name                           | type    | description                    | example |
| ------------------------------ | ------- | ------------------------------ | --------|
| second_round_score             | float   | score from second round        | 1.4213  |
| place_frequency                | float   | how often name is a place in Wikipedia | |
