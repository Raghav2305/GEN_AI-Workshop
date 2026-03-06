# Instructions to Run the Chatbot

To run this chatbot application, please follow these steps:

1.  **Set your Gemini API Key**:
    *   Ensure your Google Gemini API key is set as an environment variable named `GEMINI_API_KEY`.
    *   **Windows (Command Prompt)**:
        ```bash
        set GEMINI_API_KEY=YOUR_API_KEY_HERE
        ```
    *   **Windows (PowerShell)**:
        ```powershell
        $env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```
    *   **Linux/macOS**:
        ```bash
        export GEMINI_API_KEY=YOUR_API_KEY_HERE
        ```
    *   Replace `YOUR_API_KEY_HERE` with your actual Gemini API key. For persistent setting, add this line to your shell's profile file (e.g., `.bashrc`, `.zshrc`, `.profile`).

2.  **Navigate to the `Code2` directory**:
    ```bash
    cd Code2
    ```

3.  **Run the Flask application**:
    ```bash
    python app.py
    ```
    You should see output similar to this, indicating the server is running:
    ```
     * Serving Flask app 'app'
     * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
    ```

4.  **Open your web browser**:
    *   Go to `http://127.0.0.1:5000` to access the chatbot interface.

You can now interact with your Gemini-powered chatbot!