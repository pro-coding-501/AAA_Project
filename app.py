import streamlit as st

st.title("🤖 AAA: AlphA AI")
st.write("반갑습니다! AlphA Inc.의 인공지능 비서입니다.")

user_input = st.text_input("명령을 입력하세요")
if user_input:
    st.write(f"입력하신 내용: {user_input}")