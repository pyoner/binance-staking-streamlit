import streamlit as st
import pandas as pd
import altair as alt

from binance_staking.api import get_validators


def show():
    validators = get_validators()
    if validators.total:
        st.header('Validators')
        st.write('''Binance Smart Chain relies on a set of validators who are responsible
        for committing new blocks in the blockchain. These validators participate in the 
        consensus protocol by signing blocks that contain cryptographic signatures signed
        by each validator's private key. The validator set is determined by a staking 
        module built on Binance Chain for Binance Smart Chain, and propagated every 
        day UTC 00:00 from BC to BSC via Cross-Chain communication.''')

        df = pd.DataFrame.from_records(
            [v.dict() for v in validators.validators])
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
