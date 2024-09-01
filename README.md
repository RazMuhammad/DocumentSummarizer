# PDF Summarizer with Technical Definitions

## Overview

This project is a Python application that summarizes the content of a PDF file and provides definitions for technical terms found within the text. The application uses advanced natural language processing techniques to generate concise summaries and clear definitions, making it a valuable tool for students, researchers, and professionals who need to quickly grasp the key points of technical documents.

## Features

- **PDF Text Extraction**: Extracts text from uploaded PDF files using PyMuPDF.
- **Text Segmentation**: Segments the extracted text into topics for more focused summarization.
- **Summarization**: Utilizes a language model to generate summaries and define technical terms.
- **Technical Definitions**: Provides clear and contextually relevant definitions for technical terms, especially those related to AI and machine learning.
- **PDF Output**: Generates a new PDF file with the summarized content and technical definitions.
- **Streamlit Interface**: Offers a user-friendly web interface for uploading PDFs and downloading the summarized output.

## How It Works

1. **Upload PDF**: Users upload a PDF file through the Streamlit interface.
2. **Text Extraction**: The application extracts text from the PDF using PyMuPDF.
3. **Text Segmentation**: The extracted text is segmented into topics based on double newlines.
4. **Summarization**: Each topic is summarized using a language model, and technical terms are identified.
5. **Definition Generation**: Technical terms are defined using the same language model, providing contextually relevant definitions.
6. **PDF Generation**: The summarized text and definitions are formatted into a new PDF file using ReportLab.
7. **Download Output**: Users can download the generated PDF file containing the summaries and definitions.

## Installation

To run this application locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/RazMuhammad/DocumentSummarizer
   cd DocumentSummarizer
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Dependencies

- `PyMuPDF` for PDF text extraction.
- `NLTK` for natural language processing.
- `ReportLab` for generating PDF output.
- `Streamlit` for the web interface.
- `Groq` for accessing the language model.

## Usage

1. **Launch the Application**: Run the application using the command `streamlit run app.py`.
2. **Upload a PDF**: Use the file uploader in the Streamlit interface to upload a PDF file.
3. **Process the PDF**: The application will process the PDF, generate summaries, and provide definitions for technical terms.
4. **Download the Output**: Once processing is complete, download the generated PDF file containing the summaries and definitions.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact [raz9128256@gmail.com](mailto:your-email@example.com).
