import streamlit as st
import pandas as pd

# 🎵 앱 제목
st.title('🎧 기분에 맞는 한국 음악 추천')

# 📂 CSV 파일 불러오기
try:
    df = pd.read_csv('spotify_tracks - spotify_tracks.csv')
    st.success("✅ 데이터 로드 완료!")

    # 🔍 컬럼 확인
    if 'language' not in df.columns:
        st.error("❌ 'language' 컬럼이 존재하지 않습니다. CSV 파일을 확인해주세요.")
    else:
        st.info(f"총 {len(df)}곡 중, 한국어 곡 개수: {len(df[df['language'] == 'ko'])}")

        # 🇰🇷 한국어 곡 필터링 (없으면 전체 데이터 사용)
        df_korean = df[df['language'] == 'ko']
        if df_korean.empty:
            st.warning("⚠️ 한국어 곡이 없어 전체 데이터를 사용합니다.")
            df_korean = df  # fallback

        # 🎯 추천 함수
        def recommend_music(mood):
            if mood == '신나는':
                recommended = df_korean[(df_korean['valence'] > 0.6) & (df_korean['energy'] > 0.6)]
            elif mood == '스트레스':
                recommended = df_korean[(df_korean['valence'] < 0.5) & (df_korean['energy'] < 0.5)]
            elif mood == '운동':
                recommended = df_korean[(df_korean['energy'] > 0.7) & (df_korean['tempo'] > 100)]
            elif mood == '댄스':
                recommended = df_korean[(df_korean['danceability'] > 0.6)]
            elif mood == '추억':
                recommended = df_korean[(df_korean['popularity'] > 60) & (df_korean['year'] < 2010)]
            elif mood == '공부':
                recommended = df_korean[(df_korean['valence'] > 0.4) & (df_korean['energy'] < 0.5)]
            else:
                recommended = df_korean

            # 조건에 맞는 곡이 너무 없으면 일부라도 보여주기
            if recommended.empty:
                return df_korean.sample(n=min(5, len(df_korean)))
            else:
                return recommended.sort_values(by='popularity', ascending=False).head(10)

        # 🌈 사용자 선택
        mood = st.selectbox('지금 기분을 선택하세요:', ['신나는', '스트레스', '운동', '댄스', '추억', '공부'])

        # 📊 결과 출력
        if mood:
            recommendations = recommend_music(mood)

            st.subheader(f"🎶 '{mood}' 기분에 어울리는 추천 곡")
            for index, row in recommendations.iterrows():
                st.markdown(f"""
                **🎵 곡명:** {row['track_name']}  
                **🎤 아티스트:** {row['artist_name']}  
                **📈 인기:** {row.get('popularity', 'N/A')}  
                **📅 연도:** {row.get('year', 'N/A')}  
                **🎚️ 에너지:** {row.get('energy', 'N/A')} | **💃 댄서빌리티:** {row.get('danceability', 'N/A')} | **🎵 발렌스:** {row.get('valence', 'N/A')}  
                ---
                """)
except FileNotFoundError:
    st.error("❌ 'spotify_tracks - spotify_tracks.csv' 파일이 존재하지 않습니다. 경로를 다시 확인해주세요.")
except Exception as e:
    st.error(f"⚠️ 예외 발생: {e}")
