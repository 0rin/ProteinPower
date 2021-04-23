import itertools
import random
import math


class Algorithms():
    """Different algorithms to fold a protein. As well as a score-function."""

    @classmethod
    def score(cls, protein):
        """Put a number to a protein folding to indicate its quality. This
        enables comparison of protein foldings. The lower the number, the
        better.
        """
        weak_bonds, strong_bonds = cls.find_connections(protein.acids)
        return len(weak_bonds) * -1 + len(strong_bonds) * -5

    @classmethod
    def find_connections(cls, acids):
        """Find all connections in a folding."""
        relevant_acids = [acid for acid in acids if acid['acid_type'] != 'P']
        weak_bonds = []
        strong_bonds = []
        for acid1, acid2 in itertools.combinations(relevant_acids, 2):
            if abs(acids.index(acid1) - acids.index(acid2)) > 1 and\
               cls._distance(acid1, acid2) == 1:
                if acid1['acid_type'] == 'H' or acid2['acid_type'] == 'H':
                    weak_bonds.append([acid1, acid2])
                else:
                    strong_bonds.append([acid1, acid2])
        return weak_bonds, strong_bonds

    @classmethod
    def fold_n_times(cls, n, protein):
        """Fold the given protein n times. Stop if folding is not possible.
        Note that this is basically a hillclimber.
        """
        highscore = cls.score(protein) or 1
        indices_possible = list(range(1, len(protein.acids)-1))
        for i in range(n):
            success = False
            attempts = 0
            while not success:
                previous_folding = [acid.copy() for acid in protein.acids]
                index = random.choice(indices_possible)
                if protein.fold(index):
                    score = cls.score(protein)
                    if score > highscore:
                        protein.acids = previous_folding
                    else:
                        highscore = score
                    success = True
                else:
                    protein.acids = previous_folding
                    indices_possible.remove(index)
                if not indices_possible:
                    return

    @classmethod
    def random_folding(cls, protein):
        """Return a random folding of the protein."""
        acids_string = protein.acids_string
        previous_acid = {'x': 0,
                         'y': 0,
                         'z': 0,
                         'acid_type': acids_string[0]}
        result = [previous_acid]
        for type_acid in acids_string[1::]:
            collision = True
            while collision:
                axis = random.choice(['x', 'y', 'z'])
                direction = random.choice([-1, 1])
                acid = previous_acid.copy()
                acid['acid_type'] = type_acid
                acid[axis] += direction
                collision = cls._same_position(result, acid)
            previous_acid = acid
            result.append(acid)
        protein.acids = result

    @staticmethod
    def _same_position(folded_part, new_acid):
        """Return True iff the position of some new acid is already taken."""
        for previous_acid in folded_part:
            if previous_acid['x'] == new_acid['x'] and\
               previous_acid['y'] == new_acid['y'] and\
               previous_acid['z'] == new_acid['z']:
                return True
        return False

    @staticmethod
    def _distance(point1, point2):
        """Return euclidean distance between two points."""
        sum_squares = 0
        for dimension in 'xyz':
            sum_squares += abs(point1[dimension] - point2[dimension])**2
        return math.sqrt(sum_squares)