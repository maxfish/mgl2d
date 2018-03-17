# Run this script to remove folders and files produced from PyPI build and pytest.
# Returns the project folder to a pre-build state.

echo "Remove PyPI build folders and files..."
rm -rf build/
rm -rf dist/
rm -rf mytestpackage.egg-info/

echo "Remove pytest cache folder..."
rm -rf .cache/

echo "Cleanup complete."

