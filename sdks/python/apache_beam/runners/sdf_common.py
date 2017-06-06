import logging
import uuid

import apache_beam as beam
from apache_beam import pvalue

from apache_beam.transforms.ptransform import PTransform

from apache_beam.runners.common import DoFnInvoker, _OutputProcessor
from apache_beam.runners.common import DoFnSignature

from apache_beam.transforms.core import ParDo

from apache_beam.runners.common import PTransformMatcher
from apache_beam.pipeline import AppliedPTransform
from apache_beam.utils.windowed_value import WindowedValue


class RestrictionTracker(object):

  def current_restriction(self):
    raise NotImplementedError

  def checkpoint(self):
    raise NotImplementedError

  def check_done(self):
    raise NotImplementedError

  def try_claim(self, element):
    raise NotImplementedError

  def fraction_claimed(self):
    raise NotImplementedError


class SplittableParDoMatcher(PTransformMatcher):

  def match(self, applied_ptransform):
    assert isinstance(applied_ptransform, AppliedPTransform)

    transform = applied_ptransform.transform

    if isinstance(transform, ParDo):
      signature = DoFnSignature(transform.fn)
      return signature.is_splittable_dofn()


class PairWithRestrictionFn(beam.DoFn):

  def __init__(self, do_fn):
    signature = DoFnSignature(do_fn)
    self._invoker = DoFnInvoker.create_invoker(
        signature, process_invocation=False)

  def process(self, element, *args, **kwargs):
    initial_restriction = self._invoker.invoke_initial_restriction(element)
    yield (element, initial_restriction)

class SplitRestrictionFn(beam.DoFn):

  def __init__(self, do_fn):
    signature = DoFnSignature(do_fn)
    self._invoker = DoFnInvoker.create_invoker(
        signature, process_invocation=False)

  def process(self, element_and_restriction, *args, **kwargs):
    element, restriction = element_and_restriction
    restriction_parts = self._invoker.invoke_split(
        element,
        restriction)
    for part in restriction_parts:
      yield element, part

class ExplodeWindowsFn(beam.DoFn):

  def process(self, element, window=beam.DoFn.WindowParam, *args, **kwargs):
    yield element

class RandomUniqueKeyFn(beam.DoFn):

  def process(self, element, *args, **kwargs):
    yield (uuid.uuid4().bytes, element)


class GBKIntoKeyedWorkItems(object):
  pass


class ProcessElements(PTransform):

  def __init__(
      self, do_fn, element_coder, restriction_coder, windowing_strategy,
      side_inputs, main_output_tag, additional_output_tags):
    self._elemenet_coder = element_coder
    self._restriction_coder = restriction_coder
    self._windowing_strategy = windowing_strategy
    self.dofn = do_fn  # this has to be named dofn to match ParDo transform.
    # TODO: use/set/delete other params.

  def expand(self, pcoll):
    # TODO
    return pvalue.PCollection(pcoll.pipeline)
    # return pcoll

  def new_process_fn(self, do_fn):
    return ProcessFn(do_fn, self._elemenet_coder, self._restriction_coder,
                     self._windowing_strategy)


class SplittableParDo(PTransform):

  def __init__(self, ptransform):
    assert isinstance(ptransform, ParDo)
    self._ptransform = ptransform

  def expand(self, input):
    fn = self._ptransform.fn
    signature = DoFnSignature(fn)
    invoker = DoFnInvoker.create_invoker(signature, process_invocation=False)

    restriction_coder = invoker.invoke_restriction_coder()
    keyed_work_items = self._split_into_keyed_workitems(input, fn, restriction_coder)

    return keyed_work_items | ProcessElements(fn, None, None, None, None, None, None)

  def _split_into_keyed_workitems(self, input, fn, restriction_coder):

    logging.error('********* 1')
    logging.error('********* 2')
    keyed_work_items = (input
                        | 'pair' >> ParDo(PairWithRestrictionFn(fn)))
                        # | 'split' >> ParDo(SplitRestrictionFn(fn))
                        # | 'explode' >> ParDo(ExplodeWindowsFn()))
                        # | 'random' >> ParDo(RandomUniqueKeyFn()))
                        # | GBKIntoKeyedWorkItems())

    logging.error('********* 3')

    return keyed_work_items

    # set coder ?


class ProcessFn(beam.DoFn):

  def __init__(self, fn, elemenet_coder, restriction_coder, windowing_strategy):
    self._fn = fn
    self._element_coder = elemenet_coder
    self._restriction_coder = restriction_coder

    # signature = DoFnSignature(fn)
    # # TODO: set process_invocations to True
    #
    # class Processor(object):
    #
    #   def process_outputs(self, a, b):
    #     pass

    # output_processor = _OutputProcessor(None, [], [])

    # self.invoker = DoFnInvoker.create_invoker(signature, output_processor=output_processor, process_invocation=False)
    self._invoker = None

    logging.info('****** creating ProcessFn')

  def start_bundle(self):
    super(ProcessFn, self).start_bundle()

  def process(self, element, *args, **kwargs):
    # TODO: perform per element SDF related logic and invoke self._fn using
    # self._process_element_invoker.

    windowd_value = WindowedValue(element, 100000, None)
    #TODO: Invoke using invoker
    self._invoker.invoke_process(windowd_value, *args, **kwargs)

  def finish_bundle(self):
    super(ProcessFn, self).finish_bundle()

  def set_process_element_invoker(self, invoker):
    self._invoker = invoker

    i = 10


class SplittableProcessElementInvoker(DoFnInvoker):

  def invoke_process_element(self, invoker, element, tracker):
    # Returns a tuple (residual_restriction, future_output_watermark)
    raise NotImplementedError


class OutputAndTimeBoundSplittableProcessElementInvoker(SplittableProcessElementInvoker):

  def __init__(self, process_fn):
    self._process_fn = process_fn

  def invoke_process_element(self, invoker, element, tracker):
    assert isinstance(invoker, DoFnInvoker)
    assert isinstance(tracker, RestrictionTracker)

    invoker.invoke_process(element, tracker)

    tracker.check_done()
