import streamlit as st
import pandas as pd

from binance_staking.api import get_operations_by_delegator
from binance_staking.models import OperationType

operation_colors = {
    OperationType.delegate: 'green',
    OperationType.redelegate: 'purple',
    OperationType.undelegate: 'red',
}


def operation_color(x: pd.DataFrame):
    return [f'color: {operation_colors[v]}' for v in x]


# FEATURE: currently st.dataframe doesn't support links
def tx_explorer(tx_hash: str):
    return f'<a href="https://explorer.binance.org/tx/{tx_hash}" target="_blank">{tx_hash}</a>'


def show(address: str):
    ops = get_operations_by_delegator(address)
    if ops.total:
        df = pd.DataFrame.from_records(
            [op.dict() for op in ops.operations])
        st.header('Operations')
        st.write('Last 100 operations')
        # operations can be empty
        # example: https://api.binance.org/v1/staking/chains/bsc/delegators/bnb14yc6ruhwvdv9yr0rvwqjddvkp0eupcktldpxl4/operations?offset=0&limit=100
        if len(df):
            fields = ['amount', 'operation_type', 'val_name',
                      'src_val_name', 'time', 'tx_hash']
            st.dataframe(df[fields].style.apply(operation_color,
                         axis=1, subset=['operation_type']))
