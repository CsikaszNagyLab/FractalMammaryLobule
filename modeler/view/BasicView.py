import vtk

def get_actor(element, styler=None):
    color = element.color
    actor = vtk.vtkActor()

    actor.GetProperty().SetColor(*color)
    styler and styler(actor)
    actor.SetMapper(element.mapper)
    return actor


class BasicView:
    def __init__(self):
        self.renderer = vtk.vtkRenderer()
        self.actors = []

    def register(self, window_interactor):
        window_interactor.GetRenderWindow().AddRenderer(self.renderer)

    def detach_elements(self):
        for s in self.actors:
            self.renderer.RemoveActor(s)
        self.actors = []

    def _get_actors(self, collector):
        self.actors = []

    def attach_elements(self, collector):
        self._get_actors(collector)
        for s in self.actors:
            self.renderer.AddActor(s)
