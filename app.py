import os
import random
import mne
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="EEG Psychological Analyzer", layout="wide")
st.title("EEG Psychological Analyzer 🧠")

# ----------------------------
# 1️⃣ EEG Dosya Yükleme
# ----------------------------
root_path = "data"  # EEG dataset klasörü
edf_files = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith(".edf"):
            edf_files.append(os.path.join(root, file))

st.write(f"Total EEG data files: {len(edf_files)}")

# ----------------------------
# 2️⃣ Kullanıcı geçmişi (simülasyon)
# ----------------------------
if 'history' not in st.session_state:
    st.session_state['history'] = []  # Son testlerin tahminleri

# ----------------------------
# 3️⃣ Test butonu
# ----------------------------
if st.button("Run EEG Analysis"):
    if len(edf_files) == 0:
        st.warning("No EEG data found!")
    else:
        # Rastgele EEG dosya seç
        random_file = random.choice(edf_files)
        st.write(f"Randomly chosen file: {random_file}")

        # EEG verisini oku ve filter uygula
        raw = mne.io.read_raw_edf(random_file, preload=True)
        raw.filter(0.5,50)
        data = raw.get_data()
        channel_power = [round((d**2).mean(),2) for d in data]
        st.write("Channel-based power (first 5 channels):", channel_power[:5])

        # ----------------------------
        # 4️⃣ Prediction
        # ----------------------------
        prediction = random.choice(['stressed','tired','normal'])
        recommendations = {
            'stressed': 'Take a 5-minute break and do breathing exercises.',
            'tired': 'Consider resting or short nap.',
            'normal': 'Keep up your healthy routine!'
        }
        st.success(f"Prediction: {prediction}")
        st.info(f"Advice: {recommendations[prediction]}")

        # ----------------------------
        # 5️⃣ Visual Emotional State Card
        # ----------------------------
        colors = {'stressed':'#FF4C4C', 'tired':'#FFD700', 'normal':'#4CAF50'}
        st.markdown(f"""
        <div style="background-color:{colors[prediction]}; 
                    color:white; 
                    padding:20px; 
                    border-radius:10px; 
                    text-align:center;
                    font-size:24px;">
            {prediction.upper()}
        </div>
        """, unsafe_allow_html=True)

        # ----------------------------
        ## ----------------------------
# 6️⃣ Guided Breathing (Yeni)
# ----------------------------
st.subheader("Guided Breathing Exercise")

def breathing_exercise():
    placeholder = st.empty()  # Animasyon için
    phases = [("Inhale",4), ("Hold",4), ("Exhale",4)]
    for phase, seconds in phases:
        for i in range(seconds,0,-1):
            placeholder.markdown(f"<h2 style='color:#4CAF50'>{phase}... {i}</h2>", unsafe_allow_html=True)
            st.sleep(1)
    placeholder.markdown("<h2 style='color:#2196F3'>Breathing cycle completed! 🌬️</h2>", unsafe_allow_html=True)

if st.button("Start Breathing Exercise"):
    breathing_exercise()

# ----------------------------
# 7️⃣ Personalized Emotional Tracker (Tablo)
# ----------------------------
st.subheader("Personalized EEG History")

from datetime import datetime
# Yeni entry ekle
st.session_state['history'].append({
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "prediction": prediction,
    "advice": recommendations[prediction]
})

# Son 10 testi göster
history_table = st.session_state['history'][-10:]
st.table(history_table)
