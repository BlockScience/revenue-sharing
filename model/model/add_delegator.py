from . import delegator
import random
import scipy.stats as stats


# policy
def should_instantiate_delegate(params, step, sL, s):
    # flip a coin (1 joins if there's room and random says to)
    should_instantiate_delegate = False

    rng = random.random()
    if rng >= params['arrival_rate']:
        should_instantiate_delegate = True

    return {"should_instantiate_delegate": should_instantiate_delegate}


# mechanism
def instantiate_delegate(params, step, sL, s, inputs):
    if inputs['should_instantiate_delegate']:
        spot_price = s['spot_price']

        # add new members
        shares = 0
        reserve_token_holdings = params['expected_reserve_token_holdings'] * stats.expon.rvs()
        system_expected_revenue = params['expected_revenue']

        # epsion is the noise in the delegator's estimate of the expectation
        epsilon = stats.norm.rvs() * params['delegator_estimation_noise_variance'] + \
            params['delegator_estimation_noise_mean']

        # this must be positive
        # print(f'{system_expected_revenue=}, {epsilon=}')
        delegator_expected_revenue = (1 + epsilon) * system_expected_revenue
        if delegator_expected_revenue < 0:
            delegator_expected_revenue = 0
        # print(f'{delegator_expected_revenue=}')

        # a discount_rate of 0.9 means the 2nd time period is worth 0.9 of the current period.
        discount_rate = 0.9
        mean_discount_rate = params['mean_discount_rate']
        assert(mean_discount_rate <= 0.9)
        assert(mean_discount_rate >= 0.1)
        discount_rate = random.uniform(mean_discount_rate - 0.1, mean_discount_rate + 0.1)
        # TODO: randomize discount_rate
        d = delegator.Delegator(shares, reserve_token_holdings, delegator_expected_revenue,
                                discount_rate, spot_price)
        s['delegators'][d.id] = d

    key = "delegators"
    value = s['delegators']
    return key, value
