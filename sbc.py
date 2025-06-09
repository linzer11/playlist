import streamlit as st
import pandas as pd

st.set_page_config(page_title="외국 음악 추천", layout="centered")

st.title('🎧 기분에 맞는 한국 음악 추천')

try:
    df = pd.read_csv('spotify_tracks – spotify_tracks.csv')
    st.success("✅ 데이터 로드 완료!")

    if 'language' not in df.columns:
        st.error("❌ 'language' 컬럼이 없습니다.")
    else:
        df_korean = df[df['language'] == 'ko']
        if df_korean.empty:
            df_korean = df

        def recommend_music(mood):
            if mood == '신나는':
                rec = df_korean[(df_korean['valence'] > 0.6) & (df_korean['energy'] > 0.6)]
            elif mood == '스트레스':
                rec = df_korean[(df_korean['valence'] < 0.5) & (df_korean['energy'] < 0.5)]
            elif mood == '운동':
                rec = df_korean[(df_korean['energy'] > 0.7) & (df_korean['tempo'] > 100)]
            elif mood == '댄스':
                rec = df_korean[(df_korean['danceability'] > 0.6)]
            elif mood == '추억':
                rec = df_korean[(df_korean['popularity'] > 60) & (df_korean['year'] < 2010)]
            elif mood == '공부':
                rec = df_korean[(df_korean['valence'] > 0.4) & (df_korean['energy'] < 0.5)]
            else:
                rec = df_korean

            if rec.empty:
                return df_korean.sample(n=min(5, len(df_korean)))
            else:
                return rec.sample(n=min(10, len(rec)))  # 항상 무작위로

        mood = st.selectbox('지금 기분을 선택하세요:', ['신나는', '스트레스', '운동', '댄스', '추억', '공부'])

        # 새로고침 버튼
        if st.button("🔄 다른 추천 보기"):
            recommendations = recommend_music(mood)

            st.subheader(f"🎶 '{mood}' 기분에 어울리는 곡 추천")
            for _, row in recommendations.iterrows():
                # 링크 있는 경우 곡명을 클릭 가능하게 처리
                track_name = f"[{row['track_name']}]({row['track_url']})" if 'track_url' in row and pd.notna(row['track_url']) else row['track_name']

                st.markdown(f"""
                <div style="font-size: 14px; line-height: 1.5;">
                🎵 <b>곡명:</b> {track_name}<br>
                🎤 <b>아티스트:</b> {row['artist_name']}<br>
                📈 <b>인기:</b> {row.get('popularity', 'N/A')}<br>
                📅 <b>연도:</b> {row.get('year', 'N/A')}<br>
                🎚️ <b>에너지:</b> {row.get('energy', 'N/A')} |
                💃 <b>댄서빌리티:</b> {row.get('danceability', 'N/A')} |
                🎵 <b>발렌스:</b> {row.get('valence', 'N/A')}
                </div>
                <hr style="margin: 8px 0;">
                """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ 'spotify_tracks – spotify_tracks.csv' 파일을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"⚠️ 예외 발생: {e}")
