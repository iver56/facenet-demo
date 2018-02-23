# Setup

* Install Anaconda with Python 3.6
* Install CUDA 9.0 and cuDNN 7.0
* Clone this repo
* Navigate to the project folder in an Anaconda-activated shell
* `conda env create`
* Download and unzip the training dataset and the metadata at [http://zeus.robots.ox.ac.uk/vgg_face2/](http://zeus.robots.ox.ac.uk/vgg_face2/). Warning: Downloading and unzipping will take hours.
* Update the paths in settings.py
* Calculate feature descriptors, needed for finding the most similar face after celebrity classification: `calculate_feature_descriptors.py`. Warning: This will take ~10 hours on a GTX 1070.

# Usage
* Start the web server: `python web_service.py` and visit localhost:5000 in your browser
