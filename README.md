# Overview

Generate markdown documentation for a Github Action

## Installation

:warning: **Requires Python3** :warning:

```bash
# If you're using pip3 to install python3 modules
pip3 install gh-action-docs

# If you're already running pip to install Python3 modules
pip install gh-action-docs
```

## Usage

```bash
$ gh-action-docs

# Enable debug output
gh-action-docs --debug
```

## Prerequisites

It's necessary to have a file called `action.yml` or `action.yaml` and an existing `README.md` with the following open/close tags where you want the content to be inserted

```md
<!--start-gh-action-docs-->
<!--end-gh-action-docs-->
```

## Examples

Given the following Github `action.yml` file

```yaml
name: My Github Action
runs:
  using: docker
  image: Dockerfile
description: Do something fancy
author: YourName <your_email@domain.com>
branding:
  icon: terminal
  color: yellow
inputs:
  first_input:
    description: Very input
    default: "*"
    required: false
  another_input:
    description: Much input needed here
    default: latest
    required: false
  command:
    description: Longer description needed here to explain something difficult
    required: true
  args:
    description: Add args
    required: false
  working_dir:
    description: Where to start
    default: "."
    required: false
outputs:
  status_code:
    description: Returned status code
```

`gh-action-docs` will insert this output directly between the tags

```markdown
<!--start-gh-action-docs-->

## Inputs

| name          | description                                                   | default  | required |
| ------------- | ------------------------------------------------------------- | -------- | -------- |
| first_input   | Very input                                                    | `*`      | False    |
| another_input | Much input needed here                                        | `latest` | False    |
| command       | Longer description needed here to explain something difficult | `N/A`    | True     |
| args          | Add args                                                      | `N/A`    | False    |
| working_dir   | Where to start                                                | `.`      | False    |

## Outputs

| name        | description          |
| ----------- | -------------------- |
| status_code | Returned status code |

<!--end-gh-action-docs-->
```
