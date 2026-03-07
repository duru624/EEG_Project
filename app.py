import os
import random
import mne
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="EEG Psychological Analyzer", layout="wide")

# ----------------------------
# 0️⃣ Kullanıcı yönetimi
# ----------------------------
if 'users' not in st.session_state:
    st.session_state['users'] = {}  # username -> history list
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'breathing_active' not in st.session_state:
    st.session_state['breathing_active'] = False

# ----------------------------
# Sidebar: Login/Register
# ----------------------------
st.sidebar.title("User Login / Register")

with st.sidebar.form("login_form"):
    username = st.text_input("Username")
    col1, col2 = st.columns(2)
    login_clicked = col1.form_submit_button("Login")
    register_clicked = col2.form_submit_button("Register")
    
    if login_clicked:
        if username in st.session_state['users']:
            st.session_state['current_user'] = username
            st.sidebar.success(f"Welcome back {username}!")
        else:
            st.sidebar.warning("User not found!")
            
    if register_clicked:
        if username.strip() != "" and username not in st.session_state['users']:
            st.session_state['users'][username] = []
            st.session_state['current_user'] = username
            st.sidebar.success(f"User {username} registered!")
        else:
            st.sidebar.warning("Invalid username or already exists")

# ----------------------------
# 1️⃣ EEG Dosya Yükleme
# ----------------------------
root_path = "data"
edf_files = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith(".edf"):
            edf_files.append(os.path.join(root, file))

st.write(f"Total EEG data files: {len(edf_files)}")

# ----------------------------
# 2️⃣ Main App
# ----------------------------
if st.session_state['current_user'] is not None:
    st.header(f"Welcome {st.session_state['current_user']}! 🧠")
    
    # Emotional Card placeholder
    card_placeholder = st.empty()

    # ----------------------------
    # Run EEG Analysis
    # ----------------------------
    if st.button("Run EEG Analysis"):
        if len(edf_files) == 0:
            st.warning("No EEG data found!")
        else:
            random_file = random.choice(edf_files)
            st.write(f"Randomly chosen file: {random_file}")

            raw = mne.io.read_raw_edf(random_file, preload=True)
            raw.filter(0.5,50)
            data = raw.get_data()
            channel_power = [round((d**2).mean(),2) for d in data]
            st.write("Channel-based power (first 5 channels):", channel_power[:5])

            prediction = random.choice(['stressed','tired','normal'])
            recommendations = {
                'stressed': 'Take a 5-minute break and do breathing exercises.',
                'tired': 'Consider resting or short nap.',
                'normal': 'Keep up your healthy routine!'
            }

            # Emotional Card
            colors = {'stressed':'#FF4C4C', 'tired':'#FFD700', 'normal':'#4CAF50'}
            card_placeholder.markdown(f"""
            <div style="background-color:{colors[prediction]}; 
                        color:white; 
                        padding:40px; 
                        border-radius:15px; 
                        text-align:center;
                        font-size:36px;
                        font-weight:bold;">
                {prediction.upper()}
            </div>
            """, unsafe_allow_html=True)

            st.success(f"Prediction: {prediction}")
            st.info(f"Advice: {recommendations[prediction]}")

            # Add to user history
            st.session_state['users'][st.session_state['current_user']].append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "prediction": prediction,
                "advice": recommendations[prediction]
            })

    # ----------------------------
    # 3️⃣ Guided Breathing Exercise
    # ----------------------------
    st.subheader("Guided Breathing Exercise")
    if st.button("Start Breathing Exercise"):
        st.session_state['breathing_active'] = True

    if st.session_state['breathing_active']:
        breath_placeholder = st.empty()
        phases = [("Inhale",4), ("Hold",4), ("Exhale",4)]
        for phase, seconds in phases:
            for i in range(seconds,0,-1):
                breath_placeholder.markdown(f"<h2 style='color:#4CAF50'>{phase}... {i}</h2>", unsafe_allow_html=True)
                st.sleep(1)
        breath_placeholder.markdown("<h2 style='color:#2196F3'>Breathing cycle completed! 🌬️</h2>", unsafe_allow_html=True)
        st.session_state['breathing_active'] = False  # bitince kapat

    # ----------------------------
    # 4️⃣ Personalized History
    # ----------------------------
    history_table = st.session_state['users'][st.session_state['current_user']][-10:]
    st.subheader("Last EEG Predictions (Table & Trend)")
    col1, col2 = st.columns([1,1])
    
    # Grafik küçük
    with col1:
        fig, ax = plt.subplots(figsize=(5,3))
        x = list(range(1,len(history_table)+1))
        y = [ {'stressed':2,'tired':1,'normal':0}[p['prediction']] for p in history_table ]
        ax.plot(x,y, marker='o')
        ax.set_yticks([0,1,2])
        ax.set_yticklabels(['normal','tired','stressed'])
        ax.set_xlabel("Test #")
        ax.set_ylabel("Mental State")
        ax.set_title("Trend (Last 10)")
        st.pyplot(fig)
    
    # Tablo
    with col2:
        st.table(history_table)

else:
    st.info("Please login or register to run the EEG Analyzer.")
