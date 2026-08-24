import numpy as np


class SequenceBuilder:
    """
    Converts buffered landmark vectors into a sequence tensor.
    """

    @staticmethod
    def build(sequence):

        sequence = np.array(sequence)

        return sequence.reshape(sequence.shape[0], sequence.shape[1])