"""Prevent creating new attributes for existing objects
The new attributes created in Python won't be visible for podio IO
therefore preventing the addition of new attributes for podio objects
might be desirable and help detecting mis-assignments"""

from .utils.pythonizer import Pythonizer


class FreezeClassPythonizer(Pythonizer):
    """Prevent setting new attributes"""

    @classmethod
    def priority(cls):
        """
        This most likely should be the last pythonization loaded.
        Otherwise it may interfere with creating attributes during other pythonizations.

        Returns:
            int: Priority.
        """
        return 99

    @classmethod
    def filter(cls, class_, name):
        """
        Filter passing all the classes

        Args:
            class_ (type): Class object.
            name (str): Name of the class.

        Returns:
            bool: True.
        """
        return True

    @classmethod
    def modify(cls, class_, name):
        """Raise an `AttributeError` if new attribute would be set

        Args:
            class_ (type): Class object.
            name (str): Name of the class.
        """

        def freeze_setattr(self, attr, val):
            object_type = type(self)
            if attr not in object_type.__dict__:
                raise AttributeError(f"'{object_type}' object has no attribute '{attr}'")
            old_setattr(self, attr, val)

        old_setattr = class_.__setattr__
        class_.__setattr__ = freeze_setattr
