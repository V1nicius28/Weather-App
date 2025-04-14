from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
import requests
import pytz
from PIL import Image, ImageTk
import io

root = Tk()
root.title("Weather App")
root.geometry("900x470+300+200")
root.configure(bg="#1c3c6a")
root.resizable(False, False)

def getWeather():
    try:
        city = textfield.get()
        geolocator = Nominatim(user_agent="weather_app_vgm")
        location = geolocator.geocode(city)

        if location is None:
            messagebox.showerror("Erro", "Cidade não encontrada.")
            return

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        timezone.config(text=result)
        long_lat.config(text=f"{round(location.latitude, 4)}°N, {round(location.longitude, 4)}°E")

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)

        # OpenWeather
        openweather_api = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&units=metric&appid=API_Key"
        json_data = requests.get(openweather_api).json()

        # WeatherAPI Forecast (7 dias)
        weatherapi_url = f"http://api.weatherapi.com/v1/forecast.json?key=API_Key&q={location.latitude},{location.longitude}&days=7"
        forecast_data = requests.get(weatherapi_url).json()

        # Informações atuais
        temp = json_data['main']['temp']
        humidity = json_data['main']['humidity']
        pressure = json_data['main']['pressure']
        wind = json_data['wind']['speed']
        description = json_data['weather'][0]['description']

        t.config(text=f"{temp} °C")
        h.config(text=f"{humidity} %")
        p.config(text=f"{pressure} hPa")
        w.config(text=f"{wind} m/s")
        d.config(text=description.title())


        # Datas dos próximos 7 dias
        today = datetime.now()
        dias = [day1, day2, day3, day4, day5, day6, day7]
        temperaturas = [day1temp, day2temp, day3temp, day4temp, day5temp, day6temp, day7temp]
        imagens = [firstimage, secondimage, thirdimage, fourthimage, fifthimage, sixthimage, seventhimage]

        for i in range(7):
            dias[i].config(text=(today + timedelta(days=i)).strftime("%A"))
            icon_url = "https:" + forecast_data['forecast']['forecastday'][i]['day']['condition']['icon']
            icon_response = requests.get(icon_url)
            icon_data = icon_response.content
            icon_image = Image.open(io.BytesIO(icon_data))

            # Aumenta o tamanho apenas do primeiro dia
            if i == 0:
                icon_image = icon_image.resize((80, 80))  
            else:
                icon_image = icon_image.resize((50, 50))  
            icon_photo = ImageTk.PhotoImage(icon_image)
            imagens[i].config(image=icon_photo)
            imagens[i].image = icon_photo  

            # Temperatura
            max_temp = forecast_data['forecast']['forecastday'][i]['day']['maxtemp_c']
            min_temp = forecast_data['forecast']['forecastday'][i]['day']['mintemp_c']
            temperaturas[i].config(text=f"{int(max_temp)}°/ {int(min_temp)}°")


    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


##icon
image_icon=PhotoImage(file="Images/logo.png")
root.iconphoto(False,image_icon)

Round_box=PhotoImage(file="Images/RoundedRectangle 1.png")
Label(root,image=Round_box,bg="#1c3c6a").place(x=30,y=110)

#label
label1=Label(root,text="Temperature",font=('Helvetica',11),fg="white",bg="#27334F")
label1.place(x=50,y=120)

label2=Label(root,text="Humidity",font=('Helvetica',11),fg="white",bg="#27334F")
label2.place(x=50,y=140)

label3=Label(root,text="Pressure",font=('Helvetica',11),fg="white",bg="#27334F")
label3.place(x=50,y=160)

label4=Label(root,text="Wind Speed",font=('Helvetica',11),fg="white",bg="#27334F")
label4.place(x=50,y=180)

label5=Label(root,text="Description",font=('Helvetica',11),fg="white",bg="#27334F")
label5.place(x=50,y=200)


##search box
Search_image=PhotoImage(file="Images/RoundedRectangle 3.png")
myimage=Label(image=Search_image,bg="#1c3c6a")
myimage.place(x=310,y=120)

weat_image=PhotoImage(file="Images/Layer 7.png")
weatherimage=Label(root,image=weat_image,bg="#27334F")
weatherimage.place(x=325,y=132)

textfield=tk.Entry(root,justify='center',width=15,font=('poppins',24,'bold'),bg="#27334F",border=0,fg="white")
textfield.place(x=370,y=128)
textfield.focus()
textfield.bind("<Return>", lambda event: getWeather())

Search_icon=PhotoImage(file="Images/Layer 6.png")
myimage_icon=Button(image=Search_icon,borderwidth=0,cursor="hand2",bg="#27334F", command=getWeather)
myimage_icon.place(x=685,y=133)


##Botton box
frame=Frame(root,width=900,height=180,bg="#152341")
frame.pack(side=BOTTOM)

#bottom boxes
firstbox=PhotoImage(file="Images/RoundedRectangle 4.png")
secondbox=PhotoImage(file="Images/RoundedRectangle 2.png")

