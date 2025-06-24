import streamlit as st

st.write("🧪 **Path Test - If you see this, the root path works!**")
st.write("Current file: `index.py` at repo root")
st.write("This proves Streamlit Cloud can read files from the root directory.")

if st.button("Test Navigation"):
    st.write("Navigation would work from here!")