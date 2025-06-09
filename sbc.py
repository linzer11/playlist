import streamlit as st
import pandas as pd

# 데이터셋 로드
df = pd.read_csv('spotify_tracks.csv')

# 한국어 곡 필터링
df_korean = df[df['language'] == 'ko']

# 추천 함수 작성
def recommend_music(mood):
    # 기분에 맞는 곡 필터링
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
    
    # 인기 순으로 정렬
    recommended = recommended.sort_values(by='popularity', ascending=False)
    
    return recommended[['name', 'artist', 'popularity', 'valence', 'energy', 'tempo', 'danceability', 'year']]

# Streamlit UI 설정
st.title('기분에 맞는 한국 음악 추천')
mood = st.selectbox(
    '기분을 선택하세요:',
    ('신나는', '스트레스', '운동', '댄스', '추억', '공부')
)

st.write(f"기분: {mood}")
st.write("추천 음악을 찾고 있습니다...")

# 추천된 음악 표시
if mood:
    recommendations = recommend_music(mood)
    if len(recommendations) > 0:
        st.write(f"추천된 {mood} 기분에 맞는 음악:")
        for index, row in recommendations.iterrows():
            st.write(f"곡명: {row['name']}, 아티스트: {row['artist']}, 인기: {row['popularity']}, "
                     f"발매 연도: {row['year']}, 에너지: {row['energy']}, 발렌스: {row['valence']}")
    else:
        st.write("조건에 맞는 곡이 없습니다.")
