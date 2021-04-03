def get_value_private_price(delegator, supply, owners_share, reserve_to_revenue_token_exchange_rate, reserve,
                            risk_adjustment):
    # NOTE: this is the discounted value of the dividends
    dividend_value = delegator.dividend_value(supply, owners_share, reserve_to_revenue_token_exchange_rate)

    # NOTE: this is the current spot price, from the invariant
    share_value = 2 * reserve / supply

    risk_adjusted_share_value = share_value * risk_adjustment

    value_private_prices = dividend_value + risk_adjusted_share_value

    # print(f'{timestep=}, {private_price=}')
    return value_private_prices


def get_regression_to_mean_private_price(previous_avg_price, spot_price, smoothing_factor):
    """
    exponential moving average at last timestep, over past 14 days
    the idea is that the spot_price reverts to this mean.
    avg_price(t) = (1-alpha) * avg_price(t-1) + alpha * price(t)
    """

    # print(f'{sL=}')

    regression_to_mean_private_price = (1 - smoothing_factor) * previous_avg_price + smoothing_factor * spot_price

    return regression_to_mean_private_price


def get_avg_delta_price(previous_avg_delta_price, delta_spot_price, smoothing_factor):

    avg_delta_price = (1 - smoothing_factor) * previous_avg_delta_price + smoothing_factor * delta_spot_price
    # print(f'{avg_delta_price=}, {smoothing_factor=}, {previous_avg_delta_price=}, {delta_spot_price=}')
    return avg_delta_price


def get_trendline_private_price(avg_delta_price, spot_price):
    """
    start with regression to mean change in price.
    avg_delta_price: exponentially smoothed average change in the spot price.
    previous_avg_delta_price: previous value of above.
    i.e. if it has been trending up, it will continue trending up.
    """

    return spot_price + avg_delta_price


def compute_and_store_private_prices(params, step, sL, s, inputs):
    """
    There are 3 components to private price for a typical market actor.
    1) regression to mean (smooth weighted average)
    2) private price
    3) trendline price
    """
    delegators = s['delegators']
    supply = s['supply']
    reserve = s['reserve']
    owners_share = params['owners_share']
    risk_adjustment = params['risk_adjustment']
    reserve_to_revenue_token_exchange_rate = params['reserve_to_revenue_token_exchange_rate']
    # smoothing_factor = params['smoothing_factor']
    spot_price = s['spot_price']

    # sL is a list of lists:
    # use [-1] to get to previous timestep, then
    # use [0] to get 1st substep (beginning of the previous timestep)
    # use ['spot_price'] to access the spot price of that time.
    previous_timestep = sL[-1][0]
    # timestep = s['timestep']
    # print(f'{timestep=}: {previous_timestep=}')
    # print(f'{timestep=}')
    previous_spot_price = previous_timestep['spot_price']

    delta_spot_price = spot_price - previous_spot_price
    # print(f'{timestep=}, {spot_price=}, {previous_spot_price=}')

    for delegator in delegators.values():
        # non-time series calculations
        delegator.value_private_price = get_value_private_price(delegator, supply, owners_share,
                                                                reserve_to_revenue_token_exchange_rate, reserve,
                                                                risk_adjustment)
        # print(f'{delegator.value_private_price=}')

        # time series_calculations
        previous_avg_price = delegator.regression_to_mean_private_price
        previous_avg_delta_price = delegator.avg_delta_price

        # this only works if there is a previous spot price.
        delegator.regression_to_mean_private_price = \
            get_regression_to_mean_private_price(previous_avg_price, spot_price,
                                                 delegator.smoothing_factor)

        delegator.avg_delta_price = get_avg_delta_price(previous_avg_delta_price, delta_spot_price,
                                                        delegator.smoothing_factor)

        delegator.trendline_private_price = \
            get_trendline_private_price(delegator.avg_delta_price, spot_price)

        delegator.private_price = (delegator.regression_to_mean_private_price * delegator.component_weights[0]
                                   + delegator.value_private_price * delegator.component_weights[1]
                                   + delegator.trendline_private_price * delegator.component_weights[2])

        # print(f'{delegator.regression_to_mean_private_price=}')
        # print(f'{delegator.trendline_private_price=}')
        # print(f'{delegator.private_price=}')

    # print(delegators)
    key = 'delegators'
    value = delegators
    return key, value
