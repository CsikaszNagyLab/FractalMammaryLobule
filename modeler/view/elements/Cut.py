import vtk


class Cut:
    def __init__(self, volume, plane, z):
        self.volume = volume
        self.color = volume.color
        self.cutEdges = vtk.vtkCutter()
        self.cutEdges.SetInputConnection(self.volume.normal.GetOutputPort())
        self.cutEdges.SetCutFunction(plane)
        self.cutEdges.GenerateCutScalarsOn()
        self.cutEdges.SetValue(0, z)

        self.cutStrips = vtk.vtkStripper()
        self.cutStrips.SetInputConnection(self.cutEdges.GetOutputPort())
        self.cutStrips.Update()

        self.cutPoly = vtk.vtkPolyData()
        self.cutPoly.SetPoints(self.cutStrips.GetOutput().GetPoints())
        self.cutPoly.SetPolys(self.cutStrips.GetOutput().GetLines())

        self.cutTriangles = vtk.vtkTriangleFilter()
        self.cutTriangles.SetInput(self.cutPoly)
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.cutPoly)
        self.mapper.SetInputConnection(self.cutTriangles.GetOutputPort())

    def move(self, v):
        self.cutEdges.SetValue(0, v)
        self.cutStrips.Update()
        self.cutPoly.SetPoints(self.cutStrips.GetOutput().GetPoints())
        self.cutPoly.SetPolys(self.cutStrips.GetOutput().GetLines())
        self.mapper.Update()