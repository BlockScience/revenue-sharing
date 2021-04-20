from .model.add_delegator import (instantiate_delegate, 
                                  should_instantiate_delegate)

from .model.delegator_behaviors import (act,
                                        may_act_this_timestep)

from .model.revenue import (revenue_amt, store_revenue, distribute_revenue,
                            expected_revenue_change, expected_revenue,
                            update_delegators_expected_revenue)

from .model.private_price import compute_and_store_private_prices

from .model.delegator_behaviors_bookkeeping import (compute_cliff_vested_shares,
                                                    account_global_state_from_delegator_states,
                                                    store_reserve,
                                                    store_supply,
                                                    store_spot_price)

from .model.initializer import reinitialize_reserve, reinitialize_supply, reinitialize_delegators

psubs = [
    {   
        'label': 'Reinitialize Delegators',
        'policies': {
        },
        'variables': {
            'reserve': reinitialize_reserve,
            'supply': reinitialize_supply,
            'delegators': reinitialize_delegators
        }
        # "reserve": 10,  # money--this is only added to when a delegator buys shares
        # "supply": 10,  # shares--this is only added to when a delegator buys shares

        # # TODO: use minimum_shares=params['initial_supply']
        # # id=0 is the original provider of 10 reserve and owns 10 supply
        # # delegator_type=2 means use the value_private_price exclusively
        # "delegators": None,
        # "period_revenue": 0,  # this is passed directly to the delegators
        # "spot_price": 2,
        # "expected_revenue": 7
    },
    {
        'label': 'Update Vested Shares',
        'policies': {
        },
        'variables': {
            # 'delegators': compute_half_life_vested_shares
            'delegators': compute_cliff_vested_shares
        }
    },
    {
        'label': 'Expected Revenue Change Process',
        'policies': {
            'expected_revenue_change': expected_revenue_change  # how much is paid in.
        },
        'variables': {
            'expected_revenue': expected_revenue,
            'delegators': update_delegators_expected_revenue,
        },
    },
    {
        'label': 'Revenue Arrival Process',
        'policies': {
            'revenue_amt': revenue_amt  # how much is paid in.
        },
        'variables': {
            'period_revenue': store_revenue,
        },
    },
    {
        'label': 'Distribute Revenue',
        'policies': {
        },
        'variables': {
            'delegators': distribute_revenue,
        }
    },
    {
        # if there's a vacant spot, flip a coin
        # (heads, they join, tails nobody joins)
        'label': 'Add Delegator',
        'policies': {
            'should_instantiate_delegate': should_instantiate_delegate
        },
        'variables': {
            'delegators': instantiate_delegate,
        },
    },
    {
        'label': 'Compute and Store Private Prices',
        'policies': {
        },
        'variables': {
            'delegators': compute_and_store_private_prices,
        },
    },
    {
        'label': 'Delegator Behaviors',
        'policies': {
            # outputs ordered list of acting delegatorIds this timestep
            'may_act_this_timestep': may_act_this_timestep
        },
        'variables': {
            'delegators': act,
        },
    },
    {
        'label': 'Delegator Behaviors Bookkeeping',
        'policies': {
            'account_global_state_from_delegator_states': account_global_state_from_delegator_states
        },
        'variables': {
            'reserve': store_reserve,
            'supply': store_supply,
            'spot_price': store_spot_price,
        },
    },
]
