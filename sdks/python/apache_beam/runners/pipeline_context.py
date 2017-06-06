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

"""Utility class for serializing pipelines via the runner API.

For internal use only; no backwards-compatibility guarantees.
"""


from apache_beam import coders
from apache_beam import pipeline
from apache_beam import pvalue
from apache_beam.core.runners.api import beam_runner_api_pb2
from apache_beam.transforms import core


class _PipelineContextMap(object):
  """This is a bi-directional map between objects and ids.

  Under the hood it encodes and decodes these objects into runner API
  representations.
  """
  def __init__(self, context, obj_type, proto_map=None):
    self._pipeline_context = context
    self._obj_type = obj_type
    self._obj_to_id = {}
    self._id_to_obj = {}
    self._id_to_proto = proto_map if proto_map else {}
    self._counter = 0

  def _unique_ref(self):
    self._counter += 1
    return "ref_%s_%s" % (self._obj_type.__name__, self._counter)

  def populate_map(self, proto_map):
    for id, proto in self._id_to_proto.items():
      proto_map[id].CopyFrom(proto)

  def get_id(self, obj):
    if obj not in self._obj_to_id:
      id = self._unique_ref()
      self._id_to_obj[id] = obj
      self._obj_to_id[obj] = id
      self._id_to_proto[id] = obj.to_runner_api(self._pipeline_context)
    return self._obj_to_id[obj]

  def get_by_id(self, id):
    if id not in self._id_to_obj:
      self._id_to_obj[id] = self._obj_type.from_runner_api(
          self._id_to_proto[id], self._pipeline_context)
    return self._id_to_obj[id]


class PipelineContext(object):
  """For internal use only; no backwards-compatibility guarantees.

  Used for accessing and constructing the referenced objects of a Pipeline.
  """

  _COMPONENT_TYPES = {
      'transforms': pipeline.AppliedPTransform,
      'pcollections': pvalue.PCollection,
      'coders': coders.Coder,
      'windowing_strategies': core.Windowing,
      # TODO: environment
  }

  def __init__(self, context_proto=None):
    for name, cls in self._COMPONENT_TYPES.items():
      setattr(
          self, name, _PipelineContextMap(
              self, cls, getattr(context_proto, name, None)))

  @staticmethod
  def from_runner_api(proto):
    return PipelineContext(proto)

  def to_runner_api(self):
    context_proto = beam_runner_api_pb2.Components()
    for name in self._COMPONENT_TYPES:
      getattr(self, name).populate_map(getattr(context_proto, name))
    return context_proto
