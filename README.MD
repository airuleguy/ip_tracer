# Rodrigo Urban

## Ip Tracer

"""
I only have 1000 api calls per month so I should
schedule this every 2 hours to update
"""
Money symbols are not available in the currency API so I used a json.

This is an ip that parses ip address and returns interesting data about it, it was made with:

- Django
- Postgres
- Redis for cache

The conversion rate needs to be updated fairly regularly. Since the currency API is privated, the amount of free request is limited to 1000 per month so I decided to schedule a task every 2 hours to update the rates.

## How to run it locally

```
docker-compose up --build -d
```

When the images are up and running you can test the endpoints, using curl, postman, or
any tool of your liking.

## Resources description

### /traces/ METHOD: POST

Given an ip address returns information about it.
Example request body

```
{
    "ip":"167.62.158.169"
}
```

### /statistics/ METHOD: GET

Returns longest distance from requested traces and most traced country.
Does not requires any payload.
