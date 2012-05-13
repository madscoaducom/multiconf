#!/usr/bin/python

# Copyright 2012 Lars Hupfeldt Nielsen, Hupfeldt IT
# This code is free for anybody to use

import sys
import os.path
from os.path import join as jp
here = os.path.dirname(__file__)
sys.path.append(jp(here, '../..'))

import unittest
from oktest import ok, test, fail, todo, dummy
from utils import lazy, config_error, lineno

from multiconf.multiconf import ConfigRoot, ConfigItem, ConfigException, required
from multiconf.envs import Env, EnvGroup

dev2ct = Env('dev2CT')
dev2st = Env('dev2ST')
g_dev2 = EnvGroup('g_dev2', dev2ct, dev2st)

dev3ct = Env('dev3CT')
dev3st = Env('dev3ST')
g_dev3 = EnvGroup('g_dev3', dev3ct, dev3st)

g_dev = EnvGroup('g_dev', g_dev2, g_dev3)

pp = Env('pp')
prod = Env('prod')
g_prod = EnvGroup('g_prod', pp, prod)

valid_envs = EnvGroup('g_all', g_dev, g_prod)

class DecoratorsTest(unittest.TestCase):
    @test("required attributes - configroot")
    def _a(self):
        @required('anattr, anotherattr')
        class root(ConfigRoot):
            pass
                
        with root(prod, [prod]) as cr:
            cr.anattr(prod=1)
            cr.anotherattr(prod=2)
        ok (cr.anattr) == 1
        ok (cr.anotherattr) == 2

    @test("required attributes - configitem")
    def _a(self):
        class root(ConfigRoot):
            pass

        @required('a, b')
        class item(ConfigItem):
            pass
                
        with root(prod, [prod]) as cr:
            with item(False) as ii:
                ii.a(prod=1)
                ii.b(prod=2)
            
        ok (cr.item.a) == 1
        ok (cr.item.b) == 2

if __name__ == '__main__':
    unittest.main()