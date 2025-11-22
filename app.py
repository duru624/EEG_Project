from google.colab import drive
drive.mount('/content/drive')

!pip install mne streamlit pyngrok --quiet

import os
import random

root_path = "data"
edf_files = []

for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith(".edf"):
            edf_files.append(os.path.join(root, file))

print("Total data files:", len(edf_files))

# Test için rastgele dosya seç
random_file = random.choice(edf_files)
print("Randomly choosen data:", random_file)


import mne

# Dosyayı oku
raw = mne.io.read_raw_edf(random_file, preload=True)

# Basit filter
raw.filter(0.5, 50)

# Kanal bazlı güç (feature extraction örneği)
data = raw.get_data()
channel_power = [round((d**2).mean(), 2) for d in data]
print("Channel-based power (first 5 channels):", channel_power[:5])


prediction = random.choice(["stressed", "tired", "normal"])
recommendations = {
    "stressed": "Take a 5-minute break and do breathing exercises.",
    "tired": "Consider resting or short nap.",
    "normal": "Keep up your healthy routine!"
}

print("Prediction:", prediction)
print("Advice:", recommendations[prediction])




# Streamlit uygulaması
app_code = """
import streamlit as st
import random
import mne
import os

st.title('EEG Psychological Analyzer')

# EEG dosya listesi
root_path = "/content/drive/MyDrive/replicate/EEG"
edf_files = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith('.edf'):
            edf_files.append(os.path.join(root, file))

st.write(f"Total EEG data set: {len(edf_files)}")

if st.button('Test Et'):
    if len(edf_files) == 0:
        st.warning("EROR Data Set Couldn't Be Found.")
    else:
        random_file = random.choice(edf_files)
        st.write('Randomly choosen data:', random_file)
        
        raw = mne.io.read_raw_edf(random_file, preload=True)
        raw.filter(0.5,50)
        data = raw.get_data()
        channel_power = [round((d**2).mean(),2) for d in data]
        st.write('Channel-based power (first 5 channels):', channel_power[:5])

        prediction = random.choice(['stressed','tired','normal'])
        recommendations = {
            'stressed': 'Take a 5-minute break and do breathing exercises.',
            'tired': 'Consider resting or short nap.',
            'normal': 'Keep up your healthy routine!'
        }
        st.success(f"Prediction: {prediction}")
        st.info(f"Advice: {recommendations[prediction]}")
"""

with open("app.py","w") as f:
    f.write(app_code)


from pyngrok import ngrok
import subprocess
import time


ngrok.set_auth_token("35pM0r1tZv7ltkYTJ34p3l1CWaH_2uvuS2GgX9ZREhVJGCnaF")

# Streamlit’i arka planda çalıştır
subprocess.Popen(["streamlit","run","app.py","--server.port=8501"])

# Ngrok ile link oluştur
time.sleep(3)
url = ngrok.connect(8501)
print("Link to your site:", url)
