# AI Image Generator - IT5007 group porject

Github link: https://github.com/xiboXD/teamProject

Group member:

AUNG MYO MYINT LEO | A0268980L

Ng, yi Ming | A0211008B

Wen Xibo | A0268503A

## List of feature


In this project, we utilize the Python Flask framework for developing the backend service and React for the frontend service. Our backend leverages the image generation API provided by DALLE-3 to assist users in creating images according to their preferences. Meanwhile, the frontend offers a vibrant UI where users can select various styles and easily input prompts. Within our app, users can:

1. Generate images based on the prompts they input.

2. Choose different styles for generating images with distinct visual characteristics.

## Backend Service (Wen Xibo | A0268503A)

### Running Instructions

1. Running environment: Python3 (3.10.9)
2. Dependency installation: Go to your terminal and run `pip install -r requirements.txt`
3. Environment variable: For Mac, go to your terminal and run `export OPENAI_API_KEY='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'` For windows, run `setx OPENAI_API_KEY "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"
`
4. Start backend service: Run `python app.py` in terminal, the the backend service should be run on http://127.0.0.1:5050

## Backend Implementation

1. Architecture:

    The backend architecture involves a Flask application serving as the foundation. Incoming requests are handled via route definitions. Upon receiving a POST request to '/image/create', the backend extracts the prompt from the request body. It enqueues the job to generate an image based on the prompt using a task queue system. The architecture utilizes Redis for task queuing and MongoDB for data storage. Logging is implemented to capture request details.

2. Implementation:

    Task Queue: Utilizes Redis and RQ for asynchronous task processing. Upon receiving an image generation request, the job is enqueued to ensure non-blocking execution.
    Image Generation: Implements image generation functionality based on the provided prompt. The generated image is saved to the 'images' folder with a unique filename based on the timestamp.

    Endpoint Definitions: Defines endpoints '/image/create' for image generation and '/experiments/get-images' for fetching images from the 'images' folder as base64 strings.
    Error Handling: Proper error handling mechanisms are not explicitly defined in the provided code snippet but should be implemented to enhance robustness.

3. Authentication:

    Authentication mechanisms are not explicitly implemented in the provided code snippet. However, integration with third-party authentication services or the implementation of custom authentication using Flask extensions like Flask-Login could enhance security.

4. Setup Automation:

    Setup automation scripts for initializing the backend environment are not provided in the code snippet. However, the Flask application can be easily initialized by executing the script. Further automation using tools like Docker or shell scripts could streamline environment setup.

5. Other Novelties:

    Image Storage: Images are saved to the 'images' folder with unique filenames based on timestamps, facilitating efficient retrieval and management.

    Base64 Encoding: Images fetched from the 'images' folder are encoded as base64 strings before being sent as responses, enabling seamless integration with frontend applications.

6. Documentation:

    Although the code snippet lacks inline comments for detailed documentation, the provided report serves as documentation for the backend implementation. Adding inline comments to the code would enhance readability and maintainability.

7. README Update:

    The README file on the GitHub repository should be updated to include details about the implemented backend features, aiding in the evaluation and understanding of the project.

Overall, the backend implementation fulfills the core requirements by providing image generation functionality, task queuing, and image storage. Further enhancements can be made in terms of error handling, authentication, and documentation to improve the robustness and maintainability of the application.
