import simpy
import random

class CrashAvoidanceSimulator:
    def __init__(self, env):
        self.env = env
        self.vehicle_speed = 0
        self.braking_distance = 0
        self.evasive_success = False

    def emergency_braking(self):
        print(f"Emergency braking initiated at {self.env.now}")
        self.braking_distance = self.vehicle_speed ** 2 / (2 * 9.8)
        yield self.env.timeout(self.braking_distance / self.vehicle_speed)
        print(f"Vehicle stopped at {self.env.now}")
    
    def evasive_maneuver(self):
        print(f"Evasive maneuver initiated at {self.env.now}")
        self.evasive_success = random.choice([True, False])
        yield self.env.timeout(1)
        print(f"Evasive maneuver {'successful' if self.evasive_success else 'failed'} at {self.env.now}")

def run_scenario(env, scenario, simulator):
    if scenario == "emergency_braking":
        yield env.process(simulator.emergency_braking())
    elif scenario == "evasive_maneuver":
        yield env.process(simulator.evasive_maneuver())

env = simpy.Environment()
simulator = CrashAvoidanceSimulator(env)

# Define scenarios
scenarios = ["emergency_braking", "evasive_maneuver"]

# Run scenarios
for scenario in scenarios:
    env.process(run_scenario(env, scenario, simulator))

env.run()