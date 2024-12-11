#!/bin/bash  

# Navigate to the project directory
cd "$(dirname "$0")"

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv  # Create the virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate  # Activate the virtual environment
    echo "Installing requirements..."
    pip install -r requirements.txt  # Install the requirements
else
    echo "Activating existing virtual environment..."
    source venv/bin/activate  # Activate the existing virtual environment
fi

# Run the application
python app.py

# Navigate to the address automatically(somehow not working)
xdg-open http://localhost:5000
