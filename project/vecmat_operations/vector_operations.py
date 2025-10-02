from math import sqrt, acos


class Vector:
    """
    A class for working with vectors.

    Attributes:
        vector : list[float]
            A list representing the vector.

    Methods:
        __init__(data: list[float])
            Initializes a Vector object with the given data.

        __len__() -> int
            Returns the length of the vector.

        __mul__(other: "Vector") -> float
            Returns the dot product of two vectors.

        norm() -> float
            Returns the norm (length) of the vector.

        __xor__(other: "Vector") -> float
            Returns the angle between two vectors in radians.

        __repr__() -> str
            Returns a string representation of the vector.
    """

    def __init__(self, data: list[float]):
        """
        Initializes a Vector object

        Args:
            data (list[float]): A list of values to create the vector
        """
        self.vector = data

    def __len__(self) -> int:
        """
        Returns the length of the vector

        Returns:
            int: The number of elements in the vector
        """
        return len(self.vector)

    def __mul__(self, other: "Vector") -> float:
        """
        Computes the dot product of two vectors

        Args:
            other (Vector): Other vector

        Raises:
            ValueError: If the lengths of the vectors are not the same

        Returns:
            float: The dot product of the two vectors.
        """
        if len(self) != len(other):
            raise ValueError("Vectors must have the same length")

        return sum(self.vector[i] * other.vector[i] for i in range(len(self)))

    def norm(self) -> float:
        """
        Computes the norm (length) of the vector.

        Returns:
            float: The norm of the vector
        """
        return sqrt(sum(x**2 for x in self.vector))

    def __xor__(self, other: "Vector") -> float:
        """
        Computes the angle between two vectors

        Args:
            other (Vector): The vector to find the angle with

        Raises:
            ValueError:         If the lengths of the vectors are not the same
            ZeroDivisionError:  If the norm of one of the vectors is zero.

        Returns:
            float: The angle between the two vectors in radians.
        """
        if len(self) != len(other):
            raise ValueError("Vectors must have the same length")

        self_norm = self.norm()
        other_norm = other.norm()

        if self_norm == 0 or other_norm == 0:
            raise ZeroDivisionError("The norm of one of the vectors is zero")

        dot_prod = self * other
        return acos(dot_prod / (self_norm * other_norm))

    def __repr__(self) -> str:
        """
        Returns a string representation of the vector.

        Returns:
            str: A string representation of the vector.
        """
        return f"Vector({self.vector})"
