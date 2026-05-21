import numpy as np
from deap import base, creator, tools, algorithms

# Define the problem: Minimize Latency and Energy
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

class MOEAD_MEC:
    def __init__(self, num_tasks=10, n_subproblems=20):
        self.num_tasks = num_tasks
        self.n_subproblems = n_subproblems
        self.toolbox = base.Toolbox()
        
        # Parameters
        self.energy_threshold = 50.0  # Constraint
        self.weights = self._generate_weights()
        
        # Gene definition: [Offloading_Decisions, CPU_Frequencies, Trans_Power]
        # Example: 10 tasks * 3 parameters per task = 30 genes
        self.toolbox.register("attr_float", np.random.random)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, 
                             self.toolbox.attr_float, n=num_tasks * 3)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

    def _generate_weights(self):
        # Dynamic Weighting logic: can be adjusted based on congestion
        return np.linspace(0.1, 0.9, self.n_subproblems)

    def evaluate_system(self, individual):
        """
        Algorithm 2: Resource Allocation Sub-routine
        Calculates Latency and Energy based on the individual's genes.
        """
        data = np.array(individual).reshape(3, self.num_tasks)
        offloading = data[0] # 0 to 1 (0=local, 1=edge)
        cpu_freq = data[1]   # CPU Frequency scaling
        p_trans = data[2]    # Transmission Power
        
        latency = 0
        energy = 0
        
        for i in range(self.num_tasks):
            # Simplified MEC Models
            if offloading[i] < 0.5: # Local Execution
                t_exe = 1.0 / (cpu_freq[i] + 0.1)
                e_exe = 0.5 * (cpu_freq[i]**2)
            else: # Edge Execution
                t_exe = (1.0 / p_trans[i]) + 0.2 # Transmission + Edge Proc
                e_exe = p_trans[i] * 0.8
            
            latency += t_exe
            energy += e_exe
            
        # Constraint Handling: Penalty if energy exceeds threshold
        if energy > self.energy_threshold:
            return 9999, 9999
            
        return latency, energy

    def run(self):
        self.toolbox.register("evaluate", self.evaluate_system)
        self.toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=0, up=1, eta=20.0)
        self.toolbox.register("mutate", tools.mutPolynomialBounded, low=0, up=1, eta=20.0, indpb=0.1)
        self.toolbox.register("select", tools.selNSGA2) # MOEA/D often uses neighbor selection

        pop = self.toolbox.population(n=self.n_subproblems)
        # Simple evolutionary loop representing Algorithm 1
        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
            
        final_pop = algorithms.eaMuPlusLambda(pop, self.toolbox, mu=self.n_subproblems, 
                                             lambda_=20, cxpb=0.7, mutpb=0.2, 
                                             ngen=50, verbose=False)
        return final_pop[0]