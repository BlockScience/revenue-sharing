from . import delegator
# import random
import scipy.stats as stats


# policy
def should_instantiate_delegate(params, step, sL, s):
    # flip a coin (1 joins if there's room and random says to)
    should_instantiate_delegate = False

    if len(s['delegators']) < params['max_delegator_count']:
        # NOTE: Uncomment this if you want arrival to be randomized.
        # rng = random.random()
        # if rng >= params['arrival_rate']:
        should_instantiate_delegate = True

    return {"should_instantiate_delegate": should_instantiate_delegate}


# mechanism
def instantiate_delegate(params, step, sL, s, inputs):
    if inputs['should_instantiate_delegate']:
        spot_price = s['spot_price']

        # add new members
        shares = 0
        for i in range(params['max_delegator_count'] - len(s['delegators'])):
            # reserve_token_holdings = params['expected_reserve_token_holdings'] * stats.expon.rvs()
            reserve_token_holdings = params['expected_reserve_token_holdings']
            print(f'{reserve_token_holdings=}')
            if reserve_token_holdings < 0:
                reserve_token_holdings = 0

            system_expected_revenue = s['expected_revenue']

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

            mean_discount_rate = params['mean_discount_rate']
            assert(mean_discount_rate <= 0.9)
            assert(mean_discount_rate >= 0.1)

            # NOTE: choose one of these discount_rate calculations
            discount_rate = 0.9
            # discount_rate = random.uniform(mean_discount_rate - 0.1, mean_discount_rate + 0.1)

            # greater than 1/2 and less than 1. so draw an integer rv >= 1, and set the variable to 1-1/2^(rv)

            # NOTE: choose one of these smoothing_factor calculations
            # smoothing_factor = 1 - (1 / 2) ** random.uniform(1, 10)
            smoothing_factor = 0.1
            print(f'{smoothing_factor=}')

            d = delegator.Delegator(shares=shares,
                                    reserve_token_holdings=reserve_token_holdings,
                                    expected_revenue=delegator_expected_revenue,
                                    discount_rate=discount_rate,
                                    spot_price=spot_price,
                                    smoothing_factor=smoothing_factor)

            s['delegators'][d.id] = d

    key = "delegators"
    value = s['delegators']
    return key, value
