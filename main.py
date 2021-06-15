import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd

from binance_staking.api import get_balance

from app import sidebar, rewards, operations, validators

st.set_page_config(page_title='Binance Staking App')

sidebar.init()

st.title('Binance Staking App')

params = st.experimental_get_query_params()
param_address = params.get('address', ['']).pop()
address = st.text_input('Enter a wallet address')

if address:
    if address != param_address:
        st.experimental_set_query_params(address=[address])
else:
    address = param_address

if address:
    st.header('Address')
    st.markdown(f'[{address}](https://explorer.binance.org/address/{address})')

    # balance
    st.subheader('Balance')
    balance = get_balance(address)
    st.dataframe(pd.DataFrame.from_records([balance.dict()]))

    # operations
    operations.show(address)

    # rewards
    rewards.show(address)


# validators
validators.show()
