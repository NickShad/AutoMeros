# AutoMeros
AI segmentation model for car details detection

## Installation guide

### Project Overview
This Streamlit-based web application allows users to upload car images, performs segmentation, and displays:

  The original image

  The segmented image

  Individual car part segments

### System Requirements
  OS: Ubuntu 24.04 or Windows 10/11 (64-bit)

  RAM: 8GB+ recommended

  Storage: 10GB+ free space

### Installation Instructions

#### For Ubuntu 24.04
```bash
# Update system and install dependencies
sudo apt update
sudo apt install python3.12-pip python3.12-venv libgl1-mesa-glx git -y

# Clone repository
git clone https://github.com/NickShad/AutoMeros.git
cd AutoMeros

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### For Windows 10/11 (PowerShell)
```powershell
# Launch PowerShell as Administrator:
# 1. Press Win+X
# 2. Select "Windows PowerShell (Admin)"
# 3. Confirm UAC prompt

# Set execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Chocolatey package manager
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python and Git
choco install python3.12 git -y

# Clone repository (in regular PowerShell session)
git clone https://github.com/NickShad/AutoMeros.git
cd AutoMeros

# Create virtual environment
python3 -m venv venv

# Activate environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the application
```bash
# For Ubuntu:
source venv/bin/activate
cd frontend
streamlit run app.py

# For Windows:
.\venv\Scripts\Activate.ps1
cd frontend
streamlit run app.py
```
