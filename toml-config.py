import os
import toml


def load_config(file_path) -> dict | None:
    try:
        with open(file_path, 'r') as config_file:
            config_data = toml.load(config_file)
        return config_data
    except Exception as e:
        print(f"Error loading config file: {e}")
        return None


def get_environment_variables(config_data) -> dict:
    if config_data and 'environment_variables' in config_data:
        env_vars = config_data['environment_variables']
        return env_vars
    else:
        print("No environment variables found in the config file.")
        return {}


def set_environment_variables(env_vars) -> None:
    for key, value in env_vars.items():
        os.environ[key] = str(value)


if __name__ == "__main__":
    config_file_path_test = "config.toml"

    # Load config file
    config_data_test = load_config(config_file_path_test)

    # Get environment variables from config
    env_vars_test = get_environment_variables(config_data_test)

    # Set environment variables
    set_environment_variables(env_vars_test)

    # Example: Accessing environment variable
    example_variable_test = os.environ.get('EXAMPLE_VARIABLE')
    print(f"Value of EXAMPLE_VARIABLE: {example_variable_test}")
