from marshmallow import Schema, fields, post_load, EXCLUDE
from UnleashClient.strategies.parameters import Parameter


class ParameterSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    rollout = fields.Integer()
    stickiness = fields.String()
    groupId = fields.String(attribute="group_id")

    @post_load
    def make_constraint(self, data, **kwargs):  # pylint: disable=W0613, R0201
        return Parameter(**data)
