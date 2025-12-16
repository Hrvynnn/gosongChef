import streamlit as st
import json
from datetime import datetime
from database_manager import DatabaseManager
from ultility import wide_page
from ultility import navbar
from ultility import button_color
from ultility import cek_login
from ultility import sidebar
from ultility import button_color
cek_login()
sidebar()
wide_page()
navbar()

button_color()

st.title("History Management")
st.markdown("<br>", unsafe_allow_html=True)

db = DatabaseManager()
username = st.session_state.username

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Search History", 
    "Detail Views", 
    "Analysis History", 
    "Download History", 
    "Video History",
    "All History"
])

# TAB 1: SEARCH HISTORY
with tab1:
    st.subheader("Search History")
    
    search_history = db.get_search_history(username)
    
    if len(search_history) == 0:
        st.info("Belum ada history pencarian")
    else:
        st.write(f"Total pencarian: {len(search_history)}")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Clear All Search", type="secondary"):
                db.clear_search_history(username)
                st.success("Search history cleared")
                st.rerun()
        
        st.markdown("---")
        
        for history in search_history:
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                st.write(f"{history['search_query']}")
                st.caption(history['timestamp'])
            
            with col2:
                if history['meal_name']:
                    st.write(f"Result: {history['meal_name']}")
                else:
                    st.write("No result found")
            
            with col3:
                if st.button("Delete", key=f"del_search_{history['id']}"):
                    db.delete_search_history(history['id'])
                    st.rerun()
            
            st.markdown("---")

# TAB 2: DETAIL HISTORY
with tab2:
    st.subheader("Detail View History")
    
    detail_history = db.get_detail_history(username)
    
    if len(detail_history) == 0:
        st.info("Belum ada history detail view")
    else:
        st.write(f"Total views: {len(detail_history)}")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Clear All Details", type="secondary"):
                db.clear_detail_history(username)
                st.success("Detail history cleared")
                st.rerun()
        
        st.markdown("---")
        
        for idx in range(0, len(detail_history), 3):
            cols = st.columns(3)
            
            for col_idx, col in enumerate(cols):
                if idx + col_idx < len(detail_history):
                    history = detail_history[idx + col_idx]
                    
                    with col:
                        if history['meal_thumb']:
                            st.image(history['meal_thumb'], use_container_width=True)
                        
                        st.write(f"**{history['meal_name']}**")
                        st.caption(history['timestamp'])
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("View Again", key=f"view_{history['id']}"):
                                meal_data = json.loads(history['meal_data'])
                                st.session_state.meal = meal_data
                                st.session_state.page = "details"
                                st.switch_page("pages/home.py")
                        
                        with col_b:
                            if st.button("Delete", key=f"del_detail_{history['id']}"):
                                db.delete_detail_history(history['id'])
                                st.rerun()
                        
                        st.markdown("---")

# TAB 3: ANALYSIS HISTORY
with tab3:
    st.subheader("Analysis History")
    
    analysis_history = db.get_analysis_history(username)
    
    if len(analysis_history) == 0:
        st.info("Belum ada history analisis")
    else:
        st.write(f"Total analysis: {len(analysis_history)}")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Clear All Analysis", type="secondary"):
                db.clear_analysis_history(username)
                st.success("Analysis history cleared")
                st.rerun()
        
        st.markdown("---")
        
        for idx in range(0, len(analysis_history), 3):
            cols = st.columns(3)
            
            for col_idx, col in enumerate(cols):
                if idx + col_idx < len(analysis_history):
                    history = analysis_history[idx + col_idx]
                    
                    with col:
                        if history['meal_thumb']:
                            st.image(history['meal_thumb'], use_container_width=True)
                        
                        st.write(f"**{history['meal_name']}**")
                        st.caption(history['timestamp'])
                        
                        with st.expander("View Analysis Data"):
                            analysis_data = json.loads(history['analysis_data'])
                            st.json(analysis_data)
                        
                        if st.button("Delete", key=f"del_analysis_{history['id']}"):
                            db.delete_analysis_history(history['id'])
                            st.rerun()
                        
                        st.markdown("---")

# TAB 4: DOWNLOAD HISTORY
with tab4:
    st.subheader("Download History")
    
    download_history = db.get_download_history(username)
    
    if len(download_history) == 0:
        st.info("Belum ada history download")
    else:
        st.write(f"Total downloads: {len(download_history)}")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Clear All Downloads", type="secondary"):
                db.clear_download_history(username)
                st.success("Download history cleared")
                st.rerun()
        
        st.markdown("---")
        
        for history in download_history:
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**{history['meal_name']}**")
            
            with col2:
                st.write(f"Type: {history['download_type']}")
                st.caption(history['timestamp'])
            
            with col3:
                if st.button("Delete", key=f"del_download_{history['id']}"):
                    db.delete_download_history(history['id'])
                    st.rerun()
            
            st.markdown("---")

# TAB 5: VIDEO HISTORY
with tab5:
    st.subheader("Video Watch History")
    
    video_history = db.get_video_history(username)
    
    if len(video_history) == 0:
        st.info("Belum ada history video")
    else:
        st.write(f"Total videos watched: {len(video_history)}")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Clear All Videos", type="secondary"):
                db.clear_video_history(username)
                st.success("Video history cleared")
                st.rerun()
        
        st.markdown("---")
        
        for history in video_history:
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**{history['meal_name']}**")
            
            with col2:
                if history['video_url']:
                    st.link_button("Watch Again", history['video_url'])
                st.caption(history['timestamp'])
            
            with col3:
                if st.button("Delete", key=f"del_video_{history['id']}"):
                    db.delete_video_history(history['id'])
                    st.rerun()
            
            st.markdown("---")

# TAB 6: ALL HISTORY
with tab6:
    st.subheader("All History Summary")
    
    counts = db.get_all_history_count(username)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Searches", counts['search_history'])
    
    with col2:
        st.metric("Details", counts['detail_history'])
    
    with col3:
        st.metric("Analysis", counts['analysis_history'])
    
    with col4:
        st.metric("Downloads", counts['download_history'])
    
    with col5:
        st.metric("Videos", counts['video_history'])
    
    st.markdown("---")
    
    st.subheader("Clear All History")
    st.warning("This action will delete ALL your history data permanently")
    
    confirm = st.checkbox("I understand this action cannot be undone")
    
    if confirm:
        if st.button("Delete All History", type="primary"):
            db.clear_all_history(username)
            st.success("All history deleted successfully")
            st.rerun()

button_color()