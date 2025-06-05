# Geography Filter Options

The DataAxle Scraper now supports multiple geography search types. You can choose from 5 different geography options by modifying the `referenceusa_config.yaml` file.

## Available Geography Types

### 1. State Search (Default)
```yaml
geography_type: 'state'
state: 'California'
```
Searches for businesses within an entire state.

### 2. City/State Search
```yaml
geography_type: 'city_state'
city_state: 'Atlanta, GA'
```
Searches for businesses within a specific city and state combination.

### 3. Metro Area Search
```yaml
geography_type: 'metro_area'
metro_area: 'Atlanta-Sandy Springs-Alpharetta, GA'
```
Searches for businesses within a specific metropolitan statistical area (MSA).

### 4. County Search
```yaml
geography_type: 'county'
county: 'Fulton, GA'
```
Searches for businesses within a specific county. You can include the state for better accuracy.

### 5. ZIP Code Search
```yaml
geography_type: 'zip_codes'
zip_codes: '30309,30318,30324,30327'
```
Searches for businesses within specific ZIP codes. Provide a comma-separated list of ZIP codes.

## How to Configure

1. Open `config/referenceusa_config.yaml`
2. Find the `search_parameters` section
3. Uncomment the geography type you want to use
4. Comment out the other geography options
5. Make sure only ONE geography type is active at a time

## Examples

### Example 1: Search Atlanta Metro Area
```yaml
search_parameters:
  include_closed: false
  include_unverified: true
  # geography_type: 'state'
  # state: New Mexico
  
  geography_type: 'metro_area'
  metro_area: 'Atlanta-Sandy Springs-Alpharetta, GA'
```

### Example 2: Search Multiple ZIP Codes
```yaml
search_parameters:
  include_closed: false
  include_unverified: true
  # geography_type: 'state'
  # state: New Mexico
  
  geography_type: 'zip_codes'
  zip_codes: '10001,10002,10003,10004,10005'
```

### Example 3: Search by County
```yaml
search_parameters:
  include_closed: false
  include_unverified: true
  # geography_type: 'state'
  # state: New Mexico
  
  geography_type: 'county'
  county: 'Cook, IL'
```

## Notes

- Only one geography type can be active at a time
- The scraper will automatically select the appropriate search interface on ReferenceUSA
- Metro Area names should match exactly as they appear in ReferenceUSA
- County names can include the state abbreviation for better accuracy
- ZIP codes should be comma-separated with no spaces around commas
- City/State combinations should follow the format "City, ST"
