import tkinter as tk
from tkinter import filedialog, messagebox
from src.xmlcsvconvert import xml_to_csv, csv_to_xml, join_tables_to_xml, split_long_to_tables

def convert_xml_to_csv():
    filepath = filedialog.askopenfilename(filetypes=[("XML file", "*.xml")])
    if filepath:
        try:
            xml_to_csv(filepath)
            messagebox.showinfo("Success", "CSV saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def convert_csv_to_xml():
    filepath = filedialog.askopenfilename(filetypes=[("CSV file", "*.csv")])
    if filepath:
        try:
            csv_to_xml(filepath)
            messagebox.showinfo("Success", "XML saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def split_long_to_tables():
    filepath = filedialog.askopenfilename(filetypes=[("CSV file", "*.csv")])
    outfolder = filedialog.askdirectory()
    if filepath and outfolder:
        try:
            #split_long_to_tables(filepath, outfolder)
            messagebox.showinfo("Success", "CSV tables saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def join_tables_to_xml():
    folder = filedialog.askdirectory()
    filepath = filedialog.askopenfilename(filetypes=[("CSV file", "*.csv")])
    if folder:
        try:
            #join_tables_to_xml(folder, filepath)
            messagebox.showinfo("Success", "XML file saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("XML ↔ CSV Converter")

tk.Button(root, text="Convert XML to CSV", command=convert_xml_to_csv, width=30).pack(pady=10)
tk.Button(root, text="Convert CSV to XML", command=convert_csv_to_xml, width=30).pack(pady=10)
tk.Button(root, text="Split CSV file to CSV tables", command=split_long_to_tables, width=30).pack(pady=10)
tk.Button(root, text="Join CSV tables & Convert to XML", command=join_tables_to_xml, width=30).pack(pady=10)

root.mainloop()
