import streamlit as st
import altair as alt
import pandas as pd

from binance_staking.api import get_delegator_rewards


def show(address: str):
    rewards = get_delegator_rewards(address)
    if rewards.total:
        st.header('Rewards')
        rewards_df = pd.DataFrame.from_records(
            [r.dict() for r in rewards.rewards])
        if len(rewards_df):
            ch = alt.Chart(rewards_df)
            rewards_chart = ch.mark_line(point=True).encode(
                alt.X(shorthand='time:T',
                      timeUnit='yearmonthdate', title='date'),
                alt.Y(shorthand='reward:Q'),
                alt.Color(field='val_name', type='nominal', title='Validator'),
                tooltip=[
                    alt.Tooltip(shorthand='val_name:N', title='Validator'),
                    alt.Tooltip(shorthand='reward:Q')
                ]
            )

            total_rewards_chart = ch.mark_point(color='#d00000').encode(
                alt.X(shorthand='time:T',
                      timeUnit='yearmonthdate', title='date'),
                alt.Y(shorthand='reward:Q', aggregate='sum'),
                tooltip=['sum(reward):Q']
            )

            mean_rewards_chart = ch.mark_point(color='#f48c06').encode(
                alt.X(shorthand='time:T',
                      timeUnit='yearmonthdate', title='date'),
                alt.Y(shorthand='reward:Q', aggregate='mean'),
                tooltip=['mean(reward):Q']
            )

            r_chart = rewards_chart + total_rewards_chart + mean_rewards_chart
            st.altair_chart(r_chart, True)

            col1, col2 = st.beta_columns(2)

            # last 100 rewards
            with col1:
                st.subheader('Last 100 rewards')
                st.dataframe(rewards_df[['reward', 'val_name', 'time']])

            # rewards by date
            with col2:
                st.subheader('Daily rewards')
                st.dataframe(
                    rewards_df.groupby('time').aggregate(
                        {'reward': 'sum'}
                    ).sort_index(
                        0, ascending=False))
