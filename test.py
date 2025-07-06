import unittest
import tempfile
import os
import toml
from bump_setup.main import bump_version

class TestBumpVersion(unittest.TestCase):

    def setUp(self):
        """Setup the test environment."""
        # Mock a valid setup.py content for testing
        self.valid_setup_py = """
from setuptools import setup

setup(
    name="example_package",
    version="1.0.0",
    packages=["example_package"],
    install_requires=[],
)
        """

        # Mock a valid setup.py content with 'import setuptools' and 'setuptools.setup'
        self.setup_with_import_setuptools = """
import setuptools
setuptools.setup(
    name="example_package",
    version="1.0.0",
    packages=["example_package"],
    install_requires=[],
)
        """

        # Mock a pyproject.toml content for testing
        self.valid_pyproject_toml = """
[project]
name = "example_package"
version = "1.0.0"
dependencies = []
        """

    def create_temp_setup_py(self, content, temp_dir):
        """Create a temporary setup.py file in the given directory."""
        file_path = os.path.join(temp_dir, 'setup.py')
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path

    def create_temp_pyproject_toml(self, content, temp_dir):
        """Create a temporary pyproject.toml file in the given directory."""
        file_path = os.path.join(temp_dir, 'pyproject.toml')
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path

    def test_bump_major_version_in_setup_py(self):
        """Test the version bumping for major version in setup.py."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = self.create_temp_setup_py(self.valid_setup_py, temp_dir)
            bump_version(file_path, 'major')  # Using your bump_version logic here

            with open(file_path, 'r') as f:
                updated_code = f.read()

            # Assert the version has been bumped to 2.0.0
            self.assertIn("version='2.0.0'", updated_code)

    def test_bump_minor_version_in_setup_py(self):
        """Test the version bumping for minor version in setup.py."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = self.create_temp_setup_py(self.valid_setup_py, temp_dir)
            bump_version(file_path, 'minor')  # Using your bump_version logic here

            with open(file_path, 'r') as f:
                updated_code = f.read()

            # Assert the version has been bumped to 1.1.0
            self.assertIn("version='1.1.0'", updated_code)

    def test_bump_patch_version_in_setup_py(self):
        """Test the version bumping for patch version in setup.py."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = self.create_temp_setup_py(self.valid_setup_py, temp_dir)
            bump_version(file_path, 'patch')  # Using your bump_version logic here

            with open(file_path, 'r') as f:
                updated_code = f.read()

            # Assert the version has been bumped to 1.0.1
            self.assertIn("version='1.0.1'", updated_code)

    def test_bump_major_version_with_import_setuptools(self):
        """Test the version bumping for major version with 'import setuptools' in setup.py."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = self.create_temp_setup_py(self.setup_with_import_setuptools, temp_dir)
            bump_version(file_path, 'major')  # Using your bump_version logic here

            with open(file_path, 'r') as f:
                updated_code = f.read()

            # Assert the version has been bumped to 2.0.0
            self.assertIn("version='2.0.0'", updated_code)

    def test_bump_version_in_pyproject_toml(self):
        """Test version bumping in pyproject.toml."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = self.create_temp_pyproject_toml(self.valid_pyproject_toml, temp_dir)
            bump_version(file_path, 'major')  # Using your bump_version logic here

            with open(file_path, 'r') as f:
                updated_toml = f.read()

            # Assert the version has been bumped to 2.0.0
            toml_data = toml.loads(updated_toml)
            self.assertEqual(toml_data['project']['version'], "2.0.0")

    def test_bump_minor_version_in_pyproject_toml(self):
        """Test version bumping in pyproject.toml for minor version."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = self.create_temp_pyproject_toml(self.valid_pyproject_toml, temp_dir)
            bump_version(file_path, 'minor')  # Using your bump_version logic here

            with open(file_path, 'r') as f:
                updated_toml = f.read()

            # Assert the version has been bumped to 1.1.0
            toml_data = toml.loads(updated_toml)
            self.assertEqual(toml_data['project']['version'], "1.1.0")

    def test_bump_patch_version_in_pyproject_toml(self):
        """Test version bumping in pyproject.toml for patch version."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = self.create_temp_pyproject_toml(self.valid_pyproject_toml, temp_dir)
            bump_version(file_path, 'patch')  # Using your bump_version logic here

            with open(file_path, 'r') as f:
                updated_toml = f.read()

            # Assert the version has been bumped to 1.0.1
            toml_data = toml.loads(updated_toml)
            self.assertEqual(toml_data['project']['version'], "1.0.1")

    def test_invalid_version_type(self):
        """Test an invalid version type argument."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = self.create_temp_setup_py(self.valid_setup_py, temp_dir)

            with self.assertRaises(ValueError):  # Changed to ValueError
                bump_version(file_path, 'invalid')  # Should raise ValueError for invalid version type

    def test_version_not_found_in_setup_py(self):
        """Test that an error is raised when no version is found in setup.py."""
        code_without_version = """
from setuptools import setup
setup(
    name="example_package",
    packages=["example_package"],
    install_requires=[],
)
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary setup.py file
            file_path = self.create_temp_setup_py(code_without_version, temp_dir)

            with self.assertRaises(Exception):
                bump_version(file_path, 'patch')

if __name__ == "__main__":
    unittest.main()
