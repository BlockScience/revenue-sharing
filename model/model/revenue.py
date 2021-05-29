def revenue_amt(params, step, prev_state, state):
    timestep = state['timestep']
    # print(f'{timestep=}')

    # NOTE: Uncomment this if we want stochastic revenue streams.
    # revenue_amt = state["expected_revenue"] * stats.expon.rvs()

    if state['decoupling_risk_threshold_met']:
        revenue_amt = 0
    else:
        revenue_amt = params['gain'][timestep] * state["expected_revenue"]
    # print(f'{revenue_amt=}')

    return {'revenue_amt': revenue_amt}


def update_delegators_expected_revenue(params, step, sL, s, inputs):
    key = 'delegators'
    for d in s['delegators'].values():
        # uses expected revenue
        # d.expected_revenue = (1 - smoothing_factor) * d.expected_revenue + smoothing_factor * inputs['expected_revenue_change']

        # uses observed revenue (period_revenue)
        d.expected_revenue = (1 - d.smoothing_factor) * d.expected_revenue + d.smoothing_factor * s['period_revenue']

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
