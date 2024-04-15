import streamlit as st
import requests
import time

import streamlit as st
import pandas as pd


baseurl = "https://adelekecode.dannonapi.com/"
localurl = "http://127.0.0.1:8000/"

st.set_page_config(
    page_title="BytesParser",
    page_icon="🧊",
    # layout="wide",
    initial_sidebar_state="expanded",
    
)

st.sidebar.title("BytesParser")

st.sidebar.caption("Developer")



user_email = st.sidebar.text_input("Enter your email")
get_button = st.sidebar.button("submit")

if get_button:
    if user_email == "":
        st.sidebar.write("Please enter a valid email")
    elif not "@" in user_email:
        st.sidebar.write("Please enter a valid email")

    else:
        with st.spinner("Generating unique ID"):
            time.sleep(3)
            r = requests.post(
                url= f"{localurl}v1/user/",
                headers = {
                    "Content-Type": "application/json"
                },
                json={
                    "email": user_email
                    }
            )
            if r.status_code == 200:
                st.session_state["email"] = r.json()["email"]
                st.session_state["key"] = r.json()["sk"]
            else:
                # st.write(r.json())
                st.sidebar.write("Something went wrong, please try again")

    


    



st.title("BytesParser")
gen, get = st.tabs(["Generate URL", "Get URL(s)"])

with gen:
    if "key" in st.session_state:
        st.caption(f"Session ID: {st.session_state.key}")
    else:
        st.write("No session ID")




    con1 = st.container(border=True)


    uploaded_file = con1.file_uploader("Choose a file to uplooad...")

    
    st.write("""
    """)


    button = st.button("Generate link")



    if button:
        if 'key' in st.session_state:
            if uploaded_file is not None:
                with st.spinner("generating link..."):
                    time.sleep(3)

                    r = requests.post(
                        url= f"{localurl}v1/upload/content/",

                        headers = {

                            "Authorization": f"Bearer {st.session_state.key}"
                        },

                        files = {
                            "file": (uploaded_file)
                        },

                        data = {
                            "file_type": uploaded_file.type
                        }

                    )

                    if r.status_code == 200:

                        st.write(r.json())

                        st.caption("Image uploaded successfully")
                        st.link_button("view url", f"{r.json()['url']}")


                    else:
                        st.write(r.json())
                        st.caption("Something went wrong, please try again")
            
                    
            else:
                st.caption("Please upload an image")
        else:
            st.caption("Please generate a session ID first")



with get:
    if 'email' in st.session_state:
        st.caption(f"Email: {st.session_state.email}")
    

        con2 = st.container(border=True)
        get_url_bttn = con2.button("Get URLs")
        if get_url_bttn:
            with st.spinner("Fetching URLs..."):
                time.sleep(3)
                r = requests.get(
                    url= f"{localurl}v1/images/",

                     headers = {
                         "Content-Type": "application/json"
                    },
                     
                    json={
                        "email": st.session_state.email
                    }
                )

                if r.status_code == 200:
                    st.caption("URLs fetched successfully")
                    ex_url = []
                    ex_u_id = []
                    ex_created_at = []
                    for i in r.json():
                        ex_url.append(i["url"])
                        ex_u_id.append(i["unique_id"])
                        ex_created_at.append(i["created_at"])

                    
                    df = pd.DataFrame({
                        "url": ex_url,
                        "unique_id": ex_u_id,
                        "created_at": ex_created_at
                    })

                    st.dataframe(
                        df,
                        column_config={
                            "url": st.column_config.LinkColumn("view image")
                        }
                    )
                else:
                    st.write(r.json())
                    st.caption("Something went wrong, please try again")


                        

                   

    else:
        st.caption("Please generate a session ID first")






