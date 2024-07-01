READ ME

I built this project over a period of two weeks. It was developed using several technologies including Python, Flask, HTML, CSS, Bootstrap 5, Javascript, and jQuery. The project also integrates with the Philippine Standard Geographic Code (PSGC) API and Stripe API for checkout. Overall, this project demonstrates my ability to work with these technologies and develop a functional web application within a short timeframe.

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 main.py


sudo docker build --tag sulat-aian .
sudo docker images
sudo docker run -p 5000:5000 --env-file .env sulat-aian
sudo docker run -d -p 5000:5000 --env-file .env sulat-aian

sudo docker build --tag kriskap .
sudo docker run -d -p 6000:5000 --env-file .env kriskap

sudo docker start <container_name>
