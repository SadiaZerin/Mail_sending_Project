from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name=fields.Str(required=True)
    email = fields.Str(required=True)

  
    #password = fields.Str(required=True, load_only=True)