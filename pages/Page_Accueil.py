import streamlit as st
from datetime import datetime

# Title & subtitle
st.title("📊 Applications-PG")
st.subheader("Interactive Streamlit apps to understand market finance")

# Separator
st.markdown("---")

# About section
st.markdown("## About")
st.markdown("""
This project gathers small, focused applications built with **Streamlit**  
to **learn, explain, and visualize market finance concepts**.

The goal is to **bridge theory and practice** — turning abstract ideas into dynamic tools that make financial logic easier to see and understand.
""")

# Topics
st.markdown("## Current Topics")

st.markdown("### 🧠 Options")
st.markdown("""
- Black-Scholes option pricer (with **dynamic market data**)
- Explanation of the **Greeks** (Delta, Gamma, Vega, etc.)
- **Why Greeks matter** in hedging and strategy
- Classic **option strategies** based on market views
""")

st.markdown("### 🌍 FX (Foreign Exchange)")
st.markdown("""
- Interactive module on **FX Forwards**
- Compute and visualize the **Forward Rate Differential (FRD)**
""")

# Contact
st.markdown("---")
st.markdown("## 📬 Contact")
st.markdown("""
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
