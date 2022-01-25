#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-wand-engine
# https://github.com/scorphus/thumbor-wand-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2022, Pablo S. Blum de Aguiar <scorphus@gmail.com>

from os.path import join
from thumbor_integration_tests import EngineCase
from thumbor_integration_tests.urls_helpers import single_dataset
from thumbor_integration_tests.urls_helpers import UrlsTester
from tornado.testing import gen_test


class EngineTest(EngineCase):
    engine = "thumbor_wand_engine"

    @gen_test(timeout=60)
    async def test_single_params(self):
        if not self._app:
            return True
        group = list(single_dataset(False))  # FIXME: remove False
        count = len(group)
        tester = UrlsTester(self.http_client)

        print("Requests count: %d" % count)
        for options in group:
            joined_parts = join(*options)
            url = "unsafe/%s" % joined_parts
            await tester.try_url(self.get_url(f"/{url}"))

        tester.report()
