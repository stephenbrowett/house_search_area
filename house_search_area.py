# https://docs.traveltimeplatform.com/reference/time-map#arrival_searches

import os
import json
import requests
import numpy as np
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

mapbox_access_token = os.getenv("mapbox_access_token")
application_id = os.getenv("application_id")
api_key = os.getenv("api_key")

host = "http://api.traveltimeapp.com/v4/time-map"

header = {
	"Content-Type" : "application/json",
	"Accept" : "application/json",
	"X-Application-Id" : application_id,
	"X-Api-Key" : api_key
	}

with open("data\input.json", "r") as infile:
	tmp_req_data = json.load(infile)

req_data = {
	"arrival_searches" : []
}

for req in tmp_req_data:
	tmp = req
	tmp_bool = tmp['range']['enabled'] == 'True'
	tmp_id = str(ObjectId())

	tmp['range']['enabled'] = tmp_bool
	tmp['id'] = tmp_id

	req_data['arrival_searches'].append(tmp)

req = requests.post(url = host, headers = header, json = req_data)

if req.status_code != 200:
	req.raise_for_status()

results = req.json()


cmap = plt.cm.get_cmap('plasma')
people = np.linspace(0, 1, len(results['results']))

data = []
mean_lats = []
mean_lons = []
for n, result in enumerate(results['results']):

	colour = cmap(people[n])
	rgb_colour = f"rgb{tuple(int((255*x)) for x in colour[0:3])}"

	for i in result['shapes']:
		lats = [j['lat'] for j in i['shell']]
		lons = [j['lng'] for j in i['shell']]

		mean_lats.append(lats)
		mean_lons.append(lons)

		data.append(
			go.Scattermapbox(
				fill = "toself",
				lat = lats,
				lon = lons,
				marker = go.scattermapbox.Marker(
					size = 10,
					color = rgb_colour,
					opacity = 0.0
				),
				name = f"person {n}'s locations"
			)
		)

mean_lat = np.mean(np.concatenate(mean_lats))
mean_lon = np.mean(np.concatenate(mean_lons))

layout = go.Layout(
	title = 'Commute Locations',
	autosize = True,
	hovermode = 'closest',
	showlegend = True,
	mapbox = go.layout.Mapbox(
		accesstoken = mapbox_access_token,
		bearing = 0,
		center = go.layout.mapbox.Center(
			lat = mean_lat,
			lon = mean_lon
		),
		pitch = 0,
		zoom = 5,
		style = 'light'
	),
)
fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = "CommuteableArea.html")

