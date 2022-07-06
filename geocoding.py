#!pip3 install pandaralel
import country_converter as coco
import http.client, urllib.parse
import json
import pandas
from pandarallel import pandarallel


#collect lat,long metadata for visualization
NGO_name_country=pd.read_csv("./data/NGO_name_country.csv").query("record!=0")
NGO_metadata=pd.merge(NGO_name_country,modularity_blocks,how="inner",left_on="NGO_name",right_on="NGO").drop(["NGO","record"],axis=1)

some_names = NGO_metadata.country_name
standard_names = coco.convert(names=some_names, to='ISO3')
NGO_metadata.country_name= standard_names
NGO_metadata["lat"]=np.nan
NGO_metadata["lon"]=np.nan


conn = http.client.HTTPConnection('api.positionstack.com')

pandarallel.initialize(progress_bar=True)


def get_coordinates(address):
  try:
    params = urllib.parse.urlencode({
        'access_key': 'YOUR_ACCESS_KEY_FOR_API',
        'query': address,
        'limit': 1,
        })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    data = res.read()
    data_parsed=json.loads(data.decode('utf-8'))['data'][0]
    lat = data_parsed["latitude"]
    lon = data_parsed["longitude"]
  except:
    lat=None
    lon=None
  
  return pd.Series([lat,lon])
NGO_metadata[["lat","lon"]] = NGO_metadata.NGO_address.parallel_apply(get_coordinates)
NGO_metadata.to_csv("NGO_metadata.csv")