# -*- coding: utf-8 -*-
import re
import os
import datetime 

from modules.abuse_ch import AbuseCh

class SpyeyetrackerIpBlockList(AbuseCh):
    directory = 'spyeye/ipblocklist/'
    class_name = __class__.__name__
    list_type = 1