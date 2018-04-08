# Models
This document describe the various models used by **MARGE** to make predictions.
**MARGE** makes multiple passes over the data in the same way that a human would make multiple drafts.

### First Pass
This is the data that **MARGE** looks at during the first pass.

| name                           | type    | description                    | example |
| ------------------------------ | ------- | ------------------------------ | --------|
| has_enwiki_title               | boolean | Matched with Wikidata          | 1       |
| has_population_over_1_million  | boolean | Has population over 1 million  | 0       |
| has_population_over_1_thousand | boolean | Has population over 1 thousand | 1       |
| has_population_over_1_hundred  | boolean | Has population over 1 hundred  | 0       |
| importance                     | float   | Importance from OSMNames       | 0.54    |

### Second Pass
| name                           | type    | description                    | example |
| ------------------------------ | ------- | ------------------------------ | --------|
| country_code_rank              | integer | Number describing rank in popularity of country_code among most likely place | 1 |
| has_enwiki_title               | boolean | Matched with Wikidata          | 1       |
| has_population_over_1_million  | boolean | Has population over 1 million  | 0       |
| has_population_over_1_thousand | boolean | Has population over 1 thousand | 1       |
| has_population_over_1_hundred  | boolean | Has population over 1 hundred  | 0       |
| importance                     | float   | Importance from OSMNames       | 0.54    |
