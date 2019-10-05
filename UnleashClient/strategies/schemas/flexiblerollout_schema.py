from marshmallow import Schema, fields, post_load, EXCLUDE
from UnleashClient.strategies import FlexibleRollout
from UnleashClient.strategies.constraints.constraint_schema import ConstraintSchema


class FlexibleRolloutSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    parameters = fields.Dict()
    constraints = fields.List(fields.Nested(ConstraintSchema))

    @post_load
    def make_strategy(self, data, **kwargs):  # pylint: disable=W0613, R0201
        return FlexibleRollout(**data)
