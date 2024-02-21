class Comparator:
    count = 0

    @staticmethod
    def compare_more(a, b):
        Comparator.count += 1
        return a > b

    @staticmethod
    def compare_less(a, b):
        Comparator.count += 1
        return a < b

    @staticmethod
    def compare_more_or_eq(a, b):
        Comparator.count += 1
        return a >= b

    @staticmethod
    def compare_less_or_eq(a, b):
        Comparator.count += 1
        return a <= b

    @staticmethod
    def reset():
        prev_value = Comparator.count
        Comparator.count = 0
        return prev_value


class Assigner:
    count = 0

    @staticmethod
    def swap(array, ind1, ind2):
        Assigner.count += 2
        array[ind1], array[ind2] = array[ind2], array[ind1]

    @staticmethod
    def assign(array, ind, val):
        Assigner.count += 1
        array[ind] = val

    @staticmethod
    def reset():
        prev_value = Assigner.count
        Assigner.count = 0
        return prev_value
