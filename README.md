
# DermAI - Skin Lesion Analysis

DermAI is a deep learning-powered application for analyzing skin lesion images, predicting whether a lesion is benign (non-cancerous) or malignant (cancerous) with confidence scores. The intuitive interface makes it accessible for both healthcare professionals and researchers.

---

## 🚀 Features

- 🌄 **Image Upload**: Supports file upload, webcam, or clipboard input.
- 🧠 **Deep Learning Analysis**: Uses a pre-trained DenseNet model for classification.
- 📊 **Confidence Scores**: Displays the probability of predictions.
- 💻 **User-Friendly Interface**: Built with Gradio and styled with Material 3.
- ⚡ **Caching**: Speeds up repeated predictions.
- 🐋 **Containerized with Docker**: Easily deployable anywhere.

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Gradio
- **Containerization**: Docker
- **Styling**: Custom CSS

---

## 📥 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ritikpathania/dermai.git
   cd dermai
   ```

2. Build the Docker image:
   ```bash
   docker build -t dermai .
   ```

3. Run the Docker container:
   ```bash
   docker run -p 8000:8000 -p 7860:7860 dermai
   ```

4. Access the application:
   - Gradio UI: [http://127.0.0.1:7860](http://127.0.0.1:7860)
   - API: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🌍 Environment Variables

| Variable         | Default Value                   | Description                            |
|------------------|---------------------------------|----------------------------------------|
| `DERMAI_API_URL` | `http://127.0.0.1:8000/predict` | API endpoint for predictions           |
| `DERMAI_HOST`    | `127.0.0.1`                     | Host address for the Gradio app        |
| `DERMAI_PORT`    | `7860`                          | Port number for the Gradio app         |
| `SHARE_APP`      | `false`                         | Enable public sharing of the Gradio UI |


---

## 🚦 Usage

1. Upload a skin lesion image.
2. Click the **Analyze** button.
3. View the prediction and confidence score.


---

## 💻 Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the backend:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. Run the Gradio app:
   ```bash
   python gradio_app.py
   ```

---

## 🗃️ File Structure

```
.
├── app/
│   ├── model.py                # Model prediction logic
│   ├── main.py                 # Combined FastAPI and Gradio startup logic
│   └── static/                 
│       ├── styles.css          # Custom CSS for Gradio UI
│       ├── DermAI_logo.png     
│       └── DermAI_favicon.png  
├── gradio_app.py               # Gradio UI logic
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── README.md                   # Project documentation
└── LICENSE                     # License information
```

---

## 📝 Troubleshooting

### Port Conflict
If you encounter:
```
OSError: Cannot find empty port in range: 7860-7860
```
Run the following to kill the process occupying the port:
```bash 
  lsof -t -i:8000 | xargs kill -9
  lsof -t -i:7860 | xargs kill -9
```

### Dependency Issues
If you face issues with protobuf, try:
```bash
  pip install protobuf==3.20.*
```

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## ❤️ Acknowledgments

- Built with ❤️ by Ritik & Trusha.
- Powered by Gradio and FastAPI.
