FROM debian:unstable-slim

RUN apt-get update
RUN apt-get install -y \ 
      vim \
      gcc-riscv64-linux-gnu \
      qemu-user-static \
      python3

RUN ln -s /usr/bin/python3 /usr/bin/python3.12

RUN ln -s /usr/bin/qemu-riscv64 /usr/bin/qemu-riscv64-static