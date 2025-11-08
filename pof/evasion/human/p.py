# POF, a free and open source Python obfuscation framework.
# Copyright (C) 2022 - 2025  POF Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


def promt_unix():
    from tkinter import E, S, Tk, ttk  # noqa: PLC0415

    root = Tk()

    clicked = False

    # FIXME (deoktr): Doesn't work ...
    def click():
        root.destroy()

    root.title("System Error")
    root.resizable(0, 0)  # block resize

    root.overrideredirect(1)  # hide window

    root.geometry(
        "+%d+%d"  # noqa: UP031
        % (
            (root.winfo_screenwidth() / 2) - (root.winfo_reqwidth() / 2),
            (root.winfo_screenheight() / 2) - (root.winfo_reqheight() / 2),
        ),
    )

    root.after((5 * 1000), func=root.destroy)

    frm = ttk.Frame(root, padding="50 12 50 12")
    frm.grid()
    ttk.Label(frm, text="System error 0x02333").grid(column=0, row=0)
    ttk.Button(frm, text="Close", command=click).grid(column=0, row=1, sticky=(E, S))
    root.mainloop()
    return clicked


if __name__ == "__main__":
    import sys

    if not promt_unix():
        msg = "did not click"
        sys.stdout(msg)
        sys.exit(1)

    sys.stdout("Hello, world!")
    sys.exit(0)
