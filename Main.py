import streamlit as st
import pandas as pd
from io import BytesIO

def load_data(file):
    data = pd.read_csv(file)
    return data

def save_to_csv(data):
    bytes = BytesIO()
    data.to_csv(bytes, index=False)
    bytes.seek(0)
    return bytes

def main():
    st.title('Cumulative Frequencies Calculator')

    uploaded_file = st.file_uploader("Upload a CSV File", type=["csv"])
    if uploaded_file is not None:
        data = load_data(uploaded_file)

        cheap_cf = (1 - (data['C'].value_counts().sort_index().cumsum() / data['C'].count())) * 100
        too_cheap_cf = (1 - (data['TC'].value_counts().sort_index().cumsum() / data['TC'].count())) * 100
        expensive_cf = ((data['E'].value_counts().sort_index().cumsum() / data['E'].count()) * 100).sort_values(ascending=False)
        too_expensive_cf = ((data['TE'].value_counts().sort_index().cumsum() / data['TE'].count()) * 100).sort_values(ascending=False)
      
        price_set = set(cheap_cf.index) | set(too_cheap_cf.index) | set(expensive_cf.index) | set(too_expensive_cf.index)
        price_list = sorted(list(price_set))

        cf_data = pd.DataFrame({
            'Price': price_list,
            'cheap_cf': cheap_cf.reindex(price_list).bfill(),
            'too_cheap_cf': too_cheap_cf.reindex(price_list).bfill(),
            'Expensive_CF': expensive_cf.reindex(price_list).bfill(),
            'Too_Expensive_CF': too_expensive_cf.reindex(price_list).bfill()
        }).reset_index(drop=True)

        st.write(cf_data)
           
        bytes = save_to_csv(cf_data)
        st.download_button(
            label="Download CSV File",
            data=bytes,
            file_name='cumulative_frequencies.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()