# Copyright 2020 Cortex Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import yaml


def update_cli_config(
    cli_config_file_path,
    cortex_environment,
    operator_endpoint,
    aws_access_key_id,
    aws_secret_access_key,
):
    cli_env_config = {
        "name": cortex_environment,
        "operator_endpoint": operator_endpoint,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
    }

    try:
        with open(cli_config_file_path, "r") as f:
            cli_config = yaml.safe_load(f)
            if cli_config is None:
                raise Exception("blank cli config file")
    except:
        cli_config = {"environments": [cli_env_config]}
        with open(cli_config_file_path, "w") as f:
            yaml.dump(cli_config, f, default_flow_style=False)
        return

    if len(cli_config.get("environments", [])) == 0:
        cli_config["environments"] = [cli_env_config]
        with open(cli_config_file_path, "w") as f:
            yaml.dump(cli_config, f, default_flow_style=False)
        return

    replaced = False
    for i, prev_cli_env_config in enumerate(cli_config["environments"]):
        if prev_cli_env_config.get("name") == cortex_environment:
            cli_config["environments"][i] = cli_env_config
            replaced = True
            break

    if not replaced:
        cli_config["environments"].append(cli_env_config)

    with open(cli_config_file_path, "w") as f:
        yaml.dump(cli_config, f, default_flow_style=False)


if __name__ == "__main__":
    update_cli_config(
        cli_config_file_path=sys.argv[1],
        cortex_environment=sys.argv[2],
        operator_endpoint=sys.argv[3],
        aws_access_key_id=sys.argv[4],
        aws_secret_access_key=sys.argv[5],
    )
