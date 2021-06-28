"""Provide methods to build components
"""


class ICommand:
    """Provide methods to build components.
    """

    def execute(self):
        """Execute the module.

        Raises:
            NotImplementedError:
        """
        raise NotImplementedError()

    async def execute_async(self):
        """Execute the module asynchronously.

        Raises:
            NotImplementedError:
        """
        raise NotImplementedError()

    @staticmethod
    def convert_val(val: object):
        """Convert an object to HTTP parameter.

        Args:
          val (object): A value to convert in str.

        Returns:
            str: A string ready for HTTP request.
        """
        if val is None:
            return ""
        if isinstance(val, list) and len(val) == 1:
            if isinstance(val, int):
                return int(val)
            return val[0]

        return val

    @staticmethod
    def http_formatter(val1, val2):
        """Concatenate two objects to create http friendly string.

        Args:
            val1 (object): First value.
            val2 (object): Second value.

        Returns:
            string: A string HTTP ready.
        """
        line = f"{val1},{val2}"
        if len(line) == 1:
            line = ''
        return line
