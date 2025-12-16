import streamlit as st
import requests
import pandas as pd
import json
import string
import google.generativeai as genai
import os
import re
import time
from dotenv import load_dotenv
from ultility import wide_page
wide_page()
# ============================
# . Functions
# ============================
from ultility import show_meal
from ultility import show_details
from ultility import read_user
from ultility import save_user
from ultility import navbar
from ultility import favorite_button
from ultility import show_ingredients
from ultility import button_color
from ultility import cek_login
from ultility import analisis_gizi
from ultility import sidebar
from database_manager import DatabaseManager

db=DatabaseManager()
navbar()


    
    
# ============================
# . Fungsi: Cari Resep
# ============================

def cari_resep():
    st.header("Cari Resep 🔎")

    nama = st.text_input("Masukkan nama makanan")

    if st.button("Cari"):
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={nama}"
        response = requests.get(url).json()

        if not response["meals"]:
            st.warning("Resep tidak ditemukan.")
            return
        for meal in response["meals"]:
            show_meal(meal)
            db.add_search_history(st.session_state.username,nama,meal["idMeal"],meal["strMeal"],meal["strMealThumb"])
        


# ============================
# . Fungsi: FIlter resep dengan Ai
# ============================

# def filter_by_gemini():
    # st.header("Filter Resep ❇️")

    # load_dotenv()
    # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # model = genai.GenerativeModel("models/gemini-2.5-flash")

    # names=data_for_gemini()

    # filters = st.multiselect("Pilih Filter", ["Vegan", "Gluten Free", "Less Sugar"])

    # if st.button("Tampilkan Resep"):
    #     prompt = f"""
    #     Berdasarkan daftar resep berikut: {names}
    #     dan filter berikut: {filters},
    #     berikan 3-5 rekomendasi resep yang memenuhi kriteria di atas!.
    #     Kembalikan strMeal HANYA dalam format json, contoh:
    #     (resep:["strMeal", "strMeal", "strMeal"])
    #     Tidak boleh ada teks penjelasan.
    #     """
        
    #     response = model.generate_content(prompt)
    #     data= response.text

    #     match = re.search(r"```json(.*?)```", data, re.S)
    #     json_str = match.group(1).strip()
    #     data = json.loads(json_str)
    #     data=data["resep"]

    #     for meal in data:
    #         api_Meal_by_name=(f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal}")
    #         data = requests.get(api_Meal_by_name).json()
    #         meal = data["meals"]
            
    #         st.subheader(meal[0]["strMeal"])
    #         st.image(meal[0]["strMealThumb"],width=200)
            # favorite_button(meal[0])

# ============================
# . Fungsi: Rekomendasi Randm
# ============================

def rekomendasi_random():
    st.header("Rekomendasi")

    if "rekomendasi" not in st.session_state:
        st.session_state.rekomendasi = []
    if "rec_page" not in st.session_state:
        st.session_state.rec_page = 0

    if st.button("Refresh 🔄️"):
        st.session_state.rekomendasi = []
        for _ in range(12):
            data = requests.get("https://www.themealdb.com/api/json/v1/1/random.php").json()
            st.session_state.rekomendasi.extend(data["meals"])
        st.session_state.rec_page = 0

    if not st.session_state.rekomendasi:
        return

    per_page = 6  
    start = st.session_state.rec_page * per_page
    end = start + per_page
    page_data = st.session_state.rekomendasi[start:end]

    for row_idx in range(0, len(page_data), 2):
        cols = st.columns(2)

        for col_idx, col in enumerate(cols):
            meal_index = row_idx + col_idx

            if meal_index < len(page_data):
                with col:
                    show_meal(page_data[meal_index])
                    st.markdown("---")
    
    
    # Paging
    col1, col2 = st.columns(2)
    if col1.button("◀️Prev") and st.session_state.rec_page > 0:
        st.session_state.rec_page -= 1
        st.rerun()
    if col2.button("Next▶️") and end < len(st.session_state.rekomendasi):
        st.session_state.rec_page += 1
        st.rerun()




# ============================
# . MAIN PAGE
# ============================



cek_login()

if "page" not in st.session_state:
    st.session_state.page="home"

if st.session_state.page =="home":
    sidebar()
    st.title("Home")
    cari_resep()
    st.markdown("---")
    rekomendasi_random()
    button_color()
elif st.session_state.page =="details":
    sidebar()
    show_details(st.session_state.meal)
    button_color()
    st.button("⬅️ kembali", on_click=lambda: st.session_state.update(page="home"))
elif st.session_state.page =="analisis":
    sidebar()
    analisis_gizi(st.session_state.meal)
    button_color()
    st.button("⬅️ kembali", on_click=lambda: st.session_state.update(page="home"))