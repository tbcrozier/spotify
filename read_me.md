# Spotify API Exploration

#### Notes
- GPT - https://chatgpt.com/c/680da277-66d8-8000-adc1-f13b008cb186
- https://github.com/Mariyajoseph24/Spotify_Data_Analysis_Python_Project/blob/main/spotify.ipynb

#### spotify_auth.py
- Run this to acquire api token
- utilizes .envs variables

#### historic_load.py
- Loads data  from data/historic/Spotify%History/*json
- Loads to bq dataset


#### spotify/spotify-streaming-pipeline/
- terraform directory
- python cloud function code
- to zip new CF files:
    - cd into cloud_functions dir
    - zip ../cloud_function.zip main.py requirements.txt
    - unzip -l cloud_function.zip
- need to add     SPOTIFY_ACCESS_TOKEN = "your-spotify-access-token-here". Can possibly reference it from .env file




