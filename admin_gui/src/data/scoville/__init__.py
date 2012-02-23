#!/usr/bin/python
#-*- coding: utf-8 -*-

from data.Generic import GenericScovilleObject
from data.Instance import InstanceType
o = GenericScovilleObject()
o.getApplication().registerInstanceType(InstanceType("scoville","Scoville"))
o.destroy()