# IRS helper tool

This tool helps you fill in your IRS in CSV files instead of the platform.

This is helpful when you need to fill endless rows in tables with, for instance, your stock market gains.

## Workflow

1. Start your IRS declaration on the gov platform.
2. For each of the Anexo and Quadro that you will need to file, add some data to the fields you will need to fill in (can be dummy data)  
3. Download the XML file from the platform.
4. Convert the XML document to CSV split tables.
5. Fill in the IRS data in the CSV files.
6. Reconvert the files back to XML.
7. Upload the XML to the platform.
8. Continue with your usual process for filing the IRS.

## Installation

### Windows

1. Download and run `xmlcsvtool-setup.exe`.
2. Follow the graphical installer steps.

### Linux

1. Download debian package
wget https://github.com/yourusername/yourrepo/releases/download/v1.0.0/myapp.deb
2. Install
sudo dpkg -i myapp.deb
3. Start using the tool.

## How to build


```
pip install -r requirements.txt
python src/xmlcsvtool/gui.py
```
