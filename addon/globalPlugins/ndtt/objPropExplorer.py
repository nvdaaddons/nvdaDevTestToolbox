# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2019 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import globalPluginHandler
import ui
import api
import controlTypes

def _createDicControlTypesConstantes(prefix):
	dic = {}
	attributes = dir(controlTypes)
	for name in attributes:
		if name.startswith(prefix):
			dic[getattr(controlTypes, name)] = name[len(prefix):]
	#from logHandler import log
	#log.debug(dic)
	return dic
_DIC_ROLES = _createDicControlTypesConstantes('ROLE_')
_DIC_STATES = _createDicControlTypesConstantes('STATE_')

def getStateInfo(o):
	info = sorted(o.states)
	names = ', '.join([_DIC_STATES[i] for i in info])
	info = '{} ({})'.format(names, info)
	return info
	
def getLocationInfo(o):
	info = ', '.join('{}: {}'.format(i, getattr(o.location, i)) for i in ['left', 'top', 'width', 'height'])
	return info
			
	

	
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	
	_INFO_TYPES = ['name',
		('role', lambda o: '{} ({})'.format(_DIC_ROLES[o.role], o.role)),
		('states', getStateInfo),
		'value',
		'windowClassName',
		'windowControlID',
		'windowHandle',
		('location', getLocationInfo),
		('pythonClass', lambda o: str(type(o))),
		('pythonClassMRO', lambda o: str(type(o).mro()).replace('>, <', ',\r\n').replace('[<', '\r\n', 1).replace('>]',''))]
	
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.index = 0
		
	def script_announceObjectInfo(self, gesture):
		self.announceCurrentInfo()
	# Translators: Input help mode message for a command of the object property explorer.
	script_announceObjectInfo.__doc__=_("Announce current object property.")
	script_announceObjectInfo.category=_("WindowsUtil")
		
	def script_nextObjectInfo(self, gesture):
		self.index = (self.index + 1) % len(self._INFO_TYPES)
		self.announceCurrentInfo()
	# Translators: Input help mode message for a command of the object property explorer.
	script_nextObjectInfo.__doc__=_("Select next object property and announce it.")
	script_nextObjectInfo.category=_("WindowsUtil")
		
	def script_priorObjectInfo(self, gesture):
		self.index = (self.index - 1) % len(self._INFO_TYPES)
		self.announceCurrentInfo()
	# Translators: Input help mode message for a command of the object property explorer.
	script_priorObjectInfo.__doc__=_("Select prior object property and announce it.")
	script_priorObjectInfo.category=_("WindowsUtil")	
	
	def announceCurrentInfo(self):
		infoType = self._INFO_TYPES[self.index]
		nav = api.getNavigatorObject()
		if isinstance(infoType, tuple):
			infoType, fun = infoType
		else:
			fun = lambda o: getattr(o, infoType)
		try:
			info = fun(nav)
		except:
			info = 'Unavailable information'
		ui.message('{}: {}'.format(infoType, info))
		
	__gestures = {
		"kb:NVDA+rightArrow": "announceObjectInfo",
		"kb:NVDA+shift+leftArrow": "priorObjectInfo",
		"kb:NVDA+shift+rightArrow": "nextObjectInfo",
		}