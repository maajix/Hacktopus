# Flows
### Version
A version string for keeping track of versions

### Name 
The name of the Flow

### Description
An execution description that can be displayed while running the flow to provide
information on how far the flow has processed

### Tags
Can be set to find flows via a search function

### Variables
Variables that will be passed via the CLI e.g.
```yaml
variables:
  url: "{{url}}"
```
Will allow the use of the CLI argument `--url`

# Container
A container can hold multiple stages and is basically just a wrapper


### Parallel
A parallel option can be specified if all the stages should execute in parallel. 
This automatically means that all stages receive the same `stdin`, and one combined
`stdout` will be produced and passed to the next container.

If parallel is set to false (or absent) a chained execution will be used. This means
the first execution type in the yaml file will receive the stdin, and passes the `stdout` 
to the next stage in that container.

### Stages
Stages hold multiple tasks and information on how to execute them, e.g. `parallel`.

```python
first_stage = {
    'parallel': True,
    'description': 'Execute first_stage',
    'tasks': [
        {
            'alias': 'paramspider:discover',
            'options': [
                {'map': [{'url': 'domain'}]},
                {
                    'custom_func': [
                        {'url_to_domain': 'url'},
                        {'some_func': 'some_param'}
                    ]
                }
            ]
        },
        {'command': 'echo {{url}}'},
        {'flow': 'child_flow'}
    ]
}
```

### Execution type
A stage has an execution type:
- `alias`
- `command`
- `flow`

### Options
We can apply different options onto the execution types `alias` and `command` 

- `map`: Replaces (or maps) an execution types variable ({{value}}) to a given flow variable via the key
- `custom_func`: This will take the custom user functions name as key and the target parameters of which the values supplied via the cli will be passed to the custom function as an argument

# Execution Dict

### Example
```yaml
version: "1.0"
name: "Gather available URLs from Target"
description: "Find URLs, files, directories via crawling, fuzzing, return available non duplicate once"
tags:
  - recon
  - files
  - directories
  - active_scan

variables:
  url: "{{url}}"

stages:
  first_stage:
    parallel: true
    description: "Execute first_stage"
    tasks:
      - alias: "paramspider:discover"
        options:
          - map:
            - url: domain
          - custom_func:
            - url_to_domain: url
            - some_func: some_param
      - command: "echo {{url}}"
      - flow: "child_flow"

  second_stage:
    description: "Execute second_stage"
    tasks:
      - command: "echo second_stage"
```

### Converted to JSON
```python
execution_dict = {
    'version': '1.0',
    'name': 'Gather available URLs from Target',
    'description': 'Find URLs, files, directories via crawling, fuzzing, return available non duplicate once',
    'tags': ['recon', 'files', 'directories', 'active_scan'],
    'variables': {'url': '{{url}}'},
    'container': {
        'first_stage': {
            'parallel': True,
            'description': 'Execute first_stage',
            'tasks': [
                {
                    'alias': 'paramspider:discover',
                    'options': [
                        {'map': [{'url': 'domain'}]},
                        {'custom_func': [{'url_to_domain': 'url'}]}
                    ]
                },
                {'command': 'echo {{url}}'},
                {'flow': 'child_flow'}
            ]
        },
        'second_stage': {
            'description': 'Execute second_stage',
            'tasks': [{'command': 'echo second_stage'}]
        }
    }
}
```