# TODO: Fix symmetry when using multiple rotors.

class Enigma:
    def __init__(self, linear_maps):
        self.rotors = [Rotor(linear_map=linear_map)
                       for linear_map in linear_maps]
        pass

    def __call__(self, message):
        output = ''
        for char in message:
            rotate = True
            for rotor in self.rotors:
                char = rotor(char)
                if rotate:
                    rotate = rotor.rotate()
            output += char
        return output

    def reset(self):
        ''' Re-initializes the machine to it's original state.
        '''
        for rotor in self.rotors:
            rotor.reset()


class Rotor:
    def __init__(self, linear_map):
        self.position = 0
        self.linear_map = linear_map
        self.side_a = self.linear_map[:len(self.linear_map) // 2]
        self.side_b = self.linear_map[len(self.linear_map) // 2:]

    def __call__(self, char: str) -> str:
        ''' Passes character through self.
        '''
        char = char.upper()
        if char in self.side_a:
            index = self.side_a.index(char)
            return self.side_b[(index + self.position) % len(self.side_a)]
        elif char in self.side_b:
            index = (self.side_b.index(char) - self.position) % len(self.side_b)
            return self.side_a[index]
        return char

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


if __name__ == '__main__':
    # enigma = Enigma(('BFISJXDTVAKLZROWCYHQPNEMUG',))
    # enigma = Enigma(('BFISJXDTVAKLZROWCYHQPNEMUG',
    #                  'OUHLTEKQBVNAXCZSWGDYJFPIMR',
    #                  'TZHDGLEJSQKRPFWCBVOUIMXYNA',
    #                  'RMLYDFSCBWGKOXEQIVHUNJATPZ'))
    # while True:
    #     print(enigma(input('> ')))
    rotor = Rotor('fbdace')
    while True:
        output = ''
        for c in input('> '):
            output += rotor(c)
        print(output)
