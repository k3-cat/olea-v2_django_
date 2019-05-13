# tools

Do not move or rename any files, since paths are hard coded.

## setup_env.ps1

It runs with the `--system-site-packages` option, so you can simply switch to this virtual environment and enjoy the `pylint` (or other packages like `yapf`, `pep8`, etc.) from global environment.

In the PROD, switching the `include-system-site-packages` option in `pyvenv.cfg` file to `false` is highly recommended -- thus, a clean and standardized environment can be guaranteed.
