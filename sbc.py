import streamlit as st
import pandas as pd

# 🎵 앱 제목
st.title('🎧 기분에 맞는 한국 음악 추천')

# 📂 CSV 파일 불러오기
try:
    df = pd.read_csv('spotify_tracks - spotify_tracks.csv')
    st.success("✅ 데이터 로드 완료!")

    # 🇰🇷 한국어 곡만 필터링
    df_korean = df[df['language'] == 'ko']

    # 🎯 추천 함수 정의
    def recommend_music(mood):
        if mood == '신나는':
            recommended = df_korean[(df_korean['valence'] > 0.7) & (df_korean['energy'] > 0.7)]
        elif mood == '스트레스':
            recommended = df_korean[(df_korean['valence'] < 0.4) & (df_korean['energy'] < 0.4) & (df_korean['tempo'] < 100)]
        elif mood == '운동':
            recommended = df_korean[df_korean['energy'] > 0.7]
        elif mood == '댄스':
            recommended = df_korean[df_korean['danceability'] > 0.7]
        elif mood == '추억':
            recommended = df_korean[(df_korean['popularity'] > 70) & (df_korean['year'] < 2000)]
        elif mood == '공부':
            recommended = df_korean[(df_korean['valence'] > 0.4) & (df_korean['energy'] < 0.4)]
        else:
            recommended = pd.DataFrame()

        # 인기순 정렬
        recommended = recommended.sort_values(by='popularity', ascending=False)

        # 필요한 컬럼만 반환
        return recommended[['track_name', 'artist_name', 'popularity', 'valence', 'energy', 'tempo', 'danceability', 'year']]

    # 🌈 사용자 입력
    mood = st.selectbox('지금 기분을 선택하세요:', ['신나는', '스트레스', '운동', '댄스', '추억', '공부'])

    # 📊 추천 곡 표시
    if mood:
        recommendations = recommend_music(mood)

        if not recommendations.empty:
            st.subheader(f"🎶 '{mood}' 기분에 맞는 추천 곡")
            for index, row in recommendations.iterrows():
                st.markdown(f"""
                **🎵 곡명:** {row['track_name']}  
                **🎤 아티스트:** {row['artist_name']}  
                **📈 인기:** {row['popularity']}  
                **📅 연도:** {row['year']}  
                **🎚️ 에너지:** {row['energy']} | **💃 댄서빌리티:** {row['danceability']} | **🎵 발렌스:** {row['valence']}  
                ---
                """)
        else:
            st.warning("😥 조건에 맞는 곡이 없습니다. 다른 기분을 선택해보세요.")
except FileNotFoundError:
    st.error("❌ 'spotify_tracks - spotify_tracks.csv' 파일이 존재하지 않습니다. 경로를 다시 확인해주세요.")
