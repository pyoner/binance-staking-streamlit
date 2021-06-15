import streamlit as st
import pandas as pd

from binance_staking.api import get_operations_by_delegator


def show(address: str):
    ops = get_operations_by_delegator(address)
    if ops.total:
        ops_df = pd.DataFrame.from_records(
            [op.dict() for op in ops.operations])
        st.header('Operations')
        st.write('Last 100 operations')
        # operations can be empty
        # example: https://api.binance.org/v1/staking/chains/bsc/delegators/bnb14yc6ruhwvdv9yr0rvwqjddvkp0eupcktldpxl4/operations?offset=0&limit=100
        if len(ops_df):
            st.dataframe(
                ops_df[['amount', 'operation_type', 'val_name', 'src_val_name', 'time', 'tx_hash']])
