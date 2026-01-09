import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Movie Reviews", layout="wide")

st.title("🎬 영화 & 리뷰 감성분석 서비스")

page = st.sidebar.radio("메뉴", ["영화 목록", "영화 추가", "리뷰 작성", "최근 리뷰"])

def api_get(path, params=None):
    return requests.get(f"{BACKEND_URL}{path}", params=params, timeout=10)

def api_post(path, json=None):
    return requests.post(f"{BACKEND_URL}{path}", json=json, timeout=10)

if page == "영화 목록":
    res = api_get("/movies")
    res.raise_for_status()
    movies = res.json()

    st.subheader("영화 목록")
    cols = st.columns(3)

    for i, m in enumerate(movies):
        with cols[i % 3]:
            st.markdown(f"### {m['title']}")
            if m.get("poster_url"):
                st.image(m["poster_url"], use_container_width=True)
            st.caption(f"개봉일: {m['release_date']}")
            st.caption(f"감독: {m['director']} / 장르: {m['genre']}")

            # (옵션) 평균 평점 표시
            r = api_get(f"/reviews/ratings/{m['id']}")
            if r.ok and r.json()["rating"] is not None:
                st.info(f"감성평점(평균): {r.json()['rating']:.3f} (리뷰 {r.json()['count']}개)")

elif page == "영화 추가":
    st.subheader("영화 추가")
    with st.form("add_movie"):
        title = st.text_input("제목")
        release_date = st.text_input("개봉일(YYYY-MM-DD)")
        director = st.text_input("감독")
        genre = st.text_input("장르")
        poster_url = st.text_input("포스터 URL(선택)")
        submitted = st.form_submit_button("추가")

    if submitted:
        payload = {
            "title": title,
            "release_date": release_date,
            "director": director,
            "genre": genre,
            "poster_url": poster_url or None
        }
        res = api_post("/movies", json=payload)
        if res.ok:
            st.success("영화가 등록됐어요!")
        else:
            st.error(res.text)

elif page == "리뷰 작성":
    st.subheader("리뷰 작성 (저장된 영화 선택)")
    movies = api_get("/movies").json()
    if not movies:
        st.warning("먼저 영화를 1개 이상 등록하세요.")
    else:
        movie_map = {f"{m['id']} - {m['title']}": m["id"] for m in movies}
        selected = st.selectbox("영화 선택", list(movie_map.keys()))
        movie_id = movie_map[selected]

        with st.form("add_review"):
            author = st.text_input("작성자 이름")
            content = st.text_area("리뷰 내용", height=150)
            submitted = st.form_submit_button("등록 (감성분석 자동 실행)")

        if submitted:
            payload = {"movie_id": movie_id, "author": author, "content": content}
            res = api_post("/reviews", json=payload)
            if res.ok:
                data = res.json()
                st.success("리뷰 등록 완료!")
                st.write("감성분석 결과:")
                st.metric("Label", data["sentiment_label"])
                st.metric("Score", f"{data['sentiment_score']:.4f}")
            else:
                st.error(res.text)

elif page == "최근 리뷰":
    st.subheader("최근 20개 리뷰")

    # 영화 목록을 가져와서 id -> title 매핑 만들기
    movies_res = api_get("/movies")
    movies_res.raise_for_status()
    movies = movies_res.json()

    movie_id_to_title = {m["id"]: m["title"] for m in movies}

    # 리뷰 20개 가져오기
    res = api_get("/reviews", params={"limit": 20})
    res.raise_for_status()
    reviews = res.json()

    if not reviews:
        st.info("아직 등록된 리뷰가 없어요. '리뷰 작성'에서 리뷰를 남겨보세요.")
        st.stop()

    # movie_id 대신 title 표시
    for r in reviews:
        movie_title = movie_id_to_title.get(r["movie_id"], f"(알 수 없음: ID {r['movie_id']})")
        st.markdown(f"**영화:** {movie_title}  |  **등록일:** {r['created_at']}")
        st.write(r["content"])
        st.caption(f"감성: {r['sentiment_label']} ({r['sentiment_score']:.4f})")
        st.divider()
