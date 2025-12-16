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



#import fungsi
from ultility import cek_login
from ultility import data_for_gemini
from ultility import show_details
from ultility import favorite_button
from ultility import show_meal
from ultility import wide_page
from ultility import analisis_gizi
from ultility import button_color
from ultility import navbar
from ultility import sidebar
wide_page()
cek_login()
navbar()
sidebar()
st.markdown("<br><br><br>", unsafe_allow_html=True)





def rekomendasi_gemini():
    st.header("Rekomendasi By Gemini ❇️")
    
    jenis_makanan= st. text_input("jenis makanan apa yang anda inginkan?",placeholder="ayam bakar bumbu hitam", width=500)
    
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    names=data_for_gemini()
    
    if st.button("Cari makanan",width=150):
            prompt = f"""
            Berdasarkan daftar resep berikut: {names}, dan jenis makanan {jenis_makanan}
            berikan 1 rekomendasi/tidak boleh lebih. resep berdasarkan daftar dan jenis makanan, 
            dan juga alasan mengapa merekomendasikan makanan tersebut!.
            apapun hasilnya tetap Kembalikan 1 strMeal, dan alasannya HANYA dalam format json seperti contoh ini:
            (resep:("strMeal":"nama_resep", "alasan":"alasan")) # tanda "("/")" adalah jurung kurawal.
            Tidak boleh ada teks penjelasan tambahan dan harus sama persis dengan format.
            """
            
            response = model.generate_content(prompt)
            data= response.text
            
            meal_match = re.search(r'"strMeal"\s*:\s*"([^"]+)"', data)
            meal = meal_match.group(1) if meal_match else None

            alasan_match = re.search(r'"alasan"\s*:\s*"([^"]+)"', data)
            alasan = alasan_match.group(1) if alasan_match else None
            
            
            api_Meal_by_name=(f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal}")
            data = requests.get(api_Meal_by_name).json()
            meal = data["meals"]
            with st.spinner("..."):
                time.sleep(3)

            st.info(alasan)
            show_meal(meal[0])
            
            meal_data=(meal[0])
            st.session_state.meal = meal_data
        


# ============================
# . Fungsi: FIlter resep dengan Ai
# ============================

def filter_by_gemini():
    st.header("Filter Resep ❇️")

    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    names=data_for_gemini()

    filters = st.multiselect("Pilih Filter", ["Vegan", "Gluten Free", "Less Sugar"],width=500)

    if st.button("Tampilkan Resep"):
        prompt = f"""
        Berdasarkan daftar resep berikut: {names}
        dan filter berikut: {filters},
        berikan 3-5 rekomendasi resep yang memenuhi kriteria di atas!.
        Kembalikan strMeal HANYA dalam format json, contoh:
        (resep:["strMeal", "strMeal", "strMeal"])
        Tidak boleh ada teks penjelasan.
        """
        
        response = model.generate_content(prompt)
        data= response.text

        match = re.search(r"```json(.*?)```", data, re.S)
        json_str = match.group(1).strip()
        data = json.loads(json_str)
        data=data["resep"]
        with st.spinner("..."):
                time.sleep(3)
            
            
        
        for meal in data:
            api_Meal_by_name=(f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal}")
            data = requests.get(api_Meal_by_name).json()
            meal = data["meals"]
            
            # st.subheader(meal[0]["strMeal"])
            # st.image(meal[0]["strMealThumb"],width=200)
            st.markdown("---")
            show_meal(meal[0])
            # meal_filter_data=(meal[0])
            # st.session_state.meal_gemini = meal_filter_data
            








cek_login()

# if "page" not in st.session_state:
#     st.session_state.page="preferences"
    
# if st.session_state.page =="preferences":
rekomendasi_gemini()
filter_by_gemini()
button_color()

if st.session_state.page =="details":
    
    show_details(st.session_state.meal)
    button_color()
    st.button("⬅️ kembali", on_click=lambda: st.session_state.update(page="preferences"))
elif st.session_state.page =="analisis":
    
    analisis_gizi(st.session_state.meal)
    button_color()
    st.button("⬅️ kembali", on_click=lambda: st.session_state.update(page="preferences"))