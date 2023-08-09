from tokenize import NAME, OP

from pof.evasion.base import BaseEvasion


class ExecMethodEvasion(BaseEvasion):
    def __init__(self, method="file") -> None:
        # "file" or "memory"
        self.exec_method = method

    def import_tokens(self):
        return [
            (NAME, "import"),
            (NAME, "time"),
        ]

    def check_tokens(self):
        """Verify the execution method.

        When Python code is executed from the console or from the memory
        directly the `__file__` object will be equal to `<stdin>`, if a script
        is meant to be launched with a specific method the evasion can be added.

        Usage:

        This doesn't work (trigger evasion when file is selected)
        ```bash
        echo "print(__file__)" | ./pof.py ... | python
        Exception: evasion check triggered
        ```

        This works (doesn't trigger evasion when file is selected)
        ```bash
        echo "print(__file__)" | ./pof.py ... > bin/a.py & python bin/a.py
        /path/to/file/bin/a.py
        ```

        Todo:
        If running from the console `__file__` doesn't exist, this needs to be
        taken into account !
        """
        equal = "=!"
        if self.exec_method == "file":
            equal = "=="

        return [
            (NAME, "__file__"),
            (OP, equal),
            (NAME, repr("<stdin>")),
        ]
