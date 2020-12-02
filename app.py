from flask import Flask, render_template, url_for, request, redirect
import requests

app = Flask(__name__)

@app.route('/',  methods=['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        zip_content = request.form['zip']
        zip_three = zip_content[0:3]
        try:
            api = ('http://api.openweathermap.org/data/2.5/weather?zip='+zip_three+',ca&appid=d013ca1ae46dcf5e4a12dce7a0910a34')

            obj = requests.get(api).json()
            icon = obj['weather'][0]['icon']
            icon_url = "http://openweathermap.org/img/w/" + icon + ".png"

            kelvin_t = float(obj['main']['temp'])
            feels_like = float(obj['main']['feels_like'])
            humidity = float(obj['main']['humidity'])
            pressure = float(obj['main']['pressure'])
            icon = obj['weather'][0]['icon']
            description = obj['weather'][0]['description']
            city = obj['name']

            celsius_t = (kelvin_t - 273.15)
            feels_like = (feels_like - 273.15)
    
            return render_template("index.html", weather="Fall", temp=round(celsius_t),feels_like=round(feels_like), humidity=round(humidity), pressure=round(pressure), icon_url=icon_url, description=description, city =city)
        except:
            return render_template("error.html")
    else:
        return render_template("welcome.html")

@app.route('/index.html',  methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        zip_content = request.form['zip']
        zip_three = zip_content[0:3]
        try:
            api = ('http://api.openweathermap.org/data/2.5/weather?zip='+zip_three+',ca&appid=d013ca1ae46dcf5e4a12dce7a0910a34')

            obj = requests.get(api).json()
            icon = obj['weather'][0]['icon']
            icon_url = "http://openweathermap.org/img/w/" + icon + ".png"

            kelvin_t = float(obj['main']['temp'])
            feels_like = float(obj['main']['feels_like'])
            humidity = float(obj['main']['humidity'])
            pressure = float(obj['main']['pressure'])
            icon = obj['weather'][0]['icon']
            description = obj['weather'][0]['description']
            city = obj['name']

            celsius_t = (kelvin_t - 273.15)
            feels_like = (feels_like - 273.15)
    
            return render_template("index.html", weather="Fall", temp=round(celsius_t),feels_like=round(feels_like), humidity=round(humidity), pressure=round(pressure), icon_url=icon_url, description=description, city =city)
            
            # return redirect('/')
        except:
            return render_template("error.html")

    else:
        postalcode = 'N8W'
        api = ('http://api.openweathermap.org/data/2.5/weather?zip='+postalcode+',ca&appid=d013ca1ae46dcf5e4a12dce7a0910a34')

        obj = requests.get(api).json()
        icon = obj['weather'][0]['icon']
        icon_url = "http://openweathermap.org/img/w/" + icon + ".png"

        kelvin_t = float(obj['main']['temp'])
        feels_like = float(obj['main']['feels_like'])
        humidity = float(obj['main']['humidity'])
        pressure = float(obj['main']['pressure'])
        icon = obj['weather'][0]['icon']
        description = obj['weather'][0]['description']
        city = obj['name']

        celsius_t = (kelvin_t - 273.15)
        feels_like = (feels_like - 273.15)
    
        return render_template("index.html", weather="Fall", temp=round(celsius_t),feels_like=round(feels_like), humidity=round(humidity), pressure=round(pressure), icon_url=icon_url, description=description, city =city)

@app.route("/aboutus.html")
def aboutus():
    return render_template("aboutus.html")
