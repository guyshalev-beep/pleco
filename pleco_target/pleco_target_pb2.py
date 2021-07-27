# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pleco_target.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pleco_target.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12pleco_target.proto\" \n\x0cK8sResources\x12\x10\n\x08snippets\x18\x01 \x03(\t\"R\n\x0cK8sGWRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x0c\n\x04\x62ody\x18\x02 \x01(\t\x12\x10\n\x08\x66ileName\x18\x03 \x01(\t\x12\x11\n\tnamespace\x18\x04 \x01(\t\"?\n\rK8sGWResponse\x12\x11\n\tresources\x18\x01 \x03(\t\x12\x0e\n\x06status\x18\x02 \x01(\x08\x12\x0b\n\x03msg\x18\x03 \x01(\t2\x91\x01\n\x05K8sGW\x12\'\n\x06GetNSs\x12\r.K8sGWRequest\x1a\x0e.K8sGWResponse\x12\x30\n\x0f\x41pplyDeployment\x12\r.K8sGWRequest\x1a\x0e.K8sGWResponse\x12-\n\x0c\x41pplyService\x12\r.K8sGWRequest\x1a\x0e.K8sGWResponseb\x06proto3'
)




_K8SRESOURCES = _descriptor.Descriptor(
  name='K8sResources',
  full_name='K8sResources',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='snippets', full_name='K8sResources.snippets', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=54,
)


_K8SGWREQUEST = _descriptor.Descriptor(
  name='K8sGWRequest',
  full_name='K8sGWRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_id', full_name='K8sGWRequest.user_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='body', full_name='K8sGWRequest.body', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fileName', full_name='K8sGWRequest.fileName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='namespace', full_name='K8sGWRequest.namespace', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=138,
)


_K8SGWRESPONSE = _descriptor.Descriptor(
  name='K8sGWResponse',
  full_name='K8sGWResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resources', full_name='K8sGWResponse.resources', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='K8sGWResponse.status', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='msg', full_name='K8sGWResponse.msg', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=140,
  serialized_end=203,
)

DESCRIPTOR.message_types_by_name['K8sResources'] = _K8SRESOURCES
DESCRIPTOR.message_types_by_name['K8sGWRequest'] = _K8SGWREQUEST
DESCRIPTOR.message_types_by_name['K8sGWResponse'] = _K8SGWRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

K8sResources = _reflection.GeneratedProtocolMessageType('K8sResources', (_message.Message,), {
  'DESCRIPTOR' : _K8SRESOURCES,
  '__module__' : 'pleco_target_pb2'
  # @@protoc_insertion_point(class_scope:K8sResources)
  })
_sym_db.RegisterMessage(K8sResources)

K8sGWRequest = _reflection.GeneratedProtocolMessageType('K8sGWRequest', (_message.Message,), {
  'DESCRIPTOR' : _K8SGWREQUEST,
  '__module__' : 'pleco_target_pb2'
  # @@protoc_insertion_point(class_scope:K8sGWRequest)
  })
_sym_db.RegisterMessage(K8sGWRequest)

K8sGWResponse = _reflection.GeneratedProtocolMessageType('K8sGWResponse', (_message.Message,), {
  'DESCRIPTOR' : _K8SGWRESPONSE,
  '__module__' : 'pleco_target_pb2'
  # @@protoc_insertion_point(class_scope:K8sGWResponse)
  })
_sym_db.RegisterMessage(K8sGWResponse)



_K8SGW = _descriptor.ServiceDescriptor(
  name='K8sGW',
  full_name='K8sGW',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=206,
  serialized_end=351,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetNSs',
    full_name='K8sGW.GetNSs',
    index=0,
    containing_service=None,
    input_type=_K8SGWREQUEST,
    output_type=_K8SGWRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ApplyDeployment',
    full_name='K8sGW.ApplyDeployment',
    index=1,
    containing_service=None,
    input_type=_K8SGWREQUEST,
    output_type=_K8SGWRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ApplyService',
    full_name='K8sGW.ApplyService',
    index=2,
    containing_service=None,
    input_type=_K8SGWREQUEST,
    output_type=_K8SGWRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_K8SGW)

DESCRIPTOR.services_by_name['K8sGW'] = _K8SGW

# @@protoc_insertion_point(module_scope)
