#!/bin/bash

# Port for Wokwi MicroPython
PORT="rfc2217://localhost:4000"

# Files to copy
FILES=("main.py" "mpu6050.py")

# Loop through files and upload them
for file in "${FILES[@]}"; do
    echo "Uploading $file..."
    mpremote connect port:$PORT fs cp "$file" ":$file"
done

mpremote connect port:$PORT ls

echo "All files uploaded successfully!"