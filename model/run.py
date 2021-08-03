import pandas
from cadCAD import engine
from config import exp

def run():
    exec_mode = engine.ExecutionMode()
    ctx = engine.ExecutionContext(context=exec_mode.local_mode)
    simulation = engine.Executor(exec_context=ctx, configs=exp.configs)
    system_events, tensor_field, sessions = simulation.execute()

    # Post-processing
    df = pandas.DataFrame(system_events)
    df = df[df["substep"] == df.substep.max()]

    return df
