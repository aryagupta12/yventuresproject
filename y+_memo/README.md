# 📊 Investment Memo Generator

Transform company data into professional investment memos with AI-powered insights and document analysis.

## 🚀 New Features

### 📁 Document Upload & Analysis
- **Local File Upload**: Upload PDF, Word, Excel, and text files
- **AI-Powered Extraction**: Automatically extract company information from documents
- **Auto-Population**: Populate form fields with extracted data
- **Multi-File Support**: Process multiple documents simultaneously

### 🔗 Google Drive Integration
- **Direct Access**: Connect to Google Drive and access files directly
- **Bulk Processing**: Download and process multiple files from Google Drive
- **Smart URL Parsing**: Extract file IDs from various Google Drive URL formats
- **Secure Authentication**: OAuth 2.0 authentication with read-only access

## 📋 Supported File Types

| Format | Extension | Use Case |
|--------|-----------|----------|
| **PDF** | `.pdf` | Pitch decks, reports, presentations |
| **Word** | `.docx` | Business plans, executive summaries |
| **Excel** | `.xlsx`, `.xls` | Financial models, data sheets |
| **Text** | `.txt` | Notes, summaries, plain text docs |

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd investment-memo-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API**:
   - Get your API key from [OpenAI](https://platform.openai.com/api-keys)
   - Update the API key in `app.py` (line 9)

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🔧 Google Drive Setup (Optional)

For Google Drive integration, follow these steps:

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Google Drive API

2. **Create OAuth Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Create OAuth 2.0 Client ID (Desktop application)
   - Download as `credentials.json` in project directory

3. **First-time Authentication**:
   - Click "Connect to Google Drive" in the app
   - Follow the authorization URL
   - Complete OAuth flow

For detailed setup instructions, see [google_drive_setup.md](google_drive_setup.md).

## 🎯 How to Use

### Method 1: Upload Documents
1. **Upload Files**: Use the "Upload Files" tab to select documents
2. **Extract Information**: Click "Extract Information from Files"
3. **Review Data**: Check the extracted company information
4. **Auto-populate**: Click "Auto-populate Form" to fill in fields
5. **Generate Memo**: Complete any missing fields and generate memo

### Method 2: Google Drive
1. **Connect**: Click "Connect to Google Drive" and authenticate
2. **Add File IDs**: Paste Google Drive file IDs or URLs
3. **Process**: Click "Download and Process Google Drive Files"
4. **Generate**: Review extracted data and generate memo

### Method 3: Manual Entry
1. **Fill Forms**: Enter company details manually
2. **Use Test Data**: Generate random test data for demonstration
3. **Complete Fields**: Fill in all required information
4. **Generate Memo**: Create professional investment memo

## 📊 Features

### Core Functionality
- **AI-Powered Analysis**: GPT-4 powered memo generation
- **Two-Stage Review**: Initial memo + VC critical analysis
- **Market Analysis**: TAM/SAM/SOM visualization
- **Investment Stage Analysis**: Stage-appropriate metrics and comparisons
- **Financial Health**: Runway analysis and burn rate assessment

### Output Options
- **Professional Memo**: Formatted investment memo with VC analysis
- **Interactive Visualizations**: Market size hierarchy and stage analysis
- **Export Options**: Download as Markdown or PDF
- **Print-Ready**: Optimized for printing with page breaks

### User Experience
- **Dark Mode**: Modern dark theme interface
- **Responsive Design**: Works on desktop and mobile
- **Progress Indicators**: Clear feedback during processing
- **Error Handling**: Graceful handling of missing libraries or API issues

## 🔍 Example Workflow

1. **Start**: Open the app at `http://localhost:8501`
2. **Upload**: Upload `example_company_info.txt` (included in project)
3. **Extract**: Click "Extract Information from Files"
4. **Review**: Check the AI-extracted company data
5. **Populate**: Auto-populate the form fields
6. **Generate**: Create a comprehensive investment memo
7. **Analyze**: View market size and investment stage visualizations
8. **Export**: Download as PDF or Markdown

## 🔒 Security & Privacy

- **Local Processing**: Files are processed locally, not stored permanently
- **API Security**: OpenAI API calls are made securely
- **Google Drive**: Read-only access, OAuth 2.0 authentication
- **No Data Storage**: No company data is permanently stored
- **Credential Safety**: Credentials stored locally, never committed to repo

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **OpenAI**: AI-powered text generation and analysis
- **Google APIs**: Google Drive integration
- **Document Processing**: PyPDF2, python-docx, openpyxl
- **Visualization**: Plotly for interactive charts
- **PDF Generation**: WeasyPrint and pdfkit

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with AI integration
- **File Processing**: Multi-format document parsing
- **API Integration**: OpenAI GPT-4 and Google Drive APIs
- **Visualization**: Interactive Plotly charts

## 🚧 Troubleshooting

### Common Issues

1. **Import Errors**: Run `pip install -r requirements.txt`
2. **Google Drive Connection**: Check `credentials.json` file
3. **PDF Generation**: Install WeasyPrint or pdfkit
4. **File Processing**: Ensure files are not corrupted
5. **API Limits**: Check OpenAI API quotas

### Getting Help

- Check the console for detailed error messages
- Verify all dependencies are installed
- Ensure API keys are properly configured
- Review Google Drive setup guide for authentication issues

## 📈 Future Enhancements

- **Batch Processing**: Process multiple companies simultaneously
- **Template System**: Customizable memo templates
- **Data Sources**: Integration with more data sources (CrunchBase, PitchBook)
- **Collaboration**: Multi-user editing and commenting
- **Analytics**: Usage analytics and insights

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Ready to generate professional investment memos?** 🚀

Visit `http://localhost:8501` and start uploading your company documents! 