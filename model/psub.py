from .model.add_delegator import (instantiate_delegate,
                                  should_instantiate_delegate)

from .model.delegator_behaviors import (act,
                                        may_act_this_timestep,
                                        update_delegator_2_to_best_strategy)

from .model.revenue import (revenue_amt, store_revenue, distribute_revenue, update_delegators_expected_revenue)
# expected_revenue_change, expected_revenue,
# update_delegators_expected_revenue)

from .model.private_price import compute_and_store_private_prices

from .model.delegator_behaviors_bookkeeping import (compute_cliff_vested_shares,
                                                    account_global_state_from_delegator_states,
                                                    store_reserve,
                                                    store_supply,
                                                    store_spot_price)

from .model.decoupling_risk import decoupling_risk, decoupling_risk_threshold_met

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
    },
    {
        'label': 'Switch to Best Strategy',
        'policies': {
        },
        'variables': {
            'delegators': update_delegator_2_to_best_strategy
        }
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
        'label': 'Decoupling Risk',
        'policies': {
        },
        'variables': {
            'decoupling_risk': decoupling_risk
        }
    },
    {
        'label': 'Decoupling Risk Threshold',
        'policies': {
        },
        'variables': {
            'decoupling_risk_threshold_met': decoupling_risk_threshold_met
        }
    },    
    {
        'label': 'Revenue Arrival Process',
        'policies': {
            'revenue_amt': revenue_amt  # how much is paid in.
        },
        'variables': {
            'period_revenue': store_revenue,
            'delegators': update_delegators_expected_revenue
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
