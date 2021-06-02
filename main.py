import streamlit as st
import streamlit.report_thread as report_thread
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

from binance_staking.api import get_balance, get_operations_by_delegator, get_validators

st.title('Binance Staking App')

address = st.text_input('Enter a wallet address')
if address:
    st.header('Address')
    st.text(address)

    st.subheader('Balance')
    balance = get_balance(address)
    st.dataframe(pd.DataFrame.from_records([balance.dict()]))

    st.header('Operations')
    st.write('Last 100 operations')
    ops = get_operations_by_delegator(address)
    ops_df = pd.DataFrame.from_records([op.dict() for op in ops.operations])
    st.dataframe(
        ops_df[['amount', 'operation_type', 'val_name', 'src_val_name', 'time', 'tx_hash']])
    # st.dataframe(ops_df)

st.header('Validators')
st.write('''Binance Smart Chain relies on a set of validators who are responsible
 for committing new blocks in the blockchain. These validators participate in the 
 consensus protocol by signing blocks that contain cryptographic signatures signed
  by each validator's private key. The validator set is determined by a staking 
  module built on Binance Chain for Binance Smart Chain, and propagated every 
  day UTC 00:00 from BC to BSC via Cross-Chain communication.''')
validators = get_validators()

df = pd.DataFrame.from_records([v.dict() for v in validators.validators])
st.dataframe(df)

st.header('APR')
st.write(
    '''Annual Percentage Rate (APR) is the annual rate of interest paid to delegators.
    The calculation is based on the income of this validator 2 days ago.
    It is not compounded and updated every 24 hours.'''
)
st.vega_lite_chart(df, {
    'mark': 'bar',

    'encoding': {
        'x': {'field': 'apr', 'type': 'quantitative'},
        'y': {'field': 'name', 'sort': '-x'}
    }},
    use_container_width=True)
