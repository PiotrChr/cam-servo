PISERVOIP := 192.168.2.55
PISERVOUSER := pi
PISERVOFOLDER := /home/pi/piIpCam

CAM_NGINX := /etc/nginx/sites-enabled/cam.conf
SERVO_NGINX := /etc/nginx/sites-enabled/servo.conf
DLIB_VERSION := 19.24
# 	x11vnc -display :0

prepare:
	sudo apt-get update && sudo apt install -y \
	build-essential \
	tk-dev \
	libncurses5-dev \
	libncursesw5-dev \
	libreadline6-dev \
	libdb5.3-dev \
	libgdbm-dev \
	libsqlite3-dev \
	libssl-dev \
	libbz2-dev \
	libexpat1-dev \
	liblzma-dev \
	zlib1g-dev \
	libffi-dev \
	python3.9-dev \
	python3-distutils \
	uwsgi \
	uwsgi-src \
	uuid-dev \
	libcap-dev \
	libpcre3-dev \
	libpython3.9-dev \
	libpython3-all-dev \
	uwsgi-plugin-python3 \
	uwsgi build-essential \
	nginx \
	libatlas-base-dev \
	uwsgi-plugin-python3 \
	python3-pip \
	libopenjp2-7 \
	libavcodec-dev \
	libavformat-dev \
	libswscale-dev \
	libgtk-3-dev \

prepare_dlib:
	sudo apt-get install -y \
	cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev \
	&& rm -rf tmp \
	&& mkdir tmp \
	&& cd tmp \
	&& wget http://dlib.net/files/dlib-${DLIB_VERSION}.tar.bz2 \
	&& tar xvf dlib-${DLIB_VERSION}.tar.bz2 \
	&& cd dlib-${DLIB_VERSION} \
	&& mkdir build && cd build \
	&& cmake .. && cmake --build . --config Release \
	&& sudo make install \
	&& sudo ldconfig \
	&& cd .. \
	&& pkg-config --libs --cflags dlib-1


prepare_dlib_python:
	cd tmp/dlib-${DLIB_VERSION} \
	&& python3 setup.py install


prepare_resources:
	sudo rm -f ${CAM_NGINX} ${SERVO_NGINX} \
	&& sudo cp resources/nginx/cam.conf /etc/nginx/sites-available \
	&& sudo cp resources/nginx/servo.conf /etc/nginx/sites-available \
	&& sudo ln -s /etc/nginx/sites-available/cam.conf /etc/nginx/sites-enabled \
	&& sudo ln -s /etc/nginx/sites-available/servo.conf /etc/nginx/sites-enabled \
	&& sudo service nginx restart
	&& sudo cp resources/service/cam_producer.service /etc/systemd/system/ \
	&& sudo cp resources/service/sting_servo.service /etc/systemd/system/

# install_vnc:
# 	sudo apt-get install -y x11vnc net-tools

install_cam:
	pip3 install -r requirements.txt

test_cam:
	python3 scripts/testcam.py

sync_cam_piservo:
	rsync -av --exclude={'venv','.idea','__pycache__','.git'} ./ ${PISERVOUSER}@${PISERVOIP}:${PISERVOFOLDER}

start_uwsgi_cam:
	uwsgi resources/uwsgi/uwsgi_cam.ini --enable-threads

start_uwsgi_servo:
	uwsgi resources/uwsgi/uwsgi_servo.ini --enable-threads

start_kafka_cam:
	python3 kafkaCam.py -c 0
