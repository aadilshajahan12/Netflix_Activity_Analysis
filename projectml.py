import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Arsenal Predictor", layout="wide")

if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "score_text" not in st.session_state:
    st.session_state.score_text =None
if "home_box" not in st.session_state:
    st.session_state.home_box=0

if not st.session_state.show_result:

    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://wallpaperaccess.com/full/219120.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.7);
    }
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)
    model=pickle.load(open(r'model.sav','rb'))
    scaler=pickle.load(open(r'scaler.sav','rb'))
    if 'poss' not in st.session_state:
        st.session_state.poss=1
    if 'opp_poss' not in st.session_state:
        st.session_state.opp_poss=0
    def poss_change():
        st.session_state.opp_poss=100-st.session_state.poss
    H={'Away':0,'Home':1}
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.subheader("Enter Match Statistics")
    Home = st.radio("Match Location", options=list(H.keys()), key="home",index=None)
    col1, col2 = st.columns(2)
    st.markdown(
            """
            <style>
            /* Target the text input box */
            div[data-baseweb="input"] > div {
                background-color: #ffe6e6; /* Light pink background */
                border: 2px solid #ff4d4d; /* Red border */
                border-radius: 8px;        /* Rounded corners */
            }

            /* Change text color inside the input */
            div[data-baseweb="input"] input {
                color: #000000; /* Black text */
                caret-color: #ff0000;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    with col1:
        
        


        st.markdown("### Our Team Stats")
        
        Poss = st.slider("Possession (%)", min_value=1, max_value=99, step=1, key="poss", on_change=poss_change)
        Shots = st.number_input("Shots", min_value=0, max_value=50, step=1, key="shots")
        SOT = st.number_input("Shots on Target", min_value=0, max_value=Shots, step=1, key="sot")
        Pass = st.number_input("Passes Completed", min_value=10, max_value=2000, step=1, key="pass")
        Pass_Acc = st.slider("Pass Accuracy (%)", min_value=1, max_value=99, step=1, key="pass_acc")
        Corner = st.number_input("Corners", min_value=0, max_value=40, step=1, key="cor")
        Fouls = st.number_input("Fouls", min_value=0, max_value=40, step=1, key="foul")

    with col2:
        st.markdown("### Opponent Stats")
        Opp_Poss = st.slider("Possession (%)",value=st.session_state.opp_poss,disabled=True)
        Opp_Shots = st.number_input("Shots", min_value=0, max_value=50, step=1, key="opp_shots")
        Opp_SOT = st.number_input("Shots on Target", min_value=0, max_value=Opp_Shots, step=1, key="opp_sot")
        Opp_Pass = st.number_input("Passes Completed", min_value=10, max_value=2000, step=1, key="opp_pass")
        Opp_Pass_Acc = st.slider("Pass Accuracy (%)", min_value=1, max_value=99, step=1, key="opp_pass_acc")
        Opp_Corner = st.number_input("Corners", min_value=0, max_value=40, step=1, key="opp_cor")
        Opp_Fouls = st.number_input("Fouls", min_value=0, max_value=40, step=1, key="opp_foul")
    st.sidebar.header("Instructions")
    st.sidebar.write("Fill in match stats and click 'See Score!!!' to predict.")
    
    if st.button('See Score!!!'):
        Home= H[Home]
        SE = SOT / Shots if Shots > 0 else 0
        features = [Home, Poss, Shots, SOT, Pass, Pass_Acc, Corner, Fouls,
                    Opp_Poss, Opp_Shots, Opp_SOT, Opp_Pass, Opp_Pass_Acc, Opp_Corner, Opp_Fouls, SE]
        score = model.predict(scaler.transform([features]))
        score=np.maximum(score,0)
        st.session_state.home_box=Home
        st.session_state.show_result=True
        st.session_state.score_text=score
        st.rerun()
else:
    if st.session_state.home_box==1:
        page_bg_img = """
        <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://www.arsenal.com/sites/default/files/wallpaper/wallpaper_1920x1080_light.png");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        [data-testid="stSidebar"] {
            background: rgba(255,255,255,0.7);
        }
        </style>
        """

        st.markdown(page_bg_img, unsafe_allow_html=True)
        st.title('Score at Emirates')
            
        score_html = f"""
        <div style="background-color:#1a1a1a; padding:30px; border-radius:15px; text-align:center; display:flex; justify-content:center; align-items:center; gap:40px;">
        <div style="color:#e63946; font-size:60px; font-weight:bold;">{int(st.session_state.score_text[0][0].round())}</div>
        <div style="color:white; font-size:50px; font-weight:bold;">-</div>
        <div style="color:#457b9d; font-size:60px; font-weight:bold;">{int(st.session_state.score_text[0][1].round())}</div>
        </div>
        """
        st.markdown(score_html, unsafe_allow_html=True)
        if (st.session_state.score_text[0][0].round())<(st.session_state.score_text[0][1].round()):
            st.subheader('Lose.We try Again!!',text_alignment="center",divider='red')
        elif (st.session_state.score_text[0][0].round())>(st.session_state.score_text[0][1].round()):
            st.subheader("We Win,Let's go!! COYG!!!",text_alignment='center',divider='red')
        else:
            st.subheader('Its a Draw',text_alignment='center',divider='red')
        if st.button("🔄 Back to Input"):
            st.session_state.show_result = False
            st.rerun()
    else:
        page_bg_img = """
        <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://iol-prod.appspot.com/image/776dd98ea92cdebb97d5ac3a5a5355fff569abed/4500/jpeg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        [data-testid="stSidebar"] {
            background: rgba(255,255,255,0.7);
        }
        </style>
        """

        st.markdown(page_bg_img, unsafe_allow_html=True)
        st.title('Score Away')
            
        score_html = f"""
        <div style="background-color:#1a1a1a; padding:30px; border-radius:15px; text-align:center; display:flex; justify-content:center; align-items:center; gap:40px;">
        <div style="color:#457b9d; font-size:60px; font-weight:bold;">{int(st.session_state.score_text[0][1].round())}</div>
        <div style="color:white; font-size:50px; font-weight:bold;">-</div>
        <div style="color:#e63946; font-size:60px; font-weight:bold;">{int(st.session_state.score_text[0][0].round())}</div>
        </div>
        """
        st.markdown(score_html, unsafe_allow_html=True)
        if (st.session_state.score_text[0][0].round())<(st.session_state.score_text[0][1].round()):
            st.subheader(':red[Lose.We try Again!!]',text_alignment="center")
        elif (st.session_state.score_text[0][0].round())>(st.session_state.score_text[0][1].round()):
            st.subheader(":red[We Win,Let's go!! COYG!!!]",text_alignment='center')
        else:
            st.subheader(':red[Its a Draw]',text_alignment='center')
        if st.button("🔄 Back to Input"):
            st.session_state.show_result = False
            st.rerun()
        
