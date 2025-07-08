# ai-background-remover

AI-Powered Image Background Removal and Replacement using Computer Vision.


# ✂️ AI-Powered Image Background Remover/Changer

## Project Overview

In the world of digital content, having clean, professional images is essential. The manual process of removing image backgrounds is tedious and time-consuming. **AI-Powered Image Background Remover** is an intuitive web application designed to automate this task using cutting-edge Computer Vision and Machine Learning.

This tool allows users to upload any image, automatically remove its background with AI, and then replace it with a solid color or a new background image, transforming ordinary photos into versatile assets for e-commerce, design, presentations, and more.

## ✨ Features

* **Automatic Background Removal:** Uses advanced AI (the `rembg` library) to intelligently detect and remove image backgrounds with high precision.
* **Custom Background Replacement:** Replace the removed background with:
  * Any solid color via an interactive color picker.
  * Another uploaded image to create a composite.
* **High-Quality Output:** Enhanced processing for sharper edges and smoother results (using `alpha_matting`).
* **Intuitive User Interface:** Built with **Streamlit**, providing a clean, easy-to-use, web-based experience.
* **One-Click Download:** Download the processed image in PNG format with the new background.
* **Automated Workflow:** Streamlines image editing tasks, saving significant time and effort.

## 🚀 Technologies Used

* **Programming Language:** **Python** (primary language for all logic).
* **Artificial Intelligence / Machine Learning Core:**
  * **Computer Vision (CV) Models:** Utilizes pre-trained deep learning models (via the `rembg` library) specifically for image segmentation and background removal.
  * **Generative AI (Image Manipulation):** The core capability for creating new image compositions.
* **Image Processing:** **Pillow** (`PIL`) for handling, manipulating, and composing images.
* **Graphical User Interface (GUI) Framework:**
  * **Streamlit:** For rapid development of interactive, web-based applications.
* **Environment Management:**
  * **Python Virtual Environments (`venv`):** For isolated project dependencies.
  * `requirements.txt`: To manage project dependencies (`pip install -r requirements.txt`).
  * `python-dotenv`: For secure loading of environment variables (like API keys, though not central to `rembg` directly).
* **Model Runtime:** `onnxruntime` (for optimized performance of `rembg`'s underlying models).
* **Version Control:** **GitHub** (with GitHub Desktop integration).
* **Styling:** Custom theming via Streamlit's `.streamlit/config.toml` for a polished look.

## ⚙️ Installation & Setup

Follow these steps to get AI-Powered Image Background Remover up and running on your local machine:

1. **Clone the Repository:**

   ```bash
   git clone [https://github.com/YourGitHubUsername/ai-background-remover.git](https://github.com/YourGitHubUsername/ai-background-remover.git)
   cd ai-background-remover
   ```

   *(Replace `YourGitHubUsername` with your actual GitHub username)*
2. **Create and Activate Virtual Environment:**

   ```bash
   python -m venv .venv
   # On Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *(**Note on `rembg`**: The first time `rembg` runs, it will automatically download its core AI model (e.g., U2Net), which can be around 170MB and may take some time depending on your internet connection. Ensure you have an active internet connection when running the app for the first time.)*
4. **Set up Environment Variables (Optional):**

   * If you plan to integrate other services (like Gemini for future enhancements), create a `.env` file and add your `GEMINI_API_KEY="YOUR_KEY_HERE"`. For basic background removal, this is not strictly needed.
5. **Configure Streamlit Theme:**

   * Ensure you have a folder named `.streamlit` in your project root.
   * Inside `.streamlit`, ensure you have a file named `config.toml` with the following content for a consistent dark theme:
     ```toml
     [theme]
     base="dark"
     primaryColor="#007bff"
     backgroundColor="#1e1e2f"
     secondaryBackgroundColor="#2a2a40"
     textColor="#f0f0f0"
     font="sans serif"
     ```

## 🚀 How to Run

1. Ensure your virtual environment is activated.
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

   This will open the app in your default web browser (usually `http://localhost:8501`).

## 🗺️ Project Structure
