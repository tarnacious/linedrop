import sys
from linedrop.main import get_modules, run_fixture
from linedrop.isolation.run_process import run_process
from linedrop.main import strip_statement


def test_sample_tests():
    sys.argv = ["", "test_sample", "test_sample"]
    pattern = "^sample.*$"
    ((success, modules), out, err) = run_process(lambda: get_modules(pattern))

    assert success

    results = run_fixture(modules)

    expected = [("sample.subsample.add", 1, False, "FunctionDef"),
                ("sample.subsample.add", 2, False, "Return"),
                ("sample.factorial", 1, False, "FunctionDef"),
                ("sample.factorial", 3, False, "If"),
                ("sample.factorial", 4, False, "Raise"),
                ("sample.factorial", 6, True, "If"),
                ("sample.factorial", 7, True, "Return"),
                ("sample.factorial", 9, False, "Assign"),
                ("sample.factorial", 13, False, "Return"),
                ("sample.factorial", 11, False, "Assign"),
                ("sample.factorial", 10, False, "For")]

    mapped = [(module, line, result, strip_statement(statement))
              for (module, line, statement, result, _) in results]

    actual = sorted(mapped, key=lambda x: "%s %s" % (x[0], x[1]))
    expected = sorted(expected, key=lambda x: "%s %s" % (x[0], x[1]))
    assert actual == expected
