def promt_unix():
    # TODO (204): add try: except around tkinter imports
    from tkinter import E, S, Tk, ttk

    root = Tk()

    clicked = False

    # FIXME (204): Doesn't work ...
    def click():
        root.destroy()

    root.title("System Error")
    root.resizable(0, 0)  # block resize

    root.overrideredirect(1)  # hide window

    root.geometry(
        "+%d+%d"
        % (
            (root.winfo_screenwidth() / 2) - (root.winfo_reqwidth() / 2),
            (root.winfo_screenheight() / 2) - (root.winfo_reqheight() / 2),
        ),
    )

    root.after(int(5 * 1000), func=root.destroy)

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
