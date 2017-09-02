import math
from decimal import Decimal


class PiEstimator:
    # Expected fraction of needles crossing a line in single grid
    P = Decimal(2) / Decimal(math.pi)

    # Expected fraction of needles crossing no line in a triple grid
    Q = 3 / 2 - 3 / 2 * (4 - math.sqrt(3) / 2) / math.pi

    # Convert the 'real' pi into a high precision Decimal
    pi = Decimal(math.pi)

    def estimate_pi_single_grid(self, number_needles: int) -> (Decimal, Decimal, int):
        min_rel_error = 1E9
        best_pi = 0
        number_of_needles_that_cross = 0
        for number_of_needles_that_cross in [math.floor(number_needles * self.P), math.ceil(number_needles * self.P)]:
            pi = 2 * Decimal(number_needles) / Decimal(number_of_needles_that_cross)
            rel_error = (pi - self.pi) / self.pi
            if rel_error < min_rel_error:
                best_pi = pi
                min_rel_error = rel_error
        return number_of_needles_that_cross, best_pi, min_rel_error

    def estimate_pi_triple_grid(self, number_of_needles: int) -> (Decimal, Decimal, int):
        min_rel_error = 1E9
        best_pi = 0
        number_of_needles_that_does_not_cross = 0
        for number_of_needles_that_does_not_cross in [math.floor(number_of_needles * self.Q),
                                                      math.ceil(number_of_needles * self.Q)]:
            pi = 3 * (8 - Decimal(math.sqrt(3))) / (
                2 * (3 - 2 * (Decimal(number_of_needles_that_does_not_cross) / Decimal(number_of_needles))))
            rel_error = (pi - self.pi) / self.pi
            if rel_error < min_rel_error:
                best_pi = pi
                min_rel_error = rel_error
        return number_of_needles_that_does_not_cross, best_pi, min_rel_error

    def compare_outcomes(self):
        for number_of_needles in [int(2 ** (order + 11)) for order in range(10)]:
            single_result = self.estimate_pi_single_grid(number_of_needles)
            triple_result = self.estimate_pi_triple_grid(number_of_needles)
            print('Single: N={}, n={}, pi={:0.6f}, error:{:.2E}'.format(number_of_needles, *single_result))
            print('Triple: N={}, n={}, pi={:0.6f}, error:{:.2E}'.format(number_of_needles, *triple_result))

    def compute_minimum_number_of_needles(self):
        minimum_single = minimum_triple = 0
        single_result = triple_result = ()
        for number_of_needles in range(100, 10000000):
            single_result = self.estimate_pi_single_grid(number_of_needles)
            best_pi_single = single_result[1]
            if round(best_pi_single, 5) == Decimal('3.14159'):
                minimum_single = number_of_needles
                break
        for number_of_needles in range(1, 10000000):
            triple_result = self.estimate_pi_triple_grid(number_of_needles)
            best_pi_triple = triple_result[1]
            if round(best_pi_triple, 5) == Decimal('3.14159'):
                minimum_triple = number_of_needles
                break
        print('Single: N={}, n={}, pi={:0.6f}, error:{:.2E}'.format(minimum_single, *single_result))
        print('Triple: N={}, n={}, pi={:0.6f}, error:{:.2E}'.format(minimum_triple, *triple_result))


if __name__ == '__main__':
    pie = PiEstimator()
    pie.estimate_pi_single_grid(3000)
    pie.compare_outcomes()
    pie.compute_minimum_number_of_needles()
