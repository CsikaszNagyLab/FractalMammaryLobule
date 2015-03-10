import vtk
from Volume import Volume
from Cut import Cut
from CutIndicator import CutIndicator
from Notification import Notifier



class ElementCollector:
    def __init__(self, model):
        self.notifier = Notifier()
        self.model = model
        self.lut = vtk.vtkLookupTable()
        lut_num = model.n_levels
        self.lut.SetNumberOfTableValues(lut_num)
        ctf = vtk.vtkColorTransferFunction()
        ctf.SetColorSpaceToDiverging()
        ctf.AddRGBPoint(0.0, 0, 0, 1.0)
        ctf.AddRGBPoint(1.0, 1.0, 0, 0)
        for ii, ss in enumerate([float(xx) / float(lut_num) for xx in range(lut_num)]):
            cc = ctf.GetColor(ss)
            self.lut.SetTableValue(ii, cc[0], cc[1], cc[2], 1.0)

        def get_color(node):
            return self.lut.GetTableValue(node.level)[:3]

        self.volumes = [Volume(n, get_color(n)) for n in self.model.nodes]

        plane = vtk.vtkPlane()
        plane.SetOrigin(0, 0, 0)
        plane.SetNormal(0, 0, 1)

        self.__cut_z = 0
        self.cuts = [Cut(v, plane, self.__cut_z) for v in self.volumes]
        self.cut_indicators = [CutIndicator(c) for c in self.cuts]

    def cut(self, z):
        if z == self.__cut_z:
            return

        for c in self.cuts:
            c.move(z)
        self.__cut_z = z
        self.notifier.notify(self.__cut_z)

    cut_z = property(lambda self: self.__cut_z)