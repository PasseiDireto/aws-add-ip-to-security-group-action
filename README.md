# Add an IP ingress rule to a AWS Security Group

GitHub Action Adds a new ingress rule on a given AWS security group. After the workflow is finished, the action revokes the new rule. The main
use case for this action is when you need ephemeral access to private resources on AWS (through a private VPC/Subnet) on a GitHub Actions Workflow.


## Usage:
The easiest way to use this action is the following:
```yaml 
on: [push]
jobs:
  job:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_KEY }}
        aws-region: ${{ secrets.AWS_DEFAULT_REGION }}
    - uses: passeidireto/aws-add-ip-to-security-group-action@v1 # could be @main
      with:
        aws_security_group_ids: ${{ secrets.AWS_DEV_TOOLS_SECURITY_GROUP_ID }}
        port_range: '80-83'

```

The dash `-` notation is used to mean a range of IP addresses. The [aws-configure-credentials](https://github.com/aws-actions/configure-aws-credentials) action is the preferred way to 
setup this action, since you can use several features like self-hosted roles, AssumeRole, and much more. You can also configure it
using env variables such as:

```yaml
job:
    - uses: passeidireto/aws-add-ip-to-security-group-action@v1 # could be @main
      with:
        aws_security_group_ids: ${{ secrets.AWS_DEV_TOOLS_SECURITY_GROUP_ID }}
        port_range: '443'
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_KEY }}
        AWS_DEFAULT_REGION:  ${{secrets.AWS_DEFAULT_REGION}}
```

## Roadmap
Some neat features are already mapped and waiting for PRs or further use cases we reach:

- Multiple security groups
- Multiple port ranges
- UDP rules
- Option to not remove the ingress rule once the workflow is finished
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
