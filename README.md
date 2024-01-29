# Makeup Style Transfer

![Makeup Style Transfer](images/cover_image.jpg)

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
|- checkpoint
|- images
|- front_end
|- data
   |- util.py
   |- info.txt
model.py
app.py

## Contributors
* Nguyen Van Sy Thinh - SE173018
* Le Quoc Viet - SE173577
* Ta Quoc Trung - SE172391
* Truong Tuan Phi - SE161036
* Nguyen Khanh Duy - SE172694
