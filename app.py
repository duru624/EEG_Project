import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import mediapipe as mp

st.set_page_config(page_title="EEG Mental State App", layout="wide")

# -------------------------
# SESSION STATE
# -------------------------

if "users" not in st.session_state:
    st.session_state.users = {}

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# -------------------------
# SIDEBAR LOGIN
# -------------------------

st.sidebar.title("Account")

username = st.sidebar.text_input("Username")

col1, col2 = st.sidebar.columns(2)

login = col1.button("Login")
register = col2.button("Register")

if login:
    if username in st.session_state.users:
        st.session_state.current_user = username
        st.sidebar.success("Logged in")
    else:
        st.sidebar.error("User not found")

if register:
    if username not in st.session_state.users and username != "":
        st.session_state.users[username] = []
        st.session_state.current_user = username
        st.sidebar.success("User created")
    else:
        st.sidebar.error("Username invalid")

if st.session_state.current_user:

    if st.sidebar.button("Logout"):
        st.session_state.current_user = None
        st.sidebar.success("Logged out")


# -------------------------
# LOGIN CHECK
# -------------------------

if st.session_state.current_user is None:

    st.title("EEG Mental State Analyzer")
    st.info("Please login or register from the sidebar")

    st.stop()


# -------------------------
# MAIN PAGE
# -------------------------

st.title("EEG Mental State Analyzer")

st.write("Logged in as:", st.session_state.current_user)


# -------------------------
# TABS
# -------------------------

tab1, tab2 = st.tabs(["EEG Analysis", "Camera Detection"])


# ==================================================
# EEG TAB
# ==================================================

with tab1:

    st.header("EEG Analysis Simulation")

    if st.button("Run EEG Analysis"):

        prediction = random.choice(["normal", "tired", "stressed"])

        advice = {
            "normal": "Keep your healthy routine.",
            "tired": "You may need rest or sleep.",
            "stressed": "Take a short break and relax."
        }

        colors = {
            "normal": "#4CAF50",
            "tired": "#FFD700",
            "stressed": "#FF4C4C"
        }

        st.markdown(
            f"""
            <div style="background-color:{colors[prediction]};
                        color:white;
                        padding:40px;
                        border-radius:15px;
                        text-align:center;
                        font-size:40px;
                        font-weight:bold;">
                {prediction.upper()}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(advice[prediction])

        st.session_state.users[st.session_state.current_user].append(
            {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "state": prediction,
                "advice": advice[prediction]
            }
        )


    history = st.session_state.users[st.session_state.current_user]

    if len(history) > 0:

        st.subheader("History")

        states = {"normal":0,"tired":1,"stressed":2}

        y = [states[h["state"]] for h in history]

        x = list(range(1,len(history)+1))

        fig, ax = plt.subplots()

        ax.plot(x,y,marker="o")

        ax.set_yticks([0,1,2])
        ax.set_yticklabels(["normal","tired","stressed"])

        ax.set_xlabel("Test")

        ax.set_ylabel("Mental State")

        st.pyplot(fig)

        st.table(history)



# ==================================================
# CAMERA TAB
# ==================================================

with tab2:

    st.header("Mental State Detection With Camera")

    img = st.camera_input("Take a photo")

    if img is not None:

        image = Image.open(img)

        frame = np.array(image)

        mp_face = mp.solutions.face_mesh

        face_mesh = mp_face.FaceMesh()
        frame_rgb = frame
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:

            landmarks = results.multi_face_landmarks[0].landmark

            eye_ratio = abs(landmarks[159].y - landmarks[145].y)

            mouth_ratio = abs(landmarks[13].y - landmarks[14].y)

            st.write("Eye openness:", round(eye_ratio,4))
            st.write("Mouth tension:", round(mouth_ratio,4))

            if eye_ratio < 0.015:
                prediction = "tired"
            elif mouth_ratio > 0.03:
                prediction = "stressed"
            else:
                prediction = "normal"

            colors = {
                "normal": "#4CAF50",
                "tired": "#FFD700",
                "stressed": "#FF4C4C"
            }

            st.markdown(
                f"""
                <div style="background-color:{colors[prediction]};
                            color:white;
                            padding:40px;
                            border-radius:15px;
                            text-align:center;
                            font-size:40px;
                            font-weight:bold;">
                    {prediction.upper()}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.warning("Face not detected. Try again.")
