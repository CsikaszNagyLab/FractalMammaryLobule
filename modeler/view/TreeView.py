from BasicView import BasicView, get_actor


class TreeView(BasicView):
    def _get_actors(self, collector):
        def cut_indicator_styler(actor):
            actor.GetProperty().SetLineWidth(5)

        self.actors = ([get_actor(v) for v in collector.volumes] +
                       [get_actor(v, styler=cut_indicator_styler)
                        for v in collector.cut_indicators])
