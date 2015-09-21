# -*- encoding: utf-8 -*-
import cStringIO
from distlib._backport import tarfile
import os
import tarfile
from flask import jsonify, json
from hepdata_converter.testsuite import insert_data_as_str, insert_path
from hepdata_converter.testsuite.test_writer import WriterTestSuite

import hepdata_converter_ws
import unittest
from hepdata_converter_ws.testsuite import insert_data_as_tar_base64, insert_data_as_tar

__author__ = 'Michał Szostak'


class HepdataConverterWSTestCase(WriterTestSuite):
    def setUp(self):
        super(HepdataConverterWSTestCase, self).setUp()
        hepdata_converter_ws.app.config['TESTING'] = True
        self.app = hepdata_converter_ws.app.test_client()

    def tearDown(self):
        super(HepdataConverterWSTestCase, self).tearDown()

    @insert_data_as_tar_base64('oldhepdata/sample.input')
    @insert_path('oldhepdata/yaml')
    def test_convert(self, hepdata_input_tar, yaml_path):
        r = self.app.get('/convert', data=json.dumps({'input': hepdata_input_tar,
                                                      'options': {'input_format': 'oldhepdata', 'output_format': 'yaml'}}),
                         headers={'content-type': 'application/json'})

        with tarfile.open(mode='r:gz', fileobj=cStringIO.StringIO(r.data)) as tar:
            tar.extractall(path=self.current_tmp)

        self.assertDirsEqual(os.path.join(self.current_tmp, 'hepdata-converter-ws-data'), yaml_path)