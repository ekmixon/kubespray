import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_run(host):
    gvisorruntime = "/usr/local/bin/runsc"
    with host.sudo():
        cmd = host.command(f"{gvisorruntime} --version")
    assert cmd.rc == 0
    assert "runsc version" in cmd.stdout


def test_run_pod(host):
    runtime = "runsc"

    run_command = f"/usr/local/bin/crictl run --with-pull --runtime {runtime} /tmp/container.json /tmp/sandbox.json"

    with host.sudo():
        cmd = host.command(run_command)
    assert cmd.rc == 0

    with host.sudo():
      log_f = host.file("/tmp/gvisor1.0.log")

      assert log_f.exists
      assert b"Hello from Docker!" in log_f.content
