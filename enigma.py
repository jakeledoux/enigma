import random
import string
from typing import Hashable, List


class Enigma:
    def __init__(self, rotor_seeds: List[str], reflector_seed: str):
        self.rotors = [Rotor(rotor_seed) for rotor_seed in rotor_seeds]
        self.reflector = Reflector(reflector_seed)

    def __call__(self, message):
        output = ''
        for char in message:
            if char.isalpha():
                # Go down through rotors
                for rotor in self.rotors:
                    char = rotor(char)
                # Reflect
                char = self.reflector(char)
                # Go back up through rotors
                for rotor in reversed(self.rotors):
                    char = rotor(char, direction=-1)
                # Rotate appropriate rotors
                for rotor in self.rotors:
                    if not rotor.rotate():
                        break
            output += char
        return output

    def reset(self):
        ''' Re-initializes the machine to it's original state.
        '''
        for rotor in self.rotors:
            rotor.reset()


class Reflector:
    def __init__(self, seed, charset=string.ascii_uppercase):
        self.linear_map = permutate(seed, charset)
        self.map_len = len(self.linear_map)

    def __call__(self, char: str) -> str:
        char = char.upper()
        return self.linear_map[
            (self.linear_map.index(char) + self.map_len // 2) % self.map_len
        ]


class Rotor:
    def __init__(self, seed, charset=string.ascii_uppercase):
        self.position = 0
        self.linear_map = permutate(seed, charset)
        self.map_len = len(self.linear_map)

    def __call__(self, char: str, direction=1) -> str:
        ''' Passes character through self.
        '''
        char = char.upper()
        if direction > 0:
            index = string.ascii_uppercase.index(char)
            index = (index + self.position) % self.map_len
            return self.linear_map[index]
        elif direction < 0:
            index = self.linear_map.index(char)
            index = (index - self.position) % self.map_len
            return string.ascii_uppercase[index]

    def rotate(self) -> bool:
        ''' Rotate wheel one click. Returns whether the next wheel in the chain
            should also rotate.
        '''
        self.position += 1
        return self.position % len(self.linear_map) // 2 == 0

    def reset():
        ''' Re-orients rotor to its original position.
        '''
        self.position = 0


def permutate(seed: Hashable, charset: str) -> str:
    ''' Returns a deterministic permuation of `charset` using `seed`.
    '''
    random.seed(seed)
    permutation = list(charset)
    random.shuffle(permutation)
    return ''.join(permutation)


if __name__ == '__main__':
    # enigma = Enigma(('BFISJXDTVAKLZROWCYHQPNEMUG',))
    enigma = Enigma(rotor_seeds=('minecraft','dubstep','fruity loops'),
                    reflector_seed='sunlight')
    while True:
        print(enigma(input('> ')))
