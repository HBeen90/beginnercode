import streamlit as st
import pandas as pd
import numpy as np

st.title('2026년 모던 데이터 대시보')
option = st.sidebar.selectbox('데이터 종류 선', ['랜덤 데이', '주식데이터'])
data = pd.DataFrame(np.random.randn(20,3),columns=['A','B','C'])
st.line_chart(data)
st.dataframe(data, use_container_width =True)

