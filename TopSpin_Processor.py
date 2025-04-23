"""
How to use?

1) Extract the .txt file from TopSpin that contains the spectrum intensities.
2) Run this file.
3) Choose the .txt file generated from TopSpin
4) The program will save a .txt file that contains the ppm values and the intensities.
5) This file can be opened directly in Origin.
"""

import os
import tkinter as tk
from tkinter import filedialog

def process_txt_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Extract parameters from the comment lines
    left, right, size = None, None, None
    intensities = []

    for line in lines:
        if line.startswith('#'):
            if "LEFT" in line:
                left = float(line.split('=')[1].split()[0])
            if "RIGHT" in line:
                right = float(line.split('=')[2].split()[0])
            if "SIZE" in line:
                size = int(line.split('=')[1].split()[0])
        else:
            # Parse intensities
            intensities.extend(map(float, line.split()))

    if None in (left, right, size):
        raise ValueError("LEFT, RIGHT, or SIZE parameter is missing in the input file.")

    # Calculate ppm values
    ppm_values = [left - (abs(right) - abs(left)) / size * i for i in range(len(intensities))]

    # Write output to a new file
    with open(output_file, 'w') as file:
        for ppm, intensity in zip(ppm_values, intensities):
            file.write(f"{ppm:.6f} {intensity:.6f}\n")

if __name__ == "__main__":
    # Create a file dialog to choose the input file
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    input_filename = filedialog.askopenfilename(
        title="Select Input Text File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if input_filename:
        output_filename = os.path.splitext(input_filename)[0] + "_processed.txt"
        try:
            process_txt_file(input_filename, output_filename)
            print(f"Processed file saved to {output_filename}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No file selected.")
