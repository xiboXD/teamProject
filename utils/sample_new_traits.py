import os
import json
import random

class Sampler:
    def __init__(self, traits_file):
        self.traits = self._load_traits(traits_file)

    def _load_traits(self, traits_file):
        with open(traits_file, 'r') as f:
            return json.load(f)

    def sample(self, n):
        output = []
        for i in range(n):
            trait_args = []
            for trait_type, values in self.traits.items():
                trait_args.append({'traitType': trait_type, 'value': random.choice(values)})
            output.append(trait_args)
        return output

# Example usage
traits_file = 'traits.json'  # Specify the path to your JSON file
sampler = Sampler(traits_file)
samples = sampler.sample(5)
print(samples)
