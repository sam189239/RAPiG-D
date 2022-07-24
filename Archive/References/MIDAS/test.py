
import numpy as np
import cv2
import time


path_model = "models/"

# Read Network
#model_name = "model-f6b98070.onnx"; # MiDaS v2.1 Large
model_name = "model-small.onnx"; # MiDaS v2.1 Small


# Load the DNN model
model = cv2.dnn.readNet(path_model + model_name)


if (model.empty()):
    print("Could not load the neural net! - Check path")


# Set backend and target to CUDA to use GPU
model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

vid_dir = 'road_sample.mp4'
# Webcam
cap = cv2.VideoCapture(0)


while cap.isOpened():

    # Read in the image
    success, img = cap.read()

    imgHeight, imgWidth, channels = img.shape

    # start time to calculate FPS
    start = time.time()


    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)



    cv2.imshow('image', img)



    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

 

cap.release()
cv2.destroyAllWindows()

# https://learnopencv.com/how-to-use-opencv-dnn-module-with-nvidia-gpu-on-windows/

# cmake ^
# -G "Visual Studio 17 2022" ^
# -T host=x64 ^
# -DCMAKE_BUILD_TYPE=RELEASE ^
# -DCMAKE_INSTALL_PREFIX=%cwd%/OpenCV-%opencv-version% ^
# -DOPENCV_EXTRA_MODULES_PATH=%cwd%/opencv_contrib/modules ^
# -DINSTALL_PYTHON_EXAMPLES=OFF ^
# -DINSTALL_C_EXAMPLES=OFF ^
# -DPYTHON_EXECUTABLE=%CONDA_PREFIX%/python3 ^
# -DPYTHON3_LIBRARY=%CONDA_PREFIX%/libs/python3 ^
# -DWITH_CUDA=ON ^
# -DWITH_CUDNN=ON ^
# -DOPENCV_DNN_CUDA=ON ^
# -DWITH_CUBLAS=ON ^
# ..
