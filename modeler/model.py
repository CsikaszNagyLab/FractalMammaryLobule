# -*- coding: utf-8 -*-
import numpy as np


def rad_to_grad(angle):
    return angle*180/np.pi


def grad_to_rad(angle):
    return angle*np.pi/180


def angle_between_unit_vectors(v1, v2):
    return np.arccos(np.dot(v1, v2))


class DuctModel:
    def __init__(self, alpha, beta, length, length_ratio, radius,
                 radius_ratio, n_levels, stem_inclination=np.pi/2,
                 stem_rotation=0, tree_rotation=0):
        self.alpha = alpha
        beta = beta if isinstance(beta, list) else [beta]
        self.beta = [stem_inclination] + beta + beta[-1::]*(n_levels-len(beta))
        self.length = length
        self.length_ratio = length_ratio
        self.radius = radius
        self.radius_ratio = radius_ratio
        self.nodes = []
        self.n_levels = n_levels
        self.stem_rotation = stem_rotation
        self.tree_rotation = tree_rotation
        self.__add_node(Node(model=self))

    def __add_node(self, node):
        node.idx = len(self.nodes)
        self.nodes.append(node)
        if node.level < self.n_levels:
            self.__branch(node)

    def __branch(self, parent):
        self.__add_node(Node(parent, -1))
        self.__add_node(Node(parent, 1))

    def count_cuts(self, z):
        return len([n for n in self.nodes if n.is_cutting(z)])


def rotation_matrix(axis, theta):
    axis = axis/np.sqrt(np.dot(axis, axis))
    a = np.cos(theta/2)
    b, c, d = -axis*np.sin(theta/2)
    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                     [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                     [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])


def rotate_point(p, axis, theta):
    axis = axis/np.sqrt(np.dot(axis, axis))
    a = np.cos(theta/2)
    b, c, d = -axis*np.sin(theta/2)
    rotmat = np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                       [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                       [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

    return np.dot(rotmat, p)


class Node:
    def __init__(self, parent=None, sign=0, model=None):
        self.parent = parent
        if parent is None:
            pcoords = np.array([0, 0, 0])
            self.model = model
            self.length = model.length
            self.radius = model.radius
            self.level = 0
            self.beta = model.beta[self.level]
            self.alpha = 0
            axis_rotation = rotation_matrix(np.array([0, 0, 1]),
                                            self.model.stem_rotation)
            self.axis = self.__get_axis(axis_rotation)
            self.rotation = np.dot(rotation_matrix(self.axis,
                                                   self.model.tree_rotation),
                                   axis_rotation)

        else:
            pcoords = parent.coords
            self.model = parent.model
            self.level = parent.level + 1
            self.beta = parent.beta + sign * self.model.beta[self.level]
            self.alpha = parent.alpha + self.model.alpha
            self.length = parent.length * self.model.length_ratio
            self.radius = parent.radius * self.model.radius_ratio
            self.rotation = np.dot(rotation_matrix(parent.axis,
                                                   self.model.alpha),
                                   parent.rotation)
            self.axis = self.__get_axis(self.rotation)
        self.coords = pcoords + self.length*self.axis

    def __get_axis(self, axis_rotation):
        ax = np.array([0, np.cos(self.beta), np.sin(self.beta)])
        return np.dot(axis_rotation, ax)

    def is_cutting(self, z):
        if self.parent is None:
            pz = self.z-self.length
        else:
            pz = self.parent.z

        # arcos(...) is used to get the angle between the cylinder axis and
        # the z axis: self.axis[2] equals the dot product between the two
        # unit vectors
        extruding_z = self.radius * np.cos(np.pi/2-np.arccos(np.absolute(self.axis[2])))
        minz = min(pz, self.z)
        maxz = max(pz, self.z)
        return (minz - extruding_z) < z < (maxz + extruding_z)

    x = property(lambda self: self.coords[0])
    y = property(lambda self: self.coords[1])
    z = property(lambda self: self.coords[2])
