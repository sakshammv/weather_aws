from urllib import response
from boto3 import resource
import config
from flask import Flask, render_template, request
import json
import urllib.request


#AWS access keys

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME
 
resource = resource(
   'dynamodb',
   aws_access_key_id     = AWS_ACCESS_KEY_ID,
   aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
   region_name           = REGION_NAME
)

app = Flask(__name__)
  
@app.route('/', methods =['GET'])
def weather():
    city = "Wardha"
  
    table = resource.Table('weather_spotsense')
   
    # json data from api
    source1 = urllib.request.urlopen('http://api.weatherapi.com/v1/current.json?key=e6acd944981341e6a8b90521221105%20&q='+city+'&aqi=no').read()
    source2 = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=7dc291aeffe2ddfd6e8dd8b708cf7027').read()
  
    # JSON data to a dictionary

    list_of_data1 = json.loads(source1)
    list_of_data2 = json.loads(source2)

    response1 = table.put_item(
       Item = {
           'ID'     : "wardha1",
           'temp'   :  str(list_of_data1['current']['temp_c']),
           'api'    : "weatherapi"
       }
    )

    response2 = table.put_item(
       Item = {
           'ID'     : "wardha2",
           'temp'   :  str(list_of_data2['main']['temp'] - 273),
           'api'    : "openweathermap"
       }
    )

    print( " response " + str(response))
    
    return render_template('index.html', data = list_of_data1, data2 = list_of_data2)
  
if __name__ == '__main__':
    app.run(debug = True)