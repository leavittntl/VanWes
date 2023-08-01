import streamlit as st
import pandas as pd
import base64

def load_data(file):
    data = pd.read_csv(file)
    return data

def main():
    st.title('Cumulative Frequencies Calculator')

    uploaded_file = st.file_uploader("Upload a CSV File", type=["csv"])
    if uploaded_file is not None:
        data = load_data(uploaded_file)

        starting_price_cf = (1 - (data['C'].value_counts().sort_index().cumsum() / data['C'].count())) * 100
        not_expensive_cf = (1 - (data['TC'].value_counts().sort_index().cumsum() / data['TC'].count())) * 100
        expensive_cf = ((data['E'].value_counts().sort_index().cumsum() / data['E'].count()) * 100).sort_values(ascending=False)
        too_expensive_cf = ((data['TE'].value_counts().sort_index().cumsum() / data['TE'].count()) * 100).sort_values(ascending=False)
      
        price_set = set(starting_price_cf.index) | set(not_expensive_cf.index) | set(expensive_cf.index) | set(too_expensive_cf.index)
        price_list = sorted(list(price_set))

        cf_data = pd.DataFrame({
            'Price': price_list,
            'Starting_Price_CF': starting_price_cf.reindex(price_list, fill_value=0),
            'Not_Expensive_CF': not_expensive_cf.reindex(price_list, fill_value=0),
            'Expensive_CF': expensive_cf.reindex(price_list, fill_value=0),
            'Too_Expensive_CF': too_expensive_cf.reindex(price_list, fill_value=0)
        }).reset_index(drop=True)

        st.write(cf_data)

        csv = cf_data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as .csv)'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()