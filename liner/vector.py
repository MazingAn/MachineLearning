from decimal import Decimal, getcontext
import math

getcontext().prec = 25

class Vector(object):

    CANNOT_NORMALIZE_THE_ZERO_VECTOR = 'cannot normalize the zero vector'
    CANNOT_COMPUT_AN_ANGLE_WITH_THE_ZERO_VECTOR = 'cannot comput an angle with the zero vector'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)
            self.idx = 0

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __iter__(self):
        return iter(self)

    def next(self):
       self.idx += 1
       try:
           return Decimal(self.coordinates[self.idx-1])
       except IndexError:
           self.idx = 0
           raise StopIteration  # Done iterating.

    def __getitem__(self,index):
        return Decimal(self.coordinates[index])

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [x*c for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        return math.sqrt(sum([x**2 for x in self.coordinates]))
    
    def normalized(self):
        try:
            mat = self.magnitude()
            return self.times_scalar(1/mat)
        except ZeroDivisionError:
            raise ValueError(self.CANNOT_NORMALIZE_THE_ZERO_VECTOR)
    
    def dot(self, v):
        return sum([x*y for x, y in zip(self.coordinates, v.coordinates)])
    
    def angle_with(self, v, in_degress=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            udot = round(u1.dot(u2), 7)
            rad = math.acos(udot)
            if in_degress:
                return rad * 180 / math.pi
            return rad 
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_THE_ZERO_VECTOR:
                raise Exception(self.CANNOT_COMPUT_AN_ANGLE_WITH_THE_ZERO_VECTOR) 
            else:
                raise e
    
    def is_parallel_to(self, v):
        return ( self.is_zero() or
            v.is_zero() or
            MyDecimal.is_near_zero(self.angle_with(v)) or #接近0
            MyDecimal.is_near_zero(self.angle_with(v) - math.pi)) #接近pi

    def is_orthogonal_to(self, v):
        return MyDecimal.is_near_zero(self.dot(v))
    
    def component_orthogonal_to(self, v):
        try:
            vpra = self.component_parallel_to(v)
            return self.minus(vpra)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_THE_ZERO_VECTOR:
                raise Exception(self.CANNOT_NORMALIZE_THE_ZERO_VECTOR)
            else:
                raise e

    def component_parallel_to(self, v):
        try:
            u = v.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_THE_ZERO_VECTOR:
                raise Exception(self.CANNOT_NORMALIZE_THE_ZERO_VECTOR)
            else:
                raise e

    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            return Vector([
                y_1*z_2 - z_1*y_2,
                -(x_1*z_2 - z_1*x_2),
                x_1*y_2 - y_1*x_2
            ])
        except ValueError as e:
            raise e
    
    def area_of_parallelogram(self, v):
        try:
            return self.cross(v).magnitude()
        except ValueError as e:
            raise e


    def area_of_triangle(self, v):
        try:
            return (self.cross(v).magnitude()) / 2
        except ValueError as e:
            raise e

    def is_zero(self):
        return MyDecimal.is_near_zero(self.magnitude())

class MyDecimal(Decimal):
    @staticmethod
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

if __name__ == '__main__':
    v1 = Vector([8.462, 7.893, -8.187])
    v2 = Vector([6.984, -5.975, 4.778])
    print(v1.cross(v2))

    v1 = Vector([-8.987, -9.838, 5.031])
    v2 = Vector([-4.268, -1.861, -8.866])
    print(v1.area_of_parallelogram(v2))


    v1 = Vector([1.5, 9.547, 3.691])
    v2 = Vector([-6.007, 0.124, 5.772])
    print(v1.area_of_triangle(v2))

