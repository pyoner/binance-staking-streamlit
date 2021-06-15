import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import altair as alt

from binance_staking.api import get_balance, get_validators

from app import sidebar, rewards, operations

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
validators = get_validators()
if validators.total:
    st.header('Validators')
    st.write('''Binance Smart Chain relies on a set of validators who are responsible
    for committing new blocks in the blockchain. These validators participate in the 
    consensus protocol by signing blocks that contain cryptographic signatures signed
    by each validator's private key. The validator set is determined by a staking 
    module built on Binance Chain for Binance Smart Chain, and propagated every 
    day UTC 00:00 from BC to BSC via Cross-Chain communication.''')

    df = pd.DataFrame.from_records([v.dict() for v in validators.validators])
    st.dataframe(df)

    st.header('APR')
    st.write(
        '''Annual Percentage Rate (APR) is the annual rate of interest paid to delegators.
        The calculation is based on the income of this validator 2 days ago.
        It is not compounded and updated every 24 hours.'''
    )
    apr_chart = alt.Chart(df).mark_bar().encode(
        x='apr',
        y='name',
    )
    st.altair_chart(apr_chart, True)
