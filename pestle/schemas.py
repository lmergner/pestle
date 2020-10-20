"""
pestle/schema.py

Marshmallow Schema Base Classes
"""

import json
import falcon
from marshmallow import post_dump, post_load, pre_load, fields, Schema

# https://stackoverflow.com/questions/33782180/marshmallow-nested-change-schema-behavior


class Flagged(fields.Nested):
    """ A Nested schema field that reports itself as such """

    # TODO: write tests for self-reporting nested schemas
    @property
    def schema(self) -> None:
        schema = super(Flagged, self).schema
        setattr(schema, "nested", True)
        return schema


class JsonApi:
    @post_dump(pass_original=True)
    def jsonapi(self, data, original_data):
        """ add jsonapi data to row """
        # xxx: if we exclude / only the id attr, then the _links.self fail, because the id field never gets this far
        q_str = {}
        if self.only:
            q_str["fields"] = list(self.only)
        if self.exclude:
            q_str["exclude"] = list(self.exclude)
        data["_links"] = {
            "self": "/%s/%s" % (self.__class__._endpoint, original_data.oid),
            "rel": "/%s/%s%s"
            % (self.__class__._endpoint, original_data.oid, falcon.to_query_str(q_str)),
        }
        return data


class BaseSchema(Schema):
    """ Base Marshmallow Schema """

    # pylint: disable=E1102,W0212
    class Meta:
        render_module = json  # mujson

    _model = None
    _type = None
    nested = False

    @property
    def _envelop_key(self):
        return "_" + self._type + "s"

    @property
    def _endpoint(self):
        return self._type + "s"

    @property
    def _type(self):
        return self._type

    # Housekeeping
    oid = fields.Int(data_key="id")
    created = fields.DateTime(dump_only=True)
    modified = fields.DateTime(dump_only=True)

    @post_load
    def make_model(self, data):
        """ return an instance of the schema model """
        return self.__class__._model(**data)

    @pre_load(pass_many=True)
    def unwrap(self, data, many):
        """ unwrap the data from the envelop """
        return data.get(self.__class__._envelop_key, data)

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        """ wrap the data in an envelop unless it's nested under another schema """
        if getattr(self, "nested", False):
            return data
        if not many:
            data = [data]
        return {self._envelop_key: data, "_count": len(data)}
