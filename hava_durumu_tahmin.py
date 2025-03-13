import requests 
import gradio as gr
from api_reader import OPENWEATHER_API_KEY 

API_KEY = OPENWEATHER_API_KEY
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q" : city , 
        "appid" : API_KEY , 
        "units" : "metric" ,
        "lang" : "tr" 
    }
    response = requests.get(BASE_URL , params=params)
    data = response.json()

    if response.status_code == 200:
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        city = city.capitalize()
        return f"{city} şuanda {description} ve sıcaklık {temperature}°C."
    else : 
        return "Üzgünüm , ben sadece OpenWeatherAPI kullanarak güncel hava raporu sunan bir asistanım."

# city = input("Şehir giriniz: ")
# print(get_weather(city))

## used custom theme from https://huggingface.co/spaces/gradio/theme-gallery
with gr.Blocks(theme = 'John6666/YntecDark') as demo : 
    gr.Markdown("## OpenWeather API - Güncel Hava Raporu")
    with gr.Row():
        with gr.Column() :
            selected_city = gr.Textbox(label = "Şehir giriniz" , placeholder= "Şehir")
            submit_btn = gr.Button("Hava Durumu Tahmini Yap")
            clear_btn = gr.Button("Temizle")
        with gr.Column():
            forecast = gr.Textbox(label = "Güncel Hava Durumu")

    selected_city.submit(
        get_weather , 
        [selected_city] ,
        [forecast] 

    )

    submit_btn.click(
        get_weather , 
        [selected_city] , 
        [forecast]
    )

    clear_btn.click(
        lambda : (None , None) , 
        [] , 
        [selected_city , forecast]
    )

if __name__ == "__main__" : 
    demo.launch(show_error=True)


