import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import json
import string
import google.generativeai as genai
import os
import re
import time
import base64
from dotenv import load_dotenv
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle , Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
from database_manager import DatabaseManager
import requests

db=DatabaseManager()
# ============================
# . Functions
# ============================


# FUNGSI ESTETIKA🎨

def color_pallete():
    palette_main = [
        "#D987A5",   # Soft pink (seperti tombol Login)
        "#B277A8",   # Soft purple (seperti tombol SignUp)
        "#C492C1",   # Mauve pastel
        "#E0A3C2",   # Light rosy pink
        "#A66CA8"    # Deep dusty purple
        ]
    return palette_main


def button_color():
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #9973a0;
            color: white;
            border: none;
            padding: flex;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #d487a8;
            transform: scale(1.05);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            color: #9973a0;
        }
        </style>
    """, unsafe_allow_html=True)


def navbar():
    with open("logo.png", "rb") as file:
        img_base64 = base64.b64encode(file.read()).decode()

    st.markdown(f"""
    <style>
    .navbar {{
        position: relative;
        top: 0;
        width: 100%;
        left: 0;
        right: 0;
        padding: 10px;
        background-color: #9973a0;
        border-radius: 8px;
        color: white;
        font-size: 28px;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 15px;
        transition: all 0.3s ease;
    }}

    .navbar img {{
        height: 200px;
        width: 300px;
        border-radius: 20px;
    }}

    .navbar:hover {{
        background-color: #d487a8;
        color: #9973a0;
        transform: scale(1.01);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    </style>

    <div class="navbar">
        <img src="data:image/png;base64,{img_base64}" alt="Logo">
    </div>
    """, unsafe_allow_html=True)


# UTILITY 

def wide_page():
    st.set_page_config(
    page_title="My App",
    layout="wide"  
)


def read_user():
    with open("users.json", "r") as file:
        return json.load(file)


def save_user(user_data):
    with open("users.json", "w") as file:
        json.dump(user_data, file, indent=2)


def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("login.py")


def add_to_favorites(meal_data):
    users = read_user()
    username = st.session_state.username

    recipe = {
        "id": meal_data["idMeal"],
        "name": meal_data["strMeal"],
        "image": meal_data["strMealThumb"],
        "instructions": meal_data["strInstructions"],
        "category": meal_data.get("strCategory", ""),
        "area": meal_data.get("strArea", "")
    }

    favorites = users[username].get("favorites", [])
    favorite_ids = [f["id"] for f in favorites]

    if recipe["id"] not in favorite_ids:
        favorites.append(recipe)
        users[username]["favorites"] = favorites
        save_user(users)
        return True
    return False


def remove_from_favorites(recipe_id):
    users = read_user()
    username = st.session_state.username
    favorites = users[username].get("favorites", [])
    
    users[username]["favorites"] = [f for f in favorites if f["id"] != recipe_id]
    save_user(users)
    

def is_favorite(meal_id):
    users = read_user()
    username = st.session_state.username
    favorites = users[username].get("favorites", [])
    return meal_id in [f["id"] for f in favorites]


def favorite_button(data):
    if is_favorite(data["idMeal"]):
            st.write("❤️ Favorited")
    else:
            if st.button("🤍 Add", key=f"add_{data["idMeal"]}"):
                add_to_favorites(data)
                st.success("Ditambahkan ke favorit")
                st.rerun()


def show_ingredients(data):
    count1=0
    count2=0
    ingredients=[]
    for bahan in data:
        if "strIngredient" in bahan:
            if data[bahan]==""or data[bahan]==" ":
                break
            count1+=1 
            ingredients.append(data[bahan])
            # st.text(f"{count}. {data[bahan]}")
    for measure in data:
        if "strMeasure" in measure:
            if data[measure]==""or data[measure]==" ":
                break
            count2+=1 
            st.text(f"{count2}.  {data[measure]}  {ingredients[count2-1]}")


def show_meal(data):
        
        col1, col2, col3= st.columns([1,2,1])
        with col2:
            # st.header(data["strMeal"])
            st.image(data["strMealThumb"],width=500)
            st.write(f"**{data["strMeal"]}**")
            st.caption(f"**Category :** {data["strCategory"]}")
            st.caption(f"**Country :** {data["strArea"]}")
            favorite_button(data)

            st.button(
                "🔎detail", 
                key=f"detail_{data["idMeal"]}", 
                on_click=lambda m=data: (
                    st.session_state.update(meal=m, page = "details")
                    )
                )


def show_details(data):
    db.add_detail_history(st.session_state.username,data["idMeal"],data["strMeal"],data["strMealThumb"],data)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title(data["strMeal"])
    db.add_video_history(st.session_state.username,data["idMeal"],data["strMeal"],data["strYoutube"])
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.video(data["strYoutube"])
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    col1,col2,col3= st.columns([1,1.5,1])
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image(data["strMealThumb"],width=450)
    with col2:
        st.subheader("Cara Memasak!")
        st.write(data["strInstructions"])
        st.markdown("<br><br>", unsafe_allow_html=True)
    with col3:
        st.subheader("Bahan yang dibutuhkan!")
        show_ingredients(data)
        st.markdown("<br><br>", unsafe_allow_html=True)  
    st.markdown("---")
    export_recipe_to_pdf(data)
    st.button("📊Analisis", on_click=lambda: st.session_state.update(page="analisis"))
        

    
def data_for_gemini():
    if "allMeals" not in st.session_state:
        all_api = [f"https://www.themealdb.com/api/json/v1/1/search.php?f={i}" for i in string.ascii_lowercase]
        names = []
        for link in all_api:
            data = requests.get(link).json()
            meals = data.get("meals") or []
            for meal in meals:
                names.append(meal["strMeal"])
        st.session_state.allMeals=names
    names=st.session_state.allMeals    
    return names
    

def cek_login():
    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu")
        st.stop()


def analisis_gizi(data):
    
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    makanan=data["strMeal"]
    
    
    prompt = f"""
    Berdasarkan daftar resep berikut: {makanan}, berikan analisis nilai_gizi yang terkandung di dalam makanan tersebut,
    dengan output berupa angka kandungan gizi karbohidrat gula dan protein, serta maksimal dan minimal 5 kandungan lain.
    Dan juga peringatan untuk makanan tersebut berdasarkan nilai gizi yang dikandungnya.
    apapun hasilnya tetap Kembalikan dalam format seperti di bawah, hasilnya format json seperti contoh ini:
    (analisis:("peringatan":"peringatan", nilai_gizi: ("karbohidrat":"123", "gula": "123", "protein":"123","kandungan":"123", "kandungan": "123", "kandungan":"123", "kandungan": "123", "kandungan":"123"))) # tanda "("/")" adalah jurung kurawal.
    Output seperti format di atas, key dan value dalam format hanya contoh. Tulis kandungan(key) dan nilainya(value),value hanya berupa angka tidak boleh ada tambahan selain angka. Tidak boleh ada teks penjelasan tambahan dan harus sama persis dengan format.
    """
    
    response = model.generate_content(prompt)
    data1= response.text
    clean_str = data1.replace("```json", "").replace("```", "")
    data_json = json.loads(clean_str)
    
    #st.text(data_json["analisis"]["nilai_gizi"])
    nilai_gizi=data_json["analisis"]["nilai_gizi"]
    gizi=list(nilai_gizi.items())
    gizi_label = list(nilai_gizi.keys())
    gizi_value = list(nilai_gizi.values())
    df =pd.DataFrame(gizi, columns=["Nutrisi", "Jumlah(gr)"])
    df_pie=pd.DataFrame((gizi[:3]), columns=["Nutrisi", "Jumlah"])

    fig_pie = px.pie(
        df_pie,
        names="Nutrisi",
        values="Jumlah",
        title="Nilai Gizi",
        hole=0.3,
        color_discrete_sequence=color_pallete()
    )

    fig = px.bar(
        x= gizi_label,
        y=gizi_value,
        labels={"x":"Nutrisi", "y": "Jumlah(gr)"},
        color_discrete_sequence=color_pallete()
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.title(f"Analisis Gizi {data["strMeal"]}")
    st.markdown("<br>", unsafe_allow_html=True)
    st.warning(data_json["analisis"]["peringatan"])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image(data["strMealThumb"],width=550)
    with col2:
        st.plotly_chart(fig_pie)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Grafik Nilai Gizi")
    st.plotly_chart(fig)
    st.markdown("---")
    st.subheader("Table Nilai Gizi")
    st.dataframe(df, hide_index=True)
    db.add_analysis_history(st.session_state.username,data["idMeal"],data["strMeal"],data["strMealThumb"],nilai_gizi)
    export_dataframe_to_pdf(data, df, filename=f"{data["strMeal"]}_nutrition_analysis.pdf", title=f"Analisis Gizi {data["strMeal"]}")


def export_dataframe_to_pdf(data, df, filename="recipe_data.pdf", title="Recipe Data" ):
    
    """
    Export DataFrame ke PDF
    
    Args:
        df: pandas DataFrame yang akan di-export
        filename: Nama file PDF
        title: Judul di PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Judul
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 20))
    
    # Convert DataFrame ke list
    data = [df.columns.tolist()] + df.values.tolist()
    
    # Buat tabel
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9973a0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    # Tombol download
    if st.download_button(
        label="📥 Export to PDF",
        data=buffer,
        file_name=filename,
        mime="application/pdf"
    ):
        db.add_download_history(st.session_state.username,data["idMeal"],data["strMeal"],f"Resep {data['strMeal']}")
    

