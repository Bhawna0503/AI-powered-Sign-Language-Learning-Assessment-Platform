from collections import deque
import numpy as np


class FrameBuffer:
    """
    Stores the most recent landmark feature vectors.
    """

    def __init__(self, max_frames=30):
        self.max_frames = max_frames
        self.buffer = deque(maxlen=max_frames)

    def add_frame(self, features):
        """
        Add one landmark feature vector.
        """
        self.buffer.append(features)

    def is_full(self):
        """
        Returns True when enough frames have been collected.
        """
        return len(self.buffer) == self.max_frames

    def get_sequence(self):
        """
        Returns the buffered frames as a NumPy array.
        Shape: (20, 63)
        """
        return np.array(self.buffer)

    def clear(self):
        """
        Clears the frame buffer.
        """
        self.buffer.clear()