from __future__ import absolute_import

from bokeh.properties import HasProps, String, Either, Float, ColorSpec, Instance, List, Enum
from bokeh.charts import Column, Operation
from bokeh.models.sources import ColumnDataSource
from bokeh.models.renderers import GlyphRenderer
from bokeh.enums import Aggregation


class CompositeGlyph(HasProps):
    """Represents a subset of data.

    A collection of hetero or homogeneous glyph
    renderers which represent a subset of data. The
    purpose of the composite glyph is to abstract
    away the details of constructing glyphs, based on
    the details of a subset of data, from the grouping
    operations that a generalized builder must implement.

    In general, the Builder operates at the full column
    oriented data source level, segmenting and assigning
    attributes from a large selection, while the composite glyphs
    will typically be passed an array-like structures with
    one or more singlular attributes to apply.

    Another way to explain the concept is that the Builder
    operates as the groupby, as in pandas, while the
    CompositeGlyph operates as the apply.

    What is the responsibility of the Composite Glyph?
        - Produce GlyphRenderers
        - Apply any aggregations
        - Tag the GlyphRenderers with the group label
        - Apply transforms due to chart operations
            - Operations require implementation of special methods
    """

    label = String('All', help='Identifies the subset of data.')
    values = Either(Column(Float), Column(String), help='Array-like values.')
    color = ColorSpec(default='gray')
    agg = Enum(Aggregation, default=None)

    source = Instance(ColumnDataSource)
    operations = List(Instance(Operation))
    renderers = List(Instance(GlyphRenderer))

    def __init__(self, **kwargs):
        label = kwargs.pop('label', None)

        if label is not None:
            if not isinstance(label, str):
                label = str(label)
            kwargs['label'] = label

        super(CompositeGlyph, self).__init__(**kwargs)

        if self.agg is not None:
            self.source = self.aggregate()
        self.build()

    def aggregate(self):
        pass

    def __stack__(self, glyphs):
        pass

    def __jitter__(self, glyphs):
        pass

    def __dodge__(self, glyphs):
        pass

    def __overlay__(self, glyphs):
        pass

    def apply_operations(self):
        pass

    def build(self):
        raise NotImplementedError('Minimum requirement for CompositeGlyph is to produce renderers.')
