# Online-Video-Document-Reader

## Project Overview

This project is designed to detect Aadhar cards from video frames, extract relevant information such as name, date of birth, Aadhar number, and gender, and convert the detected frames into a PDF document. The system uses OpenCV for image processing, Tesseract for Optical Character Recognition (OCR), and MySQL for data storage.

## Features

- **Face Detection:** Identifies faces in video frames using Haar Cascades for detecting frontal faces, eyes, and mouths.
- **Aadhar Card Detection:** Detects and extracts text from Aadhar cards using Tesseract OCR.
- **Data Extraction:** Extracts details like Name, Date of Birth, Aadhar Number, and Gender from the detected Aadhar card.
- **PDF Conversion:** Converts the detected Aadhar card frames into a PDF document.
  
## Dependencies

Ensure you have the following dependencies installed:

- Python 3.x
- OpenCV
- Tesseract-OCR
- MySQL
- FPDF

You can install the Python dependencies using the following command:

```bash
pip install opencv-python pytesseract mysql-connector-python fpdf
```

## Setup Instructions

1. **Install Tesseract-OCR:**

   Download and install Tesseract-OCR from [here](https://github.com/tesseract-ocr/tesseract). 

   Set the path in your code:

   ```python
   tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
   ```

2. **Set Up Directories:**

   Make sure you have the following directories:

   - `data`: Directory where video frames are stored.
   - `data_face`: Directory where detected face images are stored.
   - `final_img`: Directory where images for PDF conversion are stored.
   - `pdf`: Directory where the final PDF files are saved.

3. **Running the Script:**

   Update the path to the video file in the script:

   ```python
   n = r"D:\python\doc_reader\New folder\4.mp4"
   ```

   Run the script using the following command:

   ```bash
   python your_script.py
   ```

   The script will process the video, extract frames containing Aadhar cards, and save the details in a PDF file.

4. **Database Configuration (Optional):**

   If you want to store extracted details in a MySQL database, configure your MySQL connection in the script:

   ```python
   db = mysql.connector.connect(
       host="localhost",
       user="yourusername",
       password="yourpassword",
       database="yourdatabase"
   )
   ```

## Usage

- **Face Detection:** The script automatically detects faces in video frames and saves them in the `data_face` directory.
- **Aadhar Detection:** It extracts text from the detected Aadhar card and checks for the presence of an Aadhar number.
- **PDF Generation:** After detecting and processing the Aadhar card, the script generates a PDF file with the extracted details.

## Troubleshooting

- **No Aadhar Detected:** Ensure the video quality is good and the Aadhar card is clearly visible in the frames.
- **OCR Accuracy:** If the OCR accuracy is low, consider pre-processing the image (e.g., resizing, grayscale conversion).

## Future Improvements

- Implement multi-threading to process videos faster.
- Add support for other document types.
- Enhance OCR accuracy with advanced image pre-processing techniques
