import tkinter as tk
from tkinter import filedialog, messagebox
from src.xml2csv import xml_to_csv  # Your existing function
from src.csv2xml import csv_to_xml  # Assume you have a reverse function

def convert_xml_to_csv():
    filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if filepath:
        try:
            xml_to_csv(filepath)
            messagebox.showinfo("Success", "CSV saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def convert_csv_to_xml():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        try:
            csv_to_xml(filepath)
            messagebox.showinfo("Success", "XML saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("XML ↔ CSV Converter")

tk.Button(root, text="Convert XML to CSV", command=convert_xml_to_csv, width=30).pack(pady=10)
tk.Button(root, text="Convert CSV to XML", command=convert_csv_to_xml, width=30).pack(pady=10)

root.mainloop()
