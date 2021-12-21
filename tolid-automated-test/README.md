# ToLID Automated Frontend testing

## Procedure

Setup the fixtures by running:

`tolid-bin/test/setup.sh`

Run the test cases with:

`tolid-bin/test/run.sh`

(This can be run multiple times without re-running the setup script).

When finished iterating the run script, teardown using:

`tolid-bin/test/teardown.sh`

## Test locations

The testcases (for now) have to be in a single file, namely:

`tolid-automated-test/robot/testcases/test.robot`

## Watching the tests live

Once the setup script has finished, navigate to the given URL:

`http://localhost:7902`

You will be prompted for a password, this is currently the default:

`secret`

TODO - change this password to an ENV variable

As the tests run, they will preview in realtime here.

TODO - make this more refined (they currently move almost too quickly to watch).
