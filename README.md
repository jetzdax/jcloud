Jinja Cloud
---

`jcloud` combines cloudformation with jinja2 templates.


# The plan

## Basics

```
$ ls
jcloud.cfg
demo.yaml.jinja2
params.yaml

$ jcloud -i demo.yaml.jinja2 -p params.yaml -e render
```

## Multi envs
```
$ jcloud -i demo.yaml.jinja2 -p common.yaml,dev.yaml -e render

# -or-

$ jcloud -i demo.yaml.jinja2 -p common,dev -e render  # params option will scan for common and common.yaml
```

## Using config
In this setup, `jcloud` loads common.yaml first, then dev.yaml. `jcloud.cfg` is automatically loaded by `jcloud` if
it detects one.
```
$ cat jcloud.cfg
common-params: common.yaml
params-dir: ./envs

$ jcloud -i demo.yaml.jinja2 -p dev -e render
```

Supported config settings:
- common-params
  Parameters file to always include (files included before the `--params` option).
- params-dir
  Where all the paramter files are found.

# Options

## Current options

-i, --input: Input jinja2 file.
-e, --execute: Command to execute (render, create, update, delete)
-p, --params: Parameters files, comma separated, `.yaml` extension optional.
-c, --config: Config file (default: jcloud.cfg)
--params-dir: Directory find the parameters files.
--common-params: Parameters files, comma separated, that will automatically be loaded (more useful in config)

## Future options

--profile: The AWS profile to use.
--region: The AWS region to use.
--use-changeset: Deploy via change set, prompts user.
-v, --verbose: Verbose logging for debugging purposes.
-V, --version: Show version
-y, --yes: Automatically answer 'yes' when prompted.
