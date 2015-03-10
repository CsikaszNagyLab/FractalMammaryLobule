from BasicView import BasicView, get_actor


class CutsView(BasicView):
    def _get_actors(self, collector):
        self.actors = [get_actor(v) for v in collector.cuts]

    def get_bounding_box(self):
        bounding_boxes = [a.GetBounds() for a in self.actors if a.GetVisibility()]

        if len(bounding_boxes) == 0:
            return -1, 1, -1, 1, -1, 1

        def min_element_at(lst, i):
            return min(lst, key=lambda x: x[i])[i]

        def max_element_at(lst, i):
            return max(lst, key=lambda x: x[i])[i]

        bounding_box = (
            min_element_at(bounding_boxes, 0),
            max_element_at(bounding_boxes, 1),
            min_element_at(bounding_boxes, 2),
            max_element_at(bounding_boxes, 3),
            min_element_at(bounding_boxes, 4),
            max_element_at(bounding_boxes, 5))
        return bounding_box
