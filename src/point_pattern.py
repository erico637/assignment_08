from .point import Point
from . import analytics
import random
import numpy as np
import scipy.spatial as ss


class PointPattern(object):
    def __init__(self):
        self.points = []

    def add_point(self, point):
        self.points.append(point)

    def remove_point(self, index):
        try:
            del(self.points[index])
        except IndexError:
            print('Index {} not in list'.format(index))

    def average_nearest_neighbor_distance(self):
        return analytics.average_nearest_neighbor_distance(self.points)

    def average_nearest_neighbor_distance_kdtree(self, mark_name=None, mark_value=None):
        point_list = []
        points = None
        if mark_name is None:
            points = self.points
        else:
            points = list(filter(lambda current_point: current_point.mark[mark_name] == mark_value, self.points))
        for point in points:
            point_list.append(point.get_array())
        point_stack = np.vstack(point_list)
        kdtree = ss.KDTree(point_stack)
        distances = []
        for p in point_stack:
            nearest_neighbor_distance, _ = kdtree.query(p, k=2)
            distances.append(nearest_neighbor_distance[1])
        nn_distances = np.array(distances)
        return np.mean(distances)

    def average_nearest_neighbor_distance_numpy(self):
        point_list = []
        for point in self.points:
            point_list.append(point.get_array())
        ndarray = np.array(point_list)
        nearest_neighbors = []
        temp_nearest_neighbor = None
        for i, point in enumerate(ndarray):
            for j, otherPoint in enumerate(ndarray):
                if i == j:
                    continue
                current_distance = ss.distance.euclidean(point, otherPoint)
                if temp_nearest_neighbor is None:
                    temp_nearest_neighbor = current_distance
                elif temp_nearest_neighbor > current_distance:
                    temp_nearest_neighbor = current_distance
            nearest_neighbors.append(temp_nearest_neighbor)
            temp_nearest_neighbor = None

        return np.mean(nearest_neighbors)

    def count_coincident(self):
        to_return = 0
        handled_indices = []
        for i, point_a in enumerate(self.points):
            for j, point_b in enumerate(self.points):
                if j in handled_indices:
                    continue
                if i == j:
                    continue
                if point_a.is_coincident(point_b):
                    to_return += 1
                    handled_indices.append(j)
        return to_return

    def list_marks(self):
        marks = []
        for point in self.points:
            if 'color' in point.mark and point.mark['color'] not in marks:
                marks.append(point.mark['color'])
        return marks

    def find_subset_with_mark(self, mark):
        return list(filter(lambda current_point: 'color' in current_point.mark and current_point.mark['color'] == mark, self.points))

    def generate_random_points(self, n=None):
        if n is None:
            n = len(self.points)
        to_return = []
        marks = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

        for i in range(n):
            to_return.append(Point(
                round(random.random(), 2),
                round(random.random(), 2),
                color=random.choice(marks)
            ))
        return to_return

    def generate_realizations(self, k):
        n = 100
        to_return = []
        for i in range(k):
            to_return.append(
                analytics.average_nearest_neighbor_distance(
                    self.generate_random_points(count=n)
                )
            )
        return to_return

    def get_critical_points(self):
        return analytics.compute_critical(self.generate_realizations(100))

    def compute_g(self, nsteps):
        ds = np.linspace(0, 1, nsteps)
        current_sum = 0
        for i in range(nsteps):
            o_i = ds[i]
            current_sum += np.abs(ds[np.argsort(np.abs(ds - o_i))[1]] - o_i)
        return current_sum / nsteps

    def generate_random_points(self, count = 2, range_min = 0, range_max = 1, seed = None):
        rng = None
        if seed is None:
            rng = np.random
        else:
            rng = np.random.RandomState(seed)
            random.seed(seed)
        pairs = rng.uniform(range_min, range_max, (count, 2))
        to_return = []
        marks = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        for i in range(len(pairs)):
            to_return.append(Point(
                pairs[i][0],
                pairs[i][1],
                color=random.choice(marks)
            ))
        return to_return
