# Data Axle Scraper - Geography Filtering Guide

## How to Use Geography Filters

The Data Axle Scraper supports various geography filters using the `state` parameter or the `zip_codes` parameter in the configuration file.

## Configuration

Open the `config/referenceusa_config.yaml` file and edit either the `state` parameter or the `zip_codes` parameter under `search_parameters`.

## State/City/County/MSA Filtering

You can enter any of the following formats in the `state` parameter:

### State Only
```yaml
search_parameters:
  state: "California"
```
This will search for all businesses in California.

### City and State
```yaml
search_parameters:
  state: "Miami, FL"
```
This will search for businesses specifically in Miami, Florida.

### County
```yaml
search_parameters:
  state: "Orange County"
```
This will search for businesses in Orange County.

### Metropolitan Statistical Area (MSA)
```yaml
search_parameters:
  state: "Dallas-Fort Worth-Arlington"
```
This will search for businesses in the Dallas-Fort Worth-Arlington metropolitan area.

## ZIP Code Filtering

You can also filter by ZIP codes using the `zip_codes` parameter:

### Single ZIP Code
```yaml
search_parameters:
  zip_codes: "30339"
```
This will search for businesses in the 30339 ZIP code.

### Multiple ZIP Codes
```yaml
search_parameters:
  zip_codes: "30339, 30080, 30060"
```
This will search for businesses in any of the listed ZIP codes.

## Important Notes

- You can use either `state` OR `zip_codes`, but not both at the same time.
- If both are specified, the system will prioritize the `zip_codes` parameter.
- For ZIP codes, separate multiple values with commas.
- For city and state searches, make sure to include the comma between city and state: "Chicago, IL"
- For counties, you may need to include the word "County" depending on how Data Axle formats it
- For MSAs, use the standard MSA naming convention

## Examples

```yaml
# State only
state: "New York"

# City and State
state: "Chicago, IL"

# County
state: "Fulton County"

# MSA
state: "New York-Newark-Jersey City"

# Single ZIP code
zip_codes: "10001"

# Multiple ZIP codes
zip_codes: "10001, 10002, 10003"
```

The scraper will use exactly what you type in the search box on the Data Axle site, so format your search term as you would if searching manually.
