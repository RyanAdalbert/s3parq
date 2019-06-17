# postgres_toggle.py

### What is it?
By default, CORE's SessionHelper will use the in-memory SQLite `configuration_mocker` in the dev environment. This behavior can be overridden with the variable `FORCE_POSTGRES` in `config/core_project.yaml`. If FORCE_POSTGRES is true, the session helper will query postgres regardless of environment. Rather than adjusting this value directly, you can import this module and call its functions to set it for you in any larger context.

### How do I use it?
postgres_toggle has two functions, `postgres()` and `cmock()`. The former sets `FORCE_POSTGRES` to true, and the latter sets `FORCE_POSTGRES` to false. Neither take any arguments. In the event that `FORCE_POSTGRES` is already set to the value of the method, the config file remains unchanged and the module will log that it is already set to True or False.