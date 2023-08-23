import pathlib

import pof


class ExampleObfuscator(pof.BaseObfuscator):
    def constant_obf(self, source):
        tokens = self._get_tokens(source)
        tokens = pof.obfuscator.ConstantsObfuscator().obfuscate_tokens(tokens)
        return self._untokenize(tokens)


def obfuscate_to_file(obf_class, func_name, source):
    out = getattr(obf_class, func_name)(source)
    file_name = func_name + ".py"
    file = pathlib.Path(__file__).parent / "out" / file_name
    with file.open("w") as f:
        f.write(out)


def run_all():
    obf = ExampleObfuscator()

    file = pathlib.Path(__file__).parent / "source.py"
    with file.open() as f:
        source = f.read()

    obfuscate_to_file(obf, "constant_obf", source)


if __name__ == "__main__":
    run_all()
