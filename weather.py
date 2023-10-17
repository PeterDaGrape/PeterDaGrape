from bs4 import BeautifulSoup
import requests      



class weather:
    def __init__(self, city_name):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        
        city_name = city_name.replace(" ", "+")
      
        res = requests.get(
            f'https://www.google.com/search?q={city_name}+weather&client=safari&sca_esv=573484139&source=hp&ei=eM4qZbXdPMmFxc8Pvrep4Ak&iflsig=AO6bgOgAAAAAZSrcidnjKX45CNzVmejBGwtcrXNuoE_Z&ved=0ahUKEwi1-ZbohvaBAxXJQvEDHb5bCpwQ4dUDCAs&uact=5&oq=canterbury+weather&gs_lp=Egdnd3Mtd2l6IhJjYW50ZXJidXJ5IHdlYXRoZXJIlxtQAFiTGnAAeACQAQKYAQCgAQCqAQC4AQPIAQD4AQE&sclient=gws-wiz', headers=headers)
      
        print("Loading...")
  
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select('#wob_loc')[0].getText().strip()
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        temperature = soup.select('#wob_tm')[0].getText().strip()
  
        print("Location: " + location)
        print("Temperature: " + temperature + "&deg;C")
        print("Time: " + time)
        print("Weather Description: " + info)


weather('Canterbury')