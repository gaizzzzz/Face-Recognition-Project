# Project Overview
- First of all, we will use `Face Detection` or the ability to find faces in images.
- Then, we'll implement `Face Recognition`.
- Finally, we will end with 3 primary tasks: train-validate-test.

When **training**, our face recognizer will need to open many image files. To accomplish this, you'll set up a directory structure:
- training/
- validation/
- output/

We can put images directly into *validation/*. For *training/*, we should have images separated by subjects into directories with the subject's name.

**Note**: The strategy works well for training on images that contain a single face.

We will build an app like a command-line interface so that users can interact with app.

------------------------------------------------------------------------------------------------------------------
# Prerequisties
## Step 1: Prepare Environment and Data

- Make sure your computer have cmake and gcc.
- Create *requirements.txt* file.
- Download dataset: https://www.kaggle.com/datasets/adg1822/7-celebrity-images/code

The structure of this project:
face_recognizer/  
│  
├── output/  
│  
├── training/  
│   └── ben_affleck/  
│       ├── img_1.jpg  
│       └── img_2.png  
│  
├── validation/  
│   ├── ben_affleck1.jpg  
│   └── michael_jordan1.jpg  
│  
├── detector.py  
├── requirements.txt  
└── unknown.jpg  

## Step 2: Load data and Train model
- Import `face-recognition` module to detect faces in images.
- Use *face_recognition.face_locations()* to find face location in an image. The function returns a list of 4-element tuples (provide 4 coordinates of the bounding box), 1 tuple for each detected face.
- Use *face_recognition.face_encodings()* to generate encodings for the detected faces. An encoding is a numeric representation of facial features that's used to match similar faces by their features.
- Then, save `name` and `encoding`.

## Step 3: Recognize Unlabeled Faces
- Load encodings from *output/* and then, load image in which we want to recognize (as test image).
- The `_recognize_face` function is to compare the *test image* with the encoding images, see if that image is in our dataset.

## Step 4: Display Results
- Create the `_display_face` function to show the detected face and its bounding box.

## Step 5: Validate Model
- Run the validation process, where model takes images with known faces and tries to identify them correctly.

## Step 6: Design command-line interface
- We create 4 flags to run in 4 modes:
    - **--help**: show you a list of options.
    - **--train**: start the training process.
    - **--validate**: start the validation process.
    - **--test**: the option that you’ll probably use the most. Use this along with the -f option to specify the location of an image with unknown faces that you want to identify. Under the hood, this works the same as validation except that you specify the image location yourself.
------------------------------------------------------------------------------------------------------------------
# Update Real-time Face Recognition
## Step 1: Update the environment
- Update *requirements.txt* file: add *opencv-python* module.
- Install the new module.

## Step 2: Train model with the given dataset and Load encodings and names of images
- Train model and save encodings to *output/*.
- Load encodings and names of images, save them to a dictionary.

## Step 3: Access webcam and Grab frames 
- Access to webcam of devices (using default webcam).
- Grab frames with `opencv`.
- Convert into RGB.

## Step 4: Detect faces in the frame
- Similar to **Step 2** of detection progress.

## Step 5: Process detected faces and Display bounding box
- Compare detected face in the frame with faces in dataset using `face_distance`, and get the minimum.
- Use the location and size of the minimum encoded frame to draw bounding box.

------------------------------------------------------------------------------------------------------------------
# References
- Refer knowledge and code: [realpython.com](https://realpython.com/face-recognition-with-python/)  
- Install and fix library: [github.com](https://github.com/sachadee/Dlib)
