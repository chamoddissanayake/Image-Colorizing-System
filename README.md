
# Image Colorizing System


This Image Colorizing System is a Flask-based web application that enables users to upload grayscale images and receive colorized versions. Utilizing a deep learning model, the system processes the uploaded images, predicting color channels and transforming them into vibrant, colored outputs. Users can easily access their original and colorized images through dedicated endpoints, making the experience seamless and user-friendly. Perfect for enhancing old photos or artistic projects, this tool breathes new life into monochrome images.
## Run Locally

Install Python 3.10.0


  https://www.python.org/downloads/release/python-3100/

Install Node 21.6.2


  https://nodejs.org/en/blog/release/v21.6.2


Clone the project

```bash
  git clone https://github.com/chamoddissanayake/Image-Colorizing-System.git
```

Go to Frontend Folder

```bash
  Frontend > image-colorizing
```

Install dependencies

```bash
  npm install
```

Start the Frontend

```bash
  npm start
```

Go to Frontend Web App

```bash
  http://localhost:3000/
```

Go to Backend Folder

```bash
  Backend >
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the Backend

```bash
  python app.py
```
## Tech Stack

**Frontend:**

  * React (Typescript)

**Backend Framework:**

  * Flask (Python)

**Image Processing Library:**

  * OpenCV (Python)

**Deep Learning Framework:**

  * OpenCV DNN module

**Model Files:**

  * Caffe (with .prototxt and .caffemodel files)

**Numerical Computation:**

  * NumPy (for array operations)

**Web Technologies:**

  * Flask-CORS (for Cross-Origin Resource Sharing)
  * RESTful API (for request handling)
## Usage/Examples


POST Method

```bash
http://localhost:5009/colorize
```

Request
```javascript
{
  "image_path": "./test_images/lion.jpg"
}
```
Response
```javascript
{
    "colorized_image_path": "output_images\\colorized_b70b5e4019b24e7f923a324d79700980.jpg"
}
```