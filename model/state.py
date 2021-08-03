# from model.model import delegator

# NOTE: shares and supply are used somewhat interchangeably.
# shares are supply owned by an individual
# and supply is the aggregate total.
genesis_state = {
    # NOTE: make these a parameter
    # NOTE: cannot import config because of circular import.
    'reserve': 10,  # money--this is only added to when a delegator buys shares
    'supply': 10,  # shares--this is only added to when a delegator buys shares

    # TODO: use minimum_shares=params['initial_supply']
    # id=0 is the original provider of 10 reserve and owns 10 supply
    # delegator_type=2 means use the value_private_price exclusively
    'delegators': None,
    'period_revenue': 0,  # actual dividend revenue generated this timestep.  this is passed directly to the delegators
    'spot_price': 2,
    'expected_revenue': 7,  # mean of dividend revenue coming in per timestep.
    'decoupling_risk': 0,  # spot_price - value_price (can be negative, is cumulative)
    'decoupling_risk_threshold_met': False,
}
