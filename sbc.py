import streamlit as st
import pandas as pd

st.write("🔍 CSV 컬럼 확인:", df.columns.tolist())
# 데이터셋 로드
df = pd.read_csv('spotify_tracks.csv')

