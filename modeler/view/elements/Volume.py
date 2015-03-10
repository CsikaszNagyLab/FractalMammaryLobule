import vtk

class Volume:
    def __init__(self, node, color):
        self.node = node
        (source, self.normal) = self._create_volume_from_point(node)
        self.color = color
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(source.GetOutputPort())

    @staticmethod
    def _create_volume_from_point(node):
        if node.parent is None:
            p = node.coords - node.length * node.axis  # [0, 0, node.length]
        else:
            p = node.parent.coords
        source = vtk.vtkLineSource()
        source.SetPoint1(*p)
        source.SetPoint2(*node.coords)
        tube = vtk.vtkTubeFilter()
        tube.SetRadius(node.radius)
        tube.SetNumberOfSides(50)
        tube.CappingOn()
        tube.SetInputConnection(source.GetOutputPort())
        normal = vtk.vtkPolyDataNormals()
        normal.SetInputConnection(tube.GetOutputPort())
        return tube, normal


