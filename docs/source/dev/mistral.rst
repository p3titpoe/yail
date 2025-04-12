Logger Manager Class
====================

The LoggerManager class is an overclass that manages loggers. It requires a MasterLoggerCache as a Registry and a Baselogger object.

.. versionadded:: 1.0


.. csv-table:: **Protected Attributes**
   :header: "What", "Type", "Desc"
   :widths: 20, 20, 80

   "**_root_cache**","MasterLoggerCache","The cache object for the root logger."
   "**_root_logger**","BaseLogger","The root logger instance."
   "**_application_name**","str","Application name, default value is yail5"
   "**_solo_on**", "bool","Indicates whether solo mode is enabled. Default value is False."
   "**_solo_list**","list","A list of logger names in solo mode."
   "**_mute_on**","bool","Indicates whether muting is currently active. Default value is False."
   "**_muted_list**","list","A list of logger names that are currently muted."


Methods:

.. py:function:: __init__(self)
   :annotation: Initializes the LoggerManager instance and sets up the root logger.


`_logger_actions` (self, action_list)
    :annotation: Mutes or unmutes loggers based on a given action list.
`mute_all_or_sip` (self)
    :annotation: Mutes all loggers, or overrides previous solo state for a specific logger (SOLO IN PLACE).
`solo_logger` (self, name=None)
    :annotation: Sets the solo state for all loggers, or only for the specified logger.
`solo_off` (self, name=None)
    :annotation: Removes the solo state from all loggers, or only from the specified logger.
`mute_logger `(self, name)
    :annotation: Mutes a specific logger, or all loggers if no argument is provided.
`mute_off` (self, name=None)
    :annotation: Offs the Mute Bus or takes a Logger out of the bus.
`rootcache` (self)
    :annotation: Returns the root cache object.
`rootlogger` (self)
    :annotation: Returns the root logger object.