# Trigger External Workflow Action

GitHub Action that triggers a Workflow from another repository using `[repository_dispatch](https://docs.github.com/pt/free-pro-team@latest/actions/reference/events-that-trigger-workflows#repository_dispatch)` event.

## Contributing

PRs welcome! This action is a Docker container, so it is very easy run it locally. Be sure you have all the required inputs represented as envrionment variables. For instance you will need a `INPUT_GITHUB_PAT` to represent the input `github_pat` the action will actually pass. Note the `INPUT_` preffix and the camel case representation.

### Development guide
Be sure you have Python 3.9, otherwise Make won't run as it should. An easy solution is to run `make` commands inside a Docker container.

Clone the repository using Git:
```shell script
git clone git@github.com:PasseiDireto/aws-add-ip-to-security-group-action.git
```

You can build the image as:

```shell script
docker build -t aws-add-ip-to-security-group-action .
```

Have an [env file](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file) ready with all the variables you need, such as:

```shell script
INPUT_AWS_SECURITY_GROUP_IDS=abc123
INPUT_PORT_RANGE=443
INPUT_DESCRIPTION=GHA Rule

```

You can name it `.env` and then run it the freshly built image:

```shell script
docker run --rm --env-file=.env aws-add-ip-to-security-group-action
```

If you want to test the cleanup step (to revoke the freshly created rule), you need to override the `entrypoint` as GitHub Actions does:

```shell script
docker run --rm --entrypoint="/action_workspace/cleanup.sh" --env-file=.env aws-add-ip-to-security-group-action
```

### Before you commit

Be sure all the tests and all the checks are passing:
```sh
pip install -r requirements/all.txt
make # run all checks
make tests # run all tests

```


# Similar actions

[This project](https://github.com/sohelamin/aws-security-group-add-ip-action) is somehow close to this one, but is not very active and does not support port ranges.
