from cadCAD import configuration

from .psub import psubs
from .state import genesis_state

# Parameters
# Values are lists because they support sweeping.

params = {
        'initial_reserve': [10],
        'initial_supply': [10],
        'expected_revenue': [7],
        'owners_share': [0.25],         # 1-theta  (theta is what all of the other delegators get)
        'arrival_rate': [0.5],
        'expected_reserve_token_holdings': [25],
        'delegator_estimation_noise_mean': [0],
        'delegator_estimation_noise_variance': [1],  # proportional to expected_revenue
        'reserve_to_revenue_token_exchange_rate': [1],
        'delegator_activity_rate': [0.5],
        'mininum_required_price_pct_diff_to_act': [0.02],
        'risk_adjustment': [0.7],  # cut 30% of the value off due to risk
        'half_life_vesting_rate': [0.5],  # this is the fraction of shares that vest each timestep if using half life vesting
        'cliff_vesting_timesteps': [14],  # this is the number of timesteps until shares are fully vested
        'num_days_for_trends': [14],  # this is the number of days to consider for private price calculation's regression to mean price
        'halflife': [0.5],  # halflife for trend analysis
        'smoothing_factor': [0.5],  # alpha for trend analysis
        'mean_discount_rate': [0.7],  # this is the mean of the delegators' discount rates
    }

simulation_config = configuration.utils.config_sim({
    'T': range(500),
    'N': 1,
    'M': params
})

exp = configuration.Experiment()

exp.append_configs(sim_configs=simulation_config,
                   initial_state=genesis_state,
                   partial_state_update_blocks=psubs)
