# house_search_area

This project is designed to highlight an appropriate region for 1 or more people to reach given a dict describing how long they're prepared to travel for. The project is an example usage of the `traveltimeapp` API and plotting on a map using plotly.

For example:
- finding the region where 2 or more people could live and both still commute to their jobs,
- finding the region in which a new business could open its offices which is close to the founders,
- narrowing down the region where a group of friends could go for a holiday,
and much more!

In order ot use this project you'll need to register at `mapbox` to get an access token and at `traveltimeapp` to get an application ID and API key. Then use these keys to fill in the relevant fields in the `.env` file in the top-level directory

For a description of how to form the `input.json` file, please refer to the API documentation at: https://traveltime.com/docs/api/reference/isochrones#request-body-json-attributes
