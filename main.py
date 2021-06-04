from altair.vegalite.v4.schema.channels import StrokeDash
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import altair as alt

from binance_staking.api import get_balance, get_delegator_rewards, get_operations_by_delegator, get_validators

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
    st.text(address)

    # balance
    st.subheader('Balance')
    balance = get_balance(address)
    st.dataframe(pd.DataFrame.from_records([balance.dict()]))

    # operations
    st.header('Operations')
    st.write('Last 100 operations')
    ops = get_operations_by_delegator(address)
    ops_df = pd.DataFrame.from_records([op.dict() for op in ops.operations])
    # operations can be empty
    # example: https://api.binance.org/v1/staking/chains/bsc/delegators/bnb14yc6ruhwvdv9yr0rvwqjddvkp0eupcktldpxl4/operations?offset=0&limit=100
    if len(ops_df):
        st.dataframe(
            ops_df[['amount', 'operation_type', 'val_name', 'src_val_name', 'time', 'tx_hash']])

    # rewards
    st.header('Rewards')
    rewards = get_delegator_rewards(address)
    rewards_df = pd.DataFrame.from_records(
        [r.dict() for r in rewards.rewards])
    if len(rewards_df):
        ch = alt.Chart(rewards_df)
        rewards_chart = ch.mark_line().encode(
            alt.X(shorthand='time:T',
                  timeUnit='yearmonthdate', title='date'),
            alt.Y(shorthand='reward:Q'),
            alt.Color(field='val_name', type='nominal', title='Validator')
        )

        total_rewards_chart = ch.mark_line().encode(
            alt.X(shorthand='time:T',
                  timeUnit='yearmonthdate', title='date'),
            alt.Y(shorthand='reward:Q', aggregate='sum'),
            alt.StrokeDash(shorthand='reward:Q', aggregate='sum', legend=None)
        )

        st.altair_chart(rewards_chart + total_rewards_chart, True)

        st.write('Last 100 rewards')
        st.dataframe(rewards_df[['reward', 'val_name', 'time']])


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
apr_chart = alt.Chart(df).mark_bar().encode(
    x='apr',
    y='name',
)
st.altair_chart(apr_chart, True)
