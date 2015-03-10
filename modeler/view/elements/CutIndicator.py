import vtk


class CutIndicator:
    def __init__(self, cut):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(cut.cutEdges.GetOutputPort())
        self.color = (1.0 - cut.color[0], 1.0 - cut.color[1], 1.0 - cut.color[2])