<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
</head>
<body>
<h1 style="color:#007bff;">AutoMeros 🚗</h1>
<p><strong>AutoMeros</strong> — технология компьютерной сегментации деталей автомобилей от компании <a href="https://t.me/dataset_rolls"><strong>DataSet роллов</strong></a>. AutoMeros позволяет <em>автоматически</em> выделять и <em>классифицировать</em> элементы автомобиля на фотографиях, формируя отчёты о расположении и комплектации деталей.</p>
<div class="container">
    <img src="automeros.jpg" align="left" alt="Пример работы AutoMeros" width="300">
    <div class="text-side" align="right">
        <h2>Основные возможности 🔥:</h2>
        <ul>
            <li>🖼️ Высокоэффективная сегментация автомобильных деталей по фотографиям.</li>
            <li>📝 Формирование отчетов с указанием местоположения и типа каждой детали.</li>
            <li>🛠️ Применение в автосервисах, центрах диагностики, автопроизводителях (например, АвтоВАЗ) и страховых компаниях.</li>
        </ul>
        <p>Использование <em>AutoMeros</em> помогает <strong>снизить нагрузку</strong> на персонал, <strong>повысить точность</strong> диагностики.</p>
    </div>
</div>
<footer>Made with ❤️ by DataSet Rolls</footer>
</body>
</html>

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
# 1. Install python3.12+ and git
# 2. Launch PowerShell as Administrator. Press Win+X

# Set execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Clone repository (in regular PowerShell session)
git clone https://github.com/NickShad/AutoMeros.git
cd AutoMeros

# Create virtual environment
python -m venv venv

# Activate environment
.\venv\Scripts\activate

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
.\venv\Scripts\activate
cd frontend
streamlit run app.py
```
