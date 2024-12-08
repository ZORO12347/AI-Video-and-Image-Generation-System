# AI Video and Image Generation System

Welcome to the **AI Video and Image Generation System**! 🎥✨ This project leverages advanced AI models to generate stunning images and videos based on user prompts. It uses FastAPI as the backend framework and integrates multiple APIs for content generation, including Unsplash and Pexels, to enhance the results.

## 📌 Features

- **Generate Images & Videos**: Input a text prompt, and the system will generate related images and videos.
- **Motivational Content**: Perfect for creating personalized and motivational content.
- **Content Storage**: The system stores generated images and videos for easy retrieval.
- **Real-time Processing**: The app handles multiple requests efficiently and processes content in real-time.

## 🔧 Technologies Used

- **Backend**: FastAPI, Python 3.10+
- **Database**: MySQL for content storage
- **APIs**: 
    - [Unsplash API](https://unsplash.com/developers)
    - [Pexels API](https://www.pexels.com/api/)

## 🚀 Installation

To get the project up and running locally, follow the steps below:

### 1. Clone the Repository
```bash
git clone https://github.com/ZORO12347/AI-Video-and-Image-Generation-System.git
cd AI-Video-and-Image-Generation-System
```

### 2. Set Up the Environment

Make sure you have Python 3.10+ installed. Then, create a virtual environment and install the required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory and add your API keys and database credentials:

```plaintext
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_email_password

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=content_generation

UNSPLASH_API_KEY=your_unsplash_key
PEXELS_API_KEY=your_pexels_key
```

### 4. Set Up the Database

Run the following SQL commands to create the necessary database and table:

```sql
CREATE DATABASE content_generation;
USE content_generation;

CREATE TABLE content_generation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    prompt TEXT NOT NULL,
    video_paths JSON,
    image_paths JSON,
    status VARCHAR(50) DEFAULT 'Processing',
    generated_at DATETIME
);
```

### 5. Running the Application Locally

To run the backend server locally:

```bash
uvicorn fastapi_app:app --reload
```

Visit http://127.0.0.1:8000 in your browser to interact with the system.

## 🌐 Deployment

This application can be deployed on multiple cloud platforms using Docker, AWS Elastic Beanstalk, or Heroku. Here’s how you can deploy:

### Option 1: Docker

1. Build the Docker image:

```bash
docker build -t ai-generation-system .
```

2. Run the Docker container:

```bash
docker run -p 8000:8000 ai-generation-system
```

### Option 2: Heroku

1. Create a new Heroku app:
```bash
heroku create
```

2. Push the code to Heroku:
```bash
git push heroku main
```

## 💻 Contributing

We welcome contributions! If you'd like to improve this project, please follow these steps:

- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes.
- Commit your changes (git commit -am 'Add new feature').
- Push to the branch (git push origin feature-branch).
- Create a pull request.

## 🙏 Acknowledgments

- Unsplash API: For providing beautiful images for content generation.
- Pexels API: For high-quality images for enriching content.
- FastAPI: For creating the backend API with great performance.
- Docker: For making deployment easy and portable.
- Heroku / AWS: For providing cloud platforms for easy deployment.

## 🎉 Conclusion

Congratulations! You have successfully set up the **AI Video and Image Generation System**. 🎬✨ 

This system allows you to generate personalized videos and images from text prompts. With powerful AI models integrated with platforms like Unsplash and Pexels, it offers a seamless user experience for content creation. Whether you are looking to deploy locally or on the cloud, this project is flexible and scalable, offering various deployment options including Docker, Heroku, and AWS Elastic Beanstalk.

Feel free to contribute to this project, report any issues, or suggest enhancements to make this tool even more powerful. Happy coding! 🚀

### 🔗 Links
- [Project GitHub Repository](https://github.com/ZORO12347/AI-Video-and-Image-Generation-System)
- [API Documentation](#)
