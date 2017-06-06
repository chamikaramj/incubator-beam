#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import beam_fn_api_pb2 as beam__fn__api__pb2

# This module is experimental. No backwards-compatibility guarantees.


class BeamFnControlStub(object):
  """
  Control Plane API

  Progress reporting and splitting still need further vetting. Also, this may change
  with the addition of new types of instructions/responses related to metrics.

  An API that describes the work that a SDK harness is meant to do.
  Stable
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Control = channel.stream_stream(
        '/org.apache.beam.fn.v1.BeamFnControl/Control',
        request_serializer=beam__fn__api__pb2.InstructionResponse.SerializeToString,
        response_deserializer=beam__fn__api__pb2.InstructionRequest.FromString,
        )


class BeamFnControlServicer(object):
  """
  Control Plane API

  Progress reporting and splitting still need further vetting. Also, this may change
  with the addition of new types of instructions/responses related to metrics.

  An API that describes the work that a SDK harness is meant to do.
  Stable
  """

  def Control(self, request_iterator, context):
    """Instructions sent by the runner to the SDK requesting different types
    of work.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BeamFnControlServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Control': grpc.stream_stream_rpc_method_handler(
          servicer.Control,
          request_deserializer=beam__fn__api__pb2.InstructionResponse.FromString,
          response_serializer=beam__fn__api__pb2.InstructionRequest.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'org.apache.beam.fn.v1.BeamFnControl', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class BeamFnDataStub(object):
  """Stable
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Data = channel.stream_stream(
        '/org.apache.beam.fn.v1.BeamFnData/Data',
        request_serializer=beam__fn__api__pb2.Elements.SerializeToString,
        response_deserializer=beam__fn__api__pb2.Elements.FromString,
        )


class BeamFnDataServicer(object):
  """Stable
  """

  def Data(self, request_iterator, context):
    """Used to send data between harnesses.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BeamFnDataServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Data': grpc.stream_stream_rpc_method_handler(
          servicer.Data,
          request_deserializer=beam__fn__api__pb2.Elements.FromString,
          response_serializer=beam__fn__api__pb2.Elements.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'org.apache.beam.fn.v1.BeamFnData', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class BeamFnStateStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.State = channel.stream_stream(
        '/org.apache.beam.fn.v1.BeamFnState/State',
        request_serializer=beam__fn__api__pb2.StateRequest.SerializeToString,
        response_deserializer=beam__fn__api__pb2.StateResponse.FromString,
        )


class BeamFnStateServicer(object):

  def State(self, request_iterator, context):
    """Used to get/append/clear state stored by the runner on behalf of the SDK.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BeamFnStateServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'State': grpc.stream_stream_rpc_method_handler(
          servicer.State,
          request_deserializer=beam__fn__api__pb2.StateRequest.FromString,
          response_serializer=beam__fn__api__pb2.StateResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'org.apache.beam.fn.v1.BeamFnState', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class BeamFnLoggingStub(object):
  """Stable
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Logging = channel.stream_stream(
        '/org.apache.beam.fn.v1.BeamFnLogging/Logging',
        request_serializer=beam__fn__api__pb2.LogEntry.List.SerializeToString,
        response_deserializer=beam__fn__api__pb2.LogControl.FromString,
        )


class BeamFnLoggingServicer(object):
  """Stable
  """

  def Logging(self, request_iterator, context):
    """Allows for the SDK to emit log entries which the runner can
    associate with the active job.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BeamFnLoggingServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Logging': grpc.stream_stream_rpc_method_handler(
          servicer.Logging,
          request_deserializer=beam__fn__api__pb2.LogEntry.List.FromString,
          response_serializer=beam__fn__api__pb2.LogControl.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'org.apache.beam.fn.v1.BeamFnLogging', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