def export_recipe_to_pdf(meal_data):
    
    """
    Export resep ke PDF lengkap dengan foto
    
    Args:
        meal_data: Dictionary data resep dari API
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Judul resep
    story.append(Paragraph(meal_data["strMeal"], styles['Title']))
    story.append(Spacer(1, 12))
    
    # Foto resep
    try:
        img_response = requests.get(meal_data["strMealThumb"])
        img = Image(BytesIO(img_response.content), width=4*inch, height=4*inch)
        story.append(img)
        story.append(Spacer(1, 12))
    except:
        pass
    
    # Informasi resep
    story.append(Paragraph(f"<b>Category:</b> {meal_data.get('strCategory', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>Area:</b> {meal_data.get('strArea', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Bahan-bahan
    story.append(Paragraph("<b>Ingredients:</b>", styles['Heading2']))
    for i in range(1, 21):
        ingredient = meal_data.get(f"strIngredient{i}", "")
        measure = meal_data.get(f"strMeasure{i}", "")
        if ingredient and ingredient.strip():
            story.append(Paragraph(f"• {measure} {ingredient}", styles['Normal']))
    
    story.append(Spacer(1, 12))
    
    # Cara memasak
    story.append(Paragraph("<b>Instructions:</b>", styles['Heading2']))
    instructions = meal_data.get("strInstructions", "").replace('\n', '<br/>')
    story.append(Paragraph(instructions, styles['Normal']))
    
    # Link YouTube
    if meal_data.get("strYoutube"):
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"<b>Video:</b> {meal_data['strYoutube']}", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    # Tombol download
    if st.download_button(
        label="📥 Download PDF",
        data=buffer,
        file_name=f"{meal_data['strMeal']}.pdf",
        mime="application/pdf",
        key=f"pdf_{meal_data['idMeal']}"
    ):
        db.add_download_history(st.session_state.username,meal_data["idMeal"],meal_data["strMeal"],f"Resep {meal_data['strMeal']}") 
    

def upload_foto_profil():
    USER_JSON = "users.json"

    
    
    uploaded = st.file_uploader("Tambahkan Foto Profil Anda", type=["jpg", "jpeg", "png"], width=300)

    if uploaded:
        
        file_bytes = uploaded.getvalue()
        b64 = base64.b64encode(file_bytes).decode("utf-8")
        
        
        mime = uploaded.type  
        data_uri = f"data:{mime};base64,{b64}"

        
        users = read_user()

        username = st.session_state.username  

        
        users[username]["profile_pic"] = data_uri
        save_user(users)

        st.success("Foto profil berhasil perbarui")
        

def show_profile_pic():
    USER_JSON = "users.json"

    def load_users():
        with open(USER_JSON, "r") as f:
            return json.load(f)


    users = read_user()
    username = st.session_state.username

    profile = users.get(username, {})

    # Tampilkan foto jika ada
    if "profile_pic" in profile:
        st.title(st.session_state.username)
        st.image(profile["profile_pic"], width=200)
        
    
def sidebar():
    with st.sidebar:
        show_profile_pic()
        st.markdown("""
        <style>
        /* Hide default multipage navigation */
        section[data-testid="stSidebar"] .css-1oe6wy4, 
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        if st.button("🏚️ Home",width=150):
            st.switch_page("pages/home.py")
        if st.button("❇️ Preferences",width=150):
            st.switch_page("pages/preferences.py")
        if st.button("👤 Profile",width=150):
            st.switch_page("pages/profile.py")
        if st.button("⌛History",width=150):
            st.switch_page("pages/history.py")
        show_rekomendasi_harian_sidebar()
        st.markdown("<br>", unsafe_allow_html=True)
        logout()


