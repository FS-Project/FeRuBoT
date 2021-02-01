#
# INFO : ini merupakan copy source code dari repo MoveAngel, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the MoveAngel repo, and has the permission of the owner.
#
FROM ferubot/docker:alpine-latest

RUN mkdir /FeRuBoT && chmod 777 /FeRuBoT
ENV PATH="/FeRuBoT/bin:$PATH"
WORKDIR /FeRuBoT

RUN git clone https://github.com/FS-Project/FeRuBoT -b master /FeRuBoT

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /FeRuBoT/

#
# Make open port TCP
#
EXPOSE 80 443

#
# Finalization
#
CMD ["python3","-m","userbot"]
