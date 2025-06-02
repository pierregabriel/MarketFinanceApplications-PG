import streamlit as st
from datetime import datetime


# Header
st.title("Pierre-Gabriel BILLAULT - Market Finance Apps")
st.subheader("Welcome to my personal portfolio")

# Introduction
st.markdown("""
This site gathers simple applications I built to **explore and better understand market finance**.

You'll find:
- A focus on **FX (Foreign Exchange)**, one of the first asset classes that caught my interest.
- Several tools around **financial options**:
    - Understanding the Greeks (sensitivities)
    - A basic option pricer
    - Visualizing classic option strategies

These projects are designed as learning tools — they are not commercial products but aim to **demonstrate concepts** and help me (and maybe you) get a clearer grasp of derivatives and trading mechanics.

Feel free to navigate through the sections!
""")

# Contact Info
st.markdown("""
---
### Contact
- 📧 Email: billaultpierregabriel@gmail.com
- 🔗 [LinkedIn](https://www.linkedin.com/in/pierre-gabriel-billault/)
""")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 10px; color: gray; font-size: 0.8em;">
    <p>© {datetime.now().year} Pierre-Gabriel BILLAULT</p>
    <p>Last updated: {datetime.now().strftime('%d/%m/%Y')}</p>
</div>
""", unsafe_allow_html=True)
