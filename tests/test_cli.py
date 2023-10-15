import subprocess


# Local testing requires running `pip install -e "."`
def test_cli():
    cmd = subprocess.run(["relic", "-h"], capture_output=True, text=True)
    data = cmd.stdout
    assert "usage: relic [-h]" in data
    exit_status = cmd.returncode
    assert exit_status == 0
