from cli.main import app


def test_goodbye(runner):
    result = runner.invoke(app, ["goodbye", "Lukasz"])
    
    assert result.exit_code == 0
    assert "Goodbye Lukasz" in result.output


def test_goodbye_with_upper_case_flag(runner):
    result = runner.invoke(app, ["goodbye", "Lukasz", "--upper-case"])
    
    assert result.exit_code == 0
    assert "Goodbye LUKASZ" in result.output
