from pof.utils.generator import AdvancedGenerator, BasicGenerator

r = 100


def test_number_name_generator():
    generator = BasicGenerator.number_name_generator()
    names = []
    for _ in range(r):
        new = next(generator)
        assert new not in names
        names.append(new)


def test_alphabet_generator():
    generator = BasicGenerator.alphabet_generator()
    names = []
    for _ in range(r):
        new = next(generator)
        assert new not in names
        names.append(new)


def test_realistic_generator():
    generator = AdvancedGenerator.realistic_generator()
    names = []
    for _ in range(r):
        new = next(generator)
        assert new not in names
        names.append(new)


def test_multi_generator():
    gen_dict = {
        1: BasicGenerator.alphabet_generator(),
        5: BasicGenerator.number_name_generator(),
    }
    generator = AdvancedGenerator.multi_generator(gen_dict)
    names = []
    for _ in range(r):
        new = next(generator)
        assert new not in names
        names.append(new)
