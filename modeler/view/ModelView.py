from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from TreeView import TreeView
from CutsView import CutsView


class ModelView(QVTKRenderWindowInteractor):
    def __init__(self, **kwargs):
        super(ModelView, self).__init__(**kwargs)
        self.__showing = False
        self.__tree_view = TreeView()
        self.__cuts_view = CutsView()

    def register(self):
        self.__tree_view.register(self)
        self.__cuts_view.register(self)

    def setup(self):
        self.__tree_view.renderer.SetViewport(0, 0.5, 1, 1)
        self.__cuts_view.renderer.SetViewport(0, 0, 1, 0.5)
        self.__cuts_view.renderer.SetBackground(0, 0, 0)
        self.__tree_view.renderer.GetActiveCamera().Elevation(-82)
        self.__tree_view.renderer.ResetCamera()

    def update(self):
        super(ModelView, self).update()
        self.__cuts_view.renderer.ResetCamera(self.__cuts_view.get_bounding_box())

    def clean(self):
        self.__tree_view.detach_elements()
        self.__cuts_view.detach_elements()

    def show(self, elements):

        if self.__showing:
            self.clean()

        self.__showing = elements is not None

        if self.__showing:
            self.__tree_view.attach_elements(elements)
            self.__cuts_view.attach_elements(elements)
            self.__tree_view.renderer.ResetCamera()
            self.__cuts_view.renderer.ResetCamera()

        self.update()
