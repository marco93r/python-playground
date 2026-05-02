import requests, sys

def get_coordinates(city):
    request_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    request_data = requests.get(request_url).json()
    try:
        result_dict = request_data['results']
    except(KeyError):
        result_dict = {}

    if len(result_dict) == 0:
        pass
    else:
        lat = result_dict[0]['latitude']
        lon = result_dict[0]['longitude']
        return lat, lon

def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lon) + "&current=temperature_2m,wind_speed_10m"
    data = requests.get(url).json()
    temperature = data['current']['temperature_2m']
    wind_speed = data['current']['wind_speed_10m']
    return temperature, wind_speed

def main():
    city = input('Enter city: ')
    try:
        lat, lon = get_coordinates(city)
    except(TypeError):
        print('City not found')
        sys.exit()
    temperature, wind_speed = get_weather(lat, lon)
    print('Weather for ' + city)
    print('Temperature:' ,temperature, '°C')
    print('Wind speed:', wind_speed, 'km/h')

main()




