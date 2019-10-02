FROM ubuntu:18.04
RUN apt update
RUN apt upgrade -y
RUN apt install -y python3.7
RUN apt install -y python3-pip
RUN python3.7 -m pip install -U discord.py
RUN mkdir /bot
ADD bot.py /bot/bot.py
ADD secret.py /bot/secret.py
CMD ["/bot/bot.py"]
