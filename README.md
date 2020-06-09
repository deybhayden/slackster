# slackster

Slack stats and metrics with Python.

## Development

Easy setup using [Pipenv](https://github.com/pypa/pipenv).

```bash
$ pipenv --python 3.8
$ pipenv install --dev
```

## Usage

Set your slack token in a `.env` file in thee root directory.

```bash
SLACK_TOKEN=xoxo-1111
```

You can then run `slackster` inside a pipenv shell.

```bash
$ pipenv shell
$ slackster diff C12345678 C90123456
```
