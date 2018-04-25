# Failed Methods
Tracking all the failed ML methods

# country_code_frequency
got a negative coefficient
implying there's some weirdness with Wikipedia data

# place_type_frequency
same as above

# percent_fields_complete
GeoNames fields might be more complete, giving them undue weight here over OSM

# country_code_has_match
Got negative coefficient. True if no more than one feature or more than one feature has country_code of item

# is_admin
Failed because most places aren't admin
