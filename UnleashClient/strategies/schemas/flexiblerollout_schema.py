from marshmallow import Schema, fields, post_load
from UnleashClient.strategies import FlexibleRollout
from UnleashClient.strategies.constraints.constraint_schema import ConstraintSchema


class FlexibleRolloutSchema(Schema):
    name = fields.String()
    parameters = fields.Dict()
    constraints = fields.List(fields.Nested(ConstraintSchema))

    @post_load
    def make_strategy(self, data, **kwargs):  # pylint: disable=W0613, R0201
        return FlexibleRollout(
            constraints=data['constraints'],
            parameters=data['parameters']
        )
