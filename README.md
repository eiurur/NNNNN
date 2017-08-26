# NNNNN

Automatic collection program of hentai images using CNN

# Requirements

- Windows 10
- CUDA
-- 8.0
- cuDNN
-- 5.1
- Anaconda
-- 4.4.0
  - Python
  -- 3.5
- tensorflow-gpu
-- 1.1.0
- MongoDB
-- 3.x


# Getting Started

1. Install Anaconda

> <a href="https://www.continuum.io/downloads" target="_blank">Download Anaconda Now! | Continuum</a>

2. Build a virtual environment

        $ conda create -n tensorenv python=3.5 numpy jupyter
        $ activate tensorenv

3. Download source code

        $ git clone https://github.com/eiurur/NNNNN
        $ cd NNNNN

4. Install required packages

        $ pip install -r requirements.txt 
        $ pip install --upgrade https://storage.googleapis.com/tensorflow/windows/gpu/tensorflow_gpu-1.1.0-cp35-cp35m-win_amd64.whl


5. create `setting.ini` under `configs` folder, then rewrite the settings.

        [development]
        CLASSES_NUM = 17
        IMAGE_SIZE_PX = 128
        FAPPABLE_FOLDER = 0,1,2,3,4
        MAX_STEPS = 200
        BATCH_SIZE = 50
        LEARNING_RATE = 1e-5

        # if you want to collect the images from twitter
        TWITTER_CONSUMER_KEY = <YOUR_TWITTER_CONSUMER_KEY>
        TWITTER_CONSUMER_SECRET = <YOUR_CONSUMER_SECRET>
        TWITTER_ACCESS_KEY = <YOUR_TWITTER_ACCESS_KEY>
        TWITTER_ACCESS_SECRET = <YOUR_TWITTER_ACCESS_SECRET>
        TWITTER_STREAING_LIST_NAME = <YOUR_TWITTER_LIST>

        # if you want to collect the images from tumblr
        TUMBLR_CONSUMER_KEY = <YOUR_TUMBLR_CONSUMER_KEY>
        TUMBLR_CONSUMER_SECRET = <YOUR_TUMBLR_CONSUMER_SECRET>
        TUMBLR_ACCESS_KEY = <YOUR_TUMBLR_ACCESS_KEY>
        TUMBLR_ACCESS_SECRET = <YOUR_ACCESS_SECRET>
        TUMBLR_BLOG_NAME = <YOUR_TUMBLR_BLOG_NAME>

6. Run `init.sh`

        $ sh init.sh

7. Copy your fappable images to `1_generate_csv/images` and `1_generate_csv/test_images`


8. Start training

        $ sh train.sh

9. Start collection

        $ sh launch_tumblr.sh 

# Usage

## train

    $ sh train.sh

## collect

tumblr

    $ sh launch_tumblr.sh

twitter

    $ sh launch_twitter.sh
