# Title:       Square-Sum Permutations
# Author:      Noah Niederklein (noah.niederklein@student.cune.edu)
# Created:     04/20/2025
# Modified:    04/22/2025
# Description: This file contains code that builds and counts the number of square-sum permutations
#              of a given length n. A square-sum permutation is a permutation of the first n positive
#              integers where the sum of every pair of consecutive numbers is a perfect square.
#              Example: 8 1 15 10 6 3 13 12 4 5 11 14 2 7 9

class SquareSumPermutations:
    """ Class to compute the number of valid square-sum permutations of integers 1..n. """

    def __init__(self, n: int):
        """ Initialize with n and compute the number of valid square-sum permutations. """

        self.n = n
        self.count = 0
        self.perfect_squares = self._get_perfect_squares()
        self.square_sum_pairs = self._square_sum_pairs(n)

        # Compute the number of permutations of 1..n such that the sum
        # of every pair of consecutive numbers is a perfect square
        self.build_and_count_paths()

    def _get_perfect_squares(self) -> set:
        """ Create a set of perfect squares up to 2n - 1. """

        perfect_squares = set()
        
        # Start at k = 2 because two distinct positive integers cannot add to 1
        k = 2
        while k * k < 2 * self.n:
            perfect_squares.add(k * k)
            k += 1

        return perfect_squares
    
    def _square_sum_pairs(self, n: int) -> dict[int, list[int]]:
        """ Determine which integers between 1 and n, inclusive, add to a perfect square.
        
        Example for n = 8:
            current = {
                1: [3, 8],
                2: [7],
                3: [1, 6],
                4: [5],
                5: [4],
                6: [3],
                7: [2],
                8: [1]
            }
        """

        # Base case
        if n == 1:
            return {1: []}
        
        # Build off the result for n - 1
        current = self._square_sum_pairs(n - 1)

        # Determine for which integers k, with 1 <= k < n, the sum k + n is a perfect square
        current[n] = []
        for k in range(1, n):
            if k + n in self.perfect_squares:
                current[k].append(n)
                current[n].append(k)
        
        return current
    
    def path_extensions(self, path: list[int]) -> list[int]:
        """ Determine which integers can be appended to a given path.
        
        Example:
            self.path_extensions(15, [15, 10, 6, 3]) -> [1, 13]

            6 is not in choices because 6 is in the path.
            22 is not in choices because 22 > 15 and n = 15.
        """

        # Removing the next two lines results in a(1) = 1, which is incorrect
        # 1 would be allowed as a starting point even when no further move is
        # possible, and since the length of the path would be 1, it would count
        if self.n == 1:
            return []
        
        # If the path is empty, allow starting from any number between 1 and n
        if path == []:
            return [k for k in range(1, self.n + 1)]
        
        # last is the last number in the path. The number that is appended
        # to the path and last should add to a perfect square.
        # Using the list comprehension [k for k in self.square_sum_pairs[last] if k not in path]
        # appears to be slightly slower
        last = path[-1]
        extensions = []
        for k in self.square_sum_pairs[last]:
            if k not in path:
                extensions.append(k)
        return extensions

    def build_and_count_paths(self, path: list[int] | None = None) -> None:
        """ Recursively builds paths and count the number of paths of length n. """

        if path is None:
            path = []

        # The path contains every integer 1..n (not a partial path,
        # which only includes a subset of the numbers 1..n)
        if len(path) == self.n:
            # To keep track of or view the paths, you can print it,
            # append it to a file, or do something else if desired
            # print(path)

            # Update self.count because another path of length n has been found
            self.count += 1
        
        # Try to keep extending the path by recursively calling the function with the new path
        for extension in self.path_extensions(path):
            self.build_and_count_paths(path + [extension])

def a(n: int) -> int:
    """ Return the number of permutations of 1..n such that the sum of every pair of consecutive numbers is a perfect square. """

    return SquareSumPermutations(n).count

if __name__ == "__main__":
    # Example case
    print(a(25))
