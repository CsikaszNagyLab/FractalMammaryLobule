from view.elements.ElementCollector import ElementCollector

class ModelControl:
    def __init__(self, window, model):
        self.__model = model
        self.__elements = ElementCollector(model)
        self.__elements.notifier.add_callback(self.__cut_changed)

        self.__view = window.model_view
        self.__cut_numbers = window.parameters.cut_numbers
        self.__slider = window.slider

        self.__view.show(self.__elements)
        self.__view.setEnabled(True)

        # set info for cuts
        self.__widest_z = min([(n.x, n.z) for n in model.nodes])[1]
        self.__bottomZ = model.nodes[0].z-model.nodes[0].length
        self.__topZ = max([n.z for n in model.nodes])

        # cut at the best side
        self.__set_cut(self.__widest_z)

        self.__slider.valueChanged.connect(self.__set_cut_from_percentage)
        self.__slider.setEnabled(True)

    def __set_cut_from_percentage(self, p):
        z = self.__get_z_from_percentage(p)
        self.__set_cut(z)

    def __set_cut(self, z):
        if self.__elements.cut_z == z:
            return
        self.__elements.cut(z)

    def __cut_changed(self, z):
        self.__view.update()
        p = self.__get_percentage_from_z(z)
        self.__slider.setValue(p)
        self.__cut_numbers.setText("%d" % self.__model.count_cuts(z))

    def __get_percentage_from_z(self, z):
        if not self.__bottomZ <= z <= self.__topZ:
            raise Exception("Z-value out of bound range")
        return 100.0*(z-self.__bottomZ)/(self.__topZ-self.__bottomZ)

    def __get_z_from_percentage(self, p):
        if not 0 <= p <= 100:
            raise Exception("Percentile value should be between 0 and 100, got: %d " % p)
        return p / 100.0 * (self.__topZ-self.__bottomZ) + self.__bottomZ

    def disconnect(self):
        self.__elements.notifier.remove_callback(self.__cut_changed)
        self.__slider.valueChanged.disconnect(self.__set_cut_from_percentage)
        self.__slider.setEnabled(False)
        self.__view.update()
        self.__view.setEnabled(False)

    model = property(lambda self: self.__elements.model)