def rekomendasi_harian_gemini():
    
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    names=data_for_gemini()
    
    
    prompt = f"""
    Berdasarkan daftar resep berikut: {names}, 
    berikan 3 rekomendasi/tidak boleh lebih, resep makanan untuk sarapan, makan siang dan makan malam masing masing 1 resep, 
    dan juga alasan mengapa merekomendasikan makanan tersebut!,berikan alasan ke pada masing masing resep.
    kembalikan dalam format json seperti contoh berikut:
    (resep:[("sarapan":"nama_resep", "alasan":"alasan"),("makan_siang":"nama_resep", "alasan":alasan"),("makan_malam":"nama_resep", "alasan":alasan")) # tanda "("dan")" adalah jurung kurawal.
    Tidak boleh ada teks penjelasan tambahan dan harus sama persis dengan format.
    """
    
    response = model.generate_content(prompt)
    data= response.text

    match = re.search(r"```json(.*?)```", data, re.S)
    json_str = match.group(1).strip()
    data = json.loads(json_str)
    data=data["resep"]
    
    # data_rekomendasi=[]
    # kategori=["sarapan","makan_siang","makan_malam"]
    # count=0
    # for resep in data:
    #     meal= resep[kategori[count]]
    #     alasan= resep["alasan"]
    #     api_Meal_by_name=(f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal}")
    #     data = requests.get(api_Meal_by_name).json()
    #     meal = data["meals"]
    #     with st.spinner("..."):
    #         time.sleep(3)
    #     # st.info(alasan)
    #     # show_meal(meal[0])
    #     data_rekomendasi.append(meal[0])
    #     count+=1


    users =read_user()
    username=st.session_state.username
    users[username]["rekomendasi_harian"] = data
    save_user(users)


