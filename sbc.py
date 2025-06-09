import streamlit as st
import pandas as pd

st.set_page_config(page_title="한국 음악 추천", layout="centered")

# 🎵 앱 제목
st.title('🎧 기분에 맞는 한국 음악 추천')

# 📂 CSV 파일 불러오기
try:
    df = pd.read_csv('spotify_tracks - spotify_tracks.csv')
    st.success("✅ 데이터 로드 완료!")

    # 컬럼 확인
    if 'language' not in df.columns:
        st.error("❌ 'language' 컬럼이 존재하지 않습니다.")
    else:
        st.caption(f"전체 곡 수: {len(df)}, 한국어 곡 수: {len(df[df['language'] == 'ko'])}")

        # 한국어 곡 필터링 (없으면 전체 사용)
        df_korean = df[df['language'] == 'ko']
        if df_korean.empty:
            st.warning("⚠️ 한국어 곡이 없어 전체 데이터를 사용합니다.")
            df_korean = df

        # 추천 함수
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

            return rec.sort_values(by='popularity', ascending=False).head(10) if not rec.empty else df_korean.sample(n=min(5, len(df_korean)))

        # 사용자 입력
        mood = st.selectbox('지금 기분을 선택하세요:', ['신나는', '스트레스', '운동', '댄스', '추억', '공부'])

        # 추천 출력
        if mood:
            st.subheader(f"🎶 '{mood}' 기분에 어울리는 곡 추천")
            recommendations = recommend_music(mood)

            for _, row in recommendations.iterrows():
                # 링크가 있으면 곡명을 클릭 가능하게
                track_display = (
                    f"[{row['track_name']}]({row['track_url']})" if 'track_url' in row and pd.notna(row['track_url'])
                    else row['track_name']
                )
                st.markdown(f"""
                <div style="font-size: 14px; line-height: 1.5;">
                🎵 <b>곡명:</b> {track_display}<br>
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
    st.error("❌ 'spotify_tracks - spotify_tracks.csv' 파일이 존재하지 않습니다.")
except Exception as e:
    st.error(f"⚠️ 예외 발생: {e}")
