import streamlit as st
from get_papers_list.fetcher import search_pubmed, fetch_paper_details, parse_xml
import pandas as pd

st.set_page_config(page_title="PubMed Paper Finder", layout="centered")
st.title("🔬 PubMed Paper Finder (LLM-style Interface)")
st.markdown("Search PubMed for papers with **non-academic authors** (Pharma or Biotech companies).")

query = st.text_input("🔍 Enter your PubMed search query", "")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        with st.spinner("Searching..."):
            try:
                ids = search_pubmed(query)
                xml_data = fetch_paper_details(ids)
                df = parse_xml(xml_data)

                if df.empty:
                    st.info("No papers found with non-academic authors.")
                else:
                    st.success(f"Found {len(df)} relevant papers!")

                    st.dataframe(df)

                    csv_filename = f"{query.replace(' ', '_')}_results.csv"
                    df.to_csv(csv_filename, index=False)
                    st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name=csv_filename)

            except Exception as e:
                st.error(f"❌ Error: {e}")
