import toml
import re
import sys

def bump_version(file_path, version_type):
    """
    Bumps the version in a `setup.py` or `pyproject.toml` file based on the version type.
    :param file_path: Path to the setup.py or pyproject.toml file
    :param version_type: Type of version bump ('major', 'minor', 'patch')
    """
    if file_path.endswith("pyproject.toml"):
        # Handle pyproject.toml
        print(f"Found pyproject.toml. Bumping version...")

        try:
            with open(file_path, 'r') as f:
                toml_data = toml.load(f)
        except Exception as e:
            print(f"Error reading pyproject.toml: {e}")
            sys.exit(1)

        # Extract version from the `[project]` section
        if 'project' in toml_data and 'version' in toml_data['project']:
            version = toml_data['project']['version']
        else:
            print("Error: No version found in pyproject.toml under [project]")
            sys.exit(1)

        # Use regex to bump version
        version_regex = r'(\d+)\.(\d+)\.(\d+)'
        match = re.match(version_regex, version)
        if not match:
            print(f"Could not extract version from {file_path}")
            sys.exit(1)

        major, minor, patch = map(int, match.groups())

        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        elif version_type == "patch":
            patch += 1
        else:
            print(f"Invalid version type: {version_type}")
            sys.exit(1)

        new_version = f'{major}.{minor}.{patch}'
        print(f"Bumping version to {new_version} in pyproject.toml")

        # Update the version in the toml data
        toml_data['project']['version'] = new_version

        # Write the updated toml data back
        try:
            with open(file_path, 'w') as f:
                toml.dump(toml_data, f)
        except Exception as e:
            print(f"Error writing pyproject.toml: {e}")
            sys.exit(1)

        print(f"Version bumped to {new_version} in pyproject.toml")

    elif file_path.endswith("setup.py"):
        # Handle setup.py
        print(f"Found setup.py. Bumping version...")

        try:
            with open(file_path, 'r') as f:
                code = f.read()
        except Exception as e:
            print(f"Error reading setup.py: {e}")
            sys.exit(1)

        # Look for the version string in setup.py using regex
        version_regex = r"version\s*=\s*['\"](\d+\.\d+\.\d+)['\"]"
        match = re.search(version_regex, code)

        if not match:
            print(f"Could not find version in {file_path}")
            sys.exit(1)

        version = match.group(1)
        major, minor, patch = map(int, version.split('.'))

        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        elif version_type == "patch":
            patch += 1
        else:
            print(f"Invalid version type: {version_type}")
            sys.exit(1)

        new_version = f'{major}.{minor}.{patch}'
        print(f"Bumping version to {new_version} in setup.py")

        # Update the version in setup.py
        updated_code = re.sub(version_regex, f"version = '{new_version}'", code)

        try:
            with open(file_path, 'w') as f:
                f.write(updated_code)
        except Exception as e:
            print(f"Error writing setup.py: {e}")
            sys.exit(1)

        print(f"Version bumped to {new_version} in setup.py")

    else:
        print(f"Unsupported file type: {file_path}")
        sys.exit(1)
