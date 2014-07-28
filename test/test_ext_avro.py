#!/usr/bin/env python
# encoding: utf-8

"""Test HdfsAvro extension."""

from avro.io import AvroTypeException
from hdfs.ext.avro import *
from helpers import _TestSession
from nose.tools import *


class TestWriter(_TestSession):

  def setup(self):
    super(TestWriter, self).setup()
    if self.client:
      self.writer = AvroWriter(self.client, 'aw.avro')

  def test_write_inferring_schema(self):
    self.writer.records.send({'foo': 'value1'})
    self.writer.records.send({'foo': 'value2', 'bar': 'that'})
    self.writer.records.close()
    data = self.client._open('aw.avro').content
    ok_('foo' in data)
    ok_('value1' in data)
    ok_('value2' in data)
    ok_(not 'that' in data)

  @raises(AvroTypeException)
  def test_invalid_schema(self):
    self.writer.records.send({'foo': 'value1'})
    self.writer.records.send({'bar': 'value2'})
