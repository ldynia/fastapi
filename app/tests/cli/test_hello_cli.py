from cli.main import app


def test_hello(runner):
    result = runner.invoke(app, ["hello", "Lukasz"])
    
    assert result.exit_code == 0
    assert "Hello Lukasz" in result.output


def test_hello_with_upper_case_flag(runner):
    result = runner.invoke(app, ["hello", "Lukasz", "--upper-case"])
    
    assert result.exit_code == 0
    assert "Hello LUKASZ" in result.output
