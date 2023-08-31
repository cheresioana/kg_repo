#starting rabbitMQ
#docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management

#starting xamp with apache 
echo "ioana" | sudo -S /opt/lampp/./manager-linux-x64.run

python3.8 -m venv my_env

source my_env/bin/activate

pip install -r requirements.txt

python Scraper/main_scraper.py

python Aggregator/main.py

python Aggregator/API/app.py

python kg/API/app.py



