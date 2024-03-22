# Makeup Style Transfer

## Overview

Makeup Style Transfer is a project that allows users to experiment with different makeup styles using a web application. Users can upload their makeup-free photos and virtually apply various makeup styles to see how they would look. The system uses AI-based filters for makeup transformation and suggests related beauty products based on the chosen makeup style.

## Features

- **User Interface:** Interactive and user-friendly web application for makeup style experimentation.
- **Face Processing:** Utilizes facial recognition and alignment to ensure accurate makeup application.
- **AI Model (BeautyGan):** Applies makeup styles to user photos for realistic previews.
- **Database Integration:** Stores user records, makeup styles, and product information in a PostgreSQL database.

## Project Structure

```plaintext
Makeup_Style_Transfer
|- model
   49_2700_G.pth
   400_139_G.pth
   checkpoint
   model.data-00000-of-00001
   model.index
   model.meta
   shape_predictor_5_face_landmarks.dat
   shape_predictor_68_face_landmarks.dat
|- fe
   |-.expo
   |-assets
   |-node_modules
   |-src
      |-components
         LoadProgress.tsx
      |-screens
         |-backup
         DashboardScreen.tsx
         ResultScreen.tsx
|- data
   |- images
      |-items
      |-styles
   util.py
   db_info.txt
model.py
app.py
requirements.txt
```

## Pipeline
<img src="pipeline.png" alt="Makeup Style Transfer PipeLine" width="800" height="600">

## System Architecture
<img src="architecture.png" alt="Makeup Style Transfer PipeLine" width="900" height="500">

## BeautyGAN Model Architecture
<img src="modelArchitecture.png" alt="Makeup Style Transfer PipeLine" width="900" height="500">

## Data Preprocessing Procedure
<img src="dataProcessing.png" alt="Makeup Style Transfer PipeLine" width="1000" height="500">

## Database Design Diagram
<img src="Database_Design_Diagram.png" alt="Database Design Diagram" width="800" height="600">

## UI-UX
<img src="product.png" alt="Database Design Diagram" width="450" height="416">

## Installation Guide

## Contributors 
- Nguyen Van Sy Thinh - SE173018
- Le Quoc Viet - SE173577
- Ta Quoc Trung - SE172391
- Truong Tuan Phi - SE161036
- Nguyen Khanh Duy - SE172694
