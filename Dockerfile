FROM ubuntu:18.04
RUN apt update
RUN apt upgrade -y
RUN apt install -y python3.7
RUN apt install -y python3-pip git
RUN python3.7 -m pip install -U git+https://github.com/Rapptz/discord.py
RUN mkdir /bot
ADD bot.py /bot/bot.py
ADD secret.py /bot/secret.py
CMD ["/bot/bot.py"]
