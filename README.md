# slackster

Collection of Slack utilities with Python.

## Development

Easy setup using [Pipenv](https://github.com/pypa/pipenv).

```bash
$ pipenv --python 3.9
$ pipenv install --dev
```

## Usage

You'll need a Slack [User token](https://api.slack.com/authentication/token-types#user) from an installed Slack app. Full permission set required to run all utilities are as follows:

* `channels:read`
* `channels:write`
* `users:read`
* `users:read.email`

Set your slack token in a `.env` file in thee root directory.

```bash
SLACK_TOKEN=xoxp-1111
```

You can then run `slackster` inside a pipenv shell.

```bash
$ pipenv shell
$ pip install -e .
$ slackster diff C12345678 C90123456
```
