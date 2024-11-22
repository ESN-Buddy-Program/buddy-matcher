echo "Setting up Python virtual environment..."

# Create the virtual environment
python3.10 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the requirements, suppressing output for already satisfied packages
pip install -q --no-cache-dir --upgrade -r requirements.txt
