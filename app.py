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
        # 6️⃣ Breathing / Guided Regulation
        # ----------------------------
        st.subheader("Guided Breathing Exercise")
        st.write("Inhale for 4 seconds → Hold 4 seconds → Exhale 4 seconds")
        if st.button("Start Breathing Exercise"):
            for i in range(4):
                st.write(f"Inhale... {4-i}")
                st.sleep(1)
            for i in range(4):
                st.write(f"Hold... {4-i}")
                st.sleep(1)
            for i in range(4):
                st.write(f"Exhale... {4-i}")
                st.sleep(1)
            st.success("Breathing cycle completed!")

        # ----------------------------
        # 7️⃣ Personalized Emotional Tracker
        # ----------------------------
        st.session_state['history'].append(prediction)
        if len(st.session_state['history']) > 10:  # son 10 testi sakla
            st.session_state['history'].pop(0)

        st.subheader("Last EEG Predictions Trend")
        fig, ax = plt.subplots()
        x = list(range(1,len(st.session_state['history'])+1))
        y = [ {'stressed':2,'tired':1,'normal':0}[p] for p in st.session_state['history'] ]
        ax.plot(x,y, marker='o')
        ax.set_yticks([0,1,2])
        ax.set_yticklabels(['normal','tired','stressed'])
        ax.set_xlabel("Test #")
        ax.set_ylabel("Mental State")
        ax.set_title("Personalized EEG Trend")
        st.pyplot(fig)