def show_rekomendasi_harian():
    users = read_user()
    username = st.session_state.username

    profile = users.get(username, {})

    if "rekomendasi_harian" in profile:
        # for resep in users[username]["rekomendasi_harian"]:
        #     show_meal(resep)
        alasan_lst=[]
        data_rekomendasi=[]
        kategori=["sarapan","makan_siang","makan_malam"]
        count=0
        for resep in users[username]["rekomendasi_harian"]:
            meal= resep[kategori[count]]
            alasan= resep["alasan"]
            api_Meal_by_name=(f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal}")
            data = requests.get(api_Meal_by_name).json()
            meal = data["meals"]
            with st.spinner("..."):
                time.sleep(3)
            #st.info(alasan)
            #show_meal(meal[0])
            alasan_lst.append(alasan)
            data_rekomendasi.append(meal[0])
            count+=1

        for idx in range(0, len(data_rekomendasi), 3):
            cols = st.columns(3)
        
        for col_idx, col in enumerate(cols):
            if idx + col_idx <=3:
                recipe = data_rekomendasi[idx + col_idx]

            with col:
                st.markdown("---")
                st.subheader(kategori[idx + col_idx])
                st.info(alasan_lst[idx + col_idx])
                st.image(recipe["strMealThumb"],width=200)
                st.text(recipe["strMeal"])
                with st.expander("Cara Memasak"):
                    st.text(recipe["strInstructions"])
    if st.button("refresh"):
        rekomendasi_harian_gemini()
        st.rerun()


def show_rekomendasi_harian_sidebar():
    jam = datetime.now().hour
    users = read_user()
    username = st.session_state.username
    profile = users.get(username, {})
    if "rekomendasi_harian" in profile:
        kategori=["sarapan","makan_siang","makan_malam"]
        meals=users[username]["rekomendasi_harian"]
        if "rekomendasi_harian" in profile:
            if jam > 0 and jam <= 9 :
                kat=0
            elif jam >9 and jam <= 15:
                kat=1 
            else:
                kat=2

        alasan=meals[kat]["alasan"]   
        api_Meal_by_name=(f"https://www.themealdb.com/api/json/v1/1/search.php?s={meals[kat][kategori[kat]]}")
        data = requests.get(api_Meal_by_name).json()
        meal = data["meals"][0]
        with st.expander(kategori[kat],width=200):
            st.info(alasan) 
        st.image(meal["strMealThumb"],caption=meal["strMeal"],width=150)
    



