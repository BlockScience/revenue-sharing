def decoupling_risk(params, step, sL, s, inputs):
    key = 'decoupling_risk'

    # NOTE: delegator 0's private price is based on spot price as well as dividend value.
    decoupling_risk = s['decoupling_risk'] + s['spot_price'] - s['delegators'][0].private_price
    value = decoupling_risk
    # print(f'{decoupling_risk=}')

    return key, value


def decoupling_risk_threshold_met(params, step, sL, s, inputs):
    """ Once the threshold is met, it stays decoupled, so do not check again """
    key = 'decoupling_risk_threshold_met'
    decoupling_risk_threshold_met = s['decoupling_risk_threshold_met']
    if not decoupling_risk_threshold_met:
        decoupling_risk_threshold_met = s['decoupling_risk'] > params['decoupling_risk_threshold']
        if decoupling_risk_threshold_met:
            print(f'{decoupling_risk_threshold_met}')
    value = decoupling_risk_threshold_met

    return key, value
