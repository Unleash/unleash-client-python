from marshmallow import Schema, fields, post_load, EXCLUDE
from UnleashClient.strategies.constraints import Constraint


class ConstraintSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    contextName = fields.String(attribute="context_name")
    operator = fields.String()
    values = fields.List(fields.String())

    @post_load
    def make_constraint(self, data, **kwargs):  # pylint: disable=W0613, R0201
        return Constraint(**data)
