import streamlit as st
import pandas as pd

st.set_page_config(page_title="외국 음악 추천", layout="centered")
st.title('🎧 기분에 맞는 음악 추천')

try:
    df = pd.read_csv('spotify_tracks - spotify_tracks.csv')
    st.success("✅ 데이터 로드 완료!")

    # 'language' 컬럼이 있는지 확인
    if 'language' not in df.columns:
        st.error("❌ 'language' 컬럼이 없습니다.")
    else:
        # 외국 곡 필터링
        df_foreign = df[df['language'] != 'ko']
        if df_foreign.empty:
            st.warning("⚠️ 외국 음악 데이터가 없어 전체 데이터를 사용합니다.")
            df_foreign = df

        # 추천 함수
        def recommend_music(mood):
            if mood == '신나는':
                rec = df_foreign[(df_foreign['valence'] > 0.6) & (df_foreign['energy'] > 0.6)]
            elif mood == '스트레스':
                rec = df_foreign[(df_foreign['valence'] < 0.5) & (df_foreign['energy'] < 0.5)]
            elif mood == '운동':
                rec = df_foreign[(df_foreign['energy'] > 0.7) & (df_foreign['tempo'] > 100)]
            elif mood == '댄스':
                rec = df_foreign[(df_foreign['danceability'] > 0.6)]
            elif mood == '추억':
                rec = df_foreign[(df_foreign['popularity'] > 60) & (df_foreign['year'] < 2010)]
            elif mood == '공부':
                rec = df_foreign[(df_foreign['valence'] > 0.4) & (df_foreign['energy'] < 0.5)]
            else:
                rec = df_foreign

            return rec.sample(n=min(10, len(rec))) if not rec.empty else df_foreign.sample(n=min(5, len(df_foreign)))

        # 🌈 사용자 기분 선택
        mood = st.selectbox('지금 기분을 선택하세요:', ['신나는', '스트레스', '운동', '댄스', '추억', '공부'])

        # 🔄 추천 버튼
        if st.button("🔄 곡 추천 받기"):
            recommendations = recommend_music(mood)

            st.subheader(f"🌍 '{mood}' 기분에 어울리는 곡 추천")

            for _, row in recommendations.iterrows():
                # 링크 처리
                if 'track_url' in row and pd.notna(row['track_url']):
                    track_name = f'<a href="{row["track_url"]}" target="_blank">{row["track_name"]}</a>'
                else:
                    track_name = row['track_name']

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
    st.error("❌ 'spotify_tracks - spotify_tracks.csv' 파일을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"⚠️ 예외 발생: {e}")
