# import scipy.stats as stats
import numpy as np


def revenue_amt(params, step, prev_state, state):
    # revenue_amt = state["expected_revenue"] * stats.expon.rvs()
    timestep = state['timestep'] * 1.0
    revenue_amt = state["expected_revenue"] * (1 + np.sin(timestep * np.pi / 16))
    # print(f'{revenue_amt=}')
    # print(f'{timestep=}')
    return {'revenue_amt': revenue_amt}


def expected_revenue_change(params, step, prev_state, state):
    expected_revenue_change = state['expected_revenue']
    shock_factor = params['shock_factor']
    shock_timestep = params['shock_timestep']
    if state['timestep'] == shock_timestep:
        expected_revenue_change *= shock_factor
    return {'expected_revenue_change': expected_revenue_change}


def expected_revenue(params, step, sL, s, inputs):
    key = 'expected_revenue'
    value = inputs['expected_revenue_change']
    return key, value


def update_delegators_expected_revenue(params, step, sL, s, inputs):
    key = 'delegators'
    # (1 - smoothing_factor) * previous_avg_price + smoothing_factor * spot_price
    smoothing_factor = 0.05
    for d in s['delegators'].values():
        # uses expected revenue
        # d.expected_revenue = (1 - smoothing_factor) * d.expected_revenue + smoothing_factor * inputs['expected_revenue_change']

        # uses observed revenue (period_revenue)
        d.expected_revenue = (1 - smoothing_factor) * d.expected_revenue + smoothing_factor * s['period_revenue']

    value = s['delegators']
    return key, value


def store_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'period_revenue'
    value = inputs['revenue_amt']

    return key, value


def distribute_revenue(params, step, sL, s, inputs):
    revenue = s['period_revenue']
    owners_share = params['owners_share']
    supply = s['supply']

    # step 1: collect revenue from the state
    non_owners_share = ((1 - owners_share) * revenue)
    revenue_per_share = non_owners_share / supply

    for id, delegator in s['delegators'].items():
        if id == 0:
            # step 2: get owners share, theta
            delegator.revenue_token_holdings += owners_share * revenue

        # step 3: distribute non-owners share
        delegator.revenue_token_holdings += delegator.shares * revenue_per_share
        # print(f'{delegator.id=}: {delegator.shares=}, {revenue_per_share=}, {delegator.revenue_token_holdings=}')

    key = 'delegators'
    value = s['delegators']
    return key, value
