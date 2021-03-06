FROM tensorflow/tensorflow:1.12.0-gpu
LABEL maintainer "Shan Yang <shan.yang@usb.ch>"


RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1 \
    && echo "/usr/local/cuda/lib64/stubs" > /etc/ld.so.conf.d/z-cuda-stubs.conf \
    && ldconfig

ENV LD_LIBRARY_PATH="/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH"


RUN apt-get install software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y apt-utils libsm6 libxext6 libxrender-dev wkhtmltopdf xvfb python3.6 python3.6-venv python3.5-venv python3-pip git-all wget && \
    rm /usr/bin/python && ln -s /usr/bin/python3.6 /usr/bin/python


RUN mkdir /apps && cd /apps && \
    git clone --single-branch --branch lungopacity https://github.com/usb-radiology/NiftyNet.git && \
    git --git-dir ./NiftyNet/.git --work-tree ./NiftyNet reset --hard 0ca71d1598da150

RUN cd / && python3.5 -m venv venv_niftynet && \
    . /venv_niftynet/bin/activate && \
    python3.5 -m pip install --upgrade pip && \
    python3.5 -m pip install -r /apps/NiftyNet/requirements-gpu.txt && \
    python3.5 -m pip install antspyx tensorflow-gpu==1.12 && \
    python3.5 -m pip install --no-cache-dir -e /apps/NiftyNet

ADD ./requirements.txt /apps/LungOpacity/

RUN cd / &&  python3.6 -m venv venv_report --clear && \
    . /venv_report/bin/activate && \
    python3.6 -m pip install --upgrade pip && \
    python3.6 -m pip install -r /apps/LungOpacity/requirements.txt && \
    rm -rf /apps/LungOpacity/

RUN mkdir /apps/niftynet_model && mkdir /apps/niftynet_model/models &&  cd /apps/niftynet_model/models &&\ 
    wget https://github.com/usb-radiology/LungOpacity/releases/download/v0.1.0/model.ckpt-200000.meta &&\ 
    wget https://github.com/usb-radiology/LungOpacity/releases/download/v0.1.0/model.ckpt-200000.index &&\ 
    wget https://github.com/usb-radiology/LungOpacity/releases/download/v0.1.0/model.ckpt-200000.data-00000-of-00001 &&\ 
    wget https://github.com/usb-radiology/LungOpacity/releases/download/v0.1.0/checkpoint


