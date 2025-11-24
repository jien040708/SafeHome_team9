from devices.siren import Siren


def test_activate_only_prints_once(capsys):
    siren = Siren("Front")

    siren.activate()
    siren.activate()

    captured = capsys.readouterr().out
    assert "[SIREN]" in captured
    # Second activation should not produce another line.
    assert captured.count("SIREN") == 1
    assert siren.is_active


def test_deactivate_respects_state(capsys):
    siren = Siren("Garage")

    siren.deactivate()
    assert "[SIREN]" not in capsys.readouterr().out

    siren.activate()
    siren.deactivate()
    captured = capsys.readouterr().out
    assert "Silenced" in captured
    assert not siren.is_active