Label(frame,image=firstbox,bg="#152341").place(x=30,y=20)
Label(frame,image=secondbox,bg="#152341").place(x=300,y=27)
Label(frame,image=secondbox,bg="#152341").place(x=400,y=27)
Label(frame,image=secondbox,bg="#152341").place(x=500,y=27)
Label(frame,image=secondbox,bg="#152341").place(x=600,y=27)
Label(frame,image=secondbox,bg="#152341").place(x=700,y=27)
Label(frame,image=secondbox,bg="#152341").place(x=800,y=27)


#clock (here we will place time)
clock=Label(root,font=("Helvetica",30,'bold'),fg="white",bg="#1c3c6a")
clock.place(x=30,y=20)


#timezone
timezone=Label(root,font=("Helvetica",20),fg="white",bg="#1c3c6a")
timezone.place(x=500,y=15)


long_lat=Label(root,font=("Helvetica",10),fg="white",bg="#1c3c6a")
long_lat.place(x=530,y=50)


#thpwd
t=Label(root,font=("Helvetica",11),fg="white",bg="#27334F")
t.place(x=150,y=120)
h=Label(root,font=("Helvetica",11),fg="white",bg="#27334F")
h.place(x=150,y=140)
p=Label(root,font=("Helvetica",11),fg="white",bg="#27334F")
p.place(x=150,y=160)
w=Label(root,font=("Helvetica",11),fg="white",bg="#27334F")
w.place(x=150,y=180)
d=Label(root,font=("Helvetica",11),fg="white",bg="#27334F")
d.place(x=150,y=200)


#first cell
firstframe=Frame(root,width=221,height=120,bg="#27334f")
firstframe.place(x=42,y=322)

day1=Label(firstframe,font="arial 20",bg="#27334f",fg="#fff")
day1.place(x=100,y=5)

firstimage=Label(firstframe,bg="#27334f")
firstimage.place(x=10,y=13)

day1temp=Label(firstframe,bg="#27334f",fg="#57adff",font="arial 18 bold")
day1temp.place(x=100,y=50)

#second cell
secondframe=Frame(root,width=64,height=104,bg="#1c2a47")
secondframe.place(x=307,y=332)

day2=Label(secondframe,bg="#1c2a47",fg="#fff")
day2.place(x=0,y=2)

secondimage=Label(secondframe,bg="#1c2a47")
secondimage.place(x=5,y=25)

day2temp=Label(secondframe,bg="#1c2a47",fg="#57adff",font="arial 12 bold")
day2temp.place(x=5,y=80)

#third cell
thirdframe=Frame(root,width=64,height=104,bg="#1c2a47")
thirdframe.place(x=407,y=332)

day3=Label(thirdframe,bg="#1c2a47",fg="#fff")
day3.place(x=0,y=2)

thirdimage=Label(thirdframe,bg="#1c2a47")
thirdimage.place(x=5,y=25)

day3temp=Label(thirdframe,bg="#1c2a47",fg="#57adff",font="arial 12 bold")
day3temp.place(x=5,y=80)

#fourth cell
fourthframe=Frame(root,width=64,height=104,bg="#1c2a47")
fourthframe.place(x=507,y=332)

day4=Label(fourthframe,bg="#1c2a47",fg="#fff")
day4.place(x=0,y=2)

fourthimage=Label(fourthframe,bg="#1c2a47")
fourthimage.place(x=5,y=25)

day4temp=Label(fourthframe,bg="#1c2a47",fg="#57adff",font="arial 12 bold")
day4temp.place(x=5,y=80)

#fifth cell
fifthframe=Frame(root,width=64,height=104,bg="#1c2a47")
fifthframe.place(x=607,y=332)

day5=Label(fifthframe,bg="#1c2a47",fg="#fff")
day5.place(x=0,y=2)

fifthimage=Label(fifthframe,bg="#1c2a47")
fifthimage.place(x=5,y=25)

day5temp=Label(fifthframe,bg="#1c2a47",fg="#57adff",font="arial 12 bold")
day5temp.place(x=5,y=80)

#sixth cell
sixthframe=Frame(root,width=64,height=104,bg="#1c2a47")
sixthframe.place(x=707,y=332)

day6=Label(sixthframe,bg="#1c2a47",fg="#fff")
day6.place(x=0,y=2)

sixthimage=Label(sixthframe,bg="#1c2a47")
sixthimage.place(x=5,y=25)

day6temp=Label(sixthframe,bg="#1c2a47",fg="#57adff",font="arial 12 bold")
day6temp.place(x=5,y=80)

#seventh cell
seventhframe=Frame(root,width=64,height=104,bg="#1c2a47")
seventhframe.place(x=807,y=332)

day7=Label(seventhframe,bg="#1c2a47",fg="#fff")
day7.place(x=0,y=2)

seventhimage=Label(seventhframe,bg="#1c2a47")
seventhimage.place(x=5,y=25)

day7temp=Label(seventhframe,bg="#1c2a47",fg="#57adff",font="arial 12 bold")
day7temp.place(x=5,y=80)

root.mainloop()
