FROM flink:1.17.1

# Versions
ENV \
  # Apt-Get
  BUILD_ESSENTIAL_VER=12.9ubuntu3 \
  JDK_VER=11.0.20.1+1-0ubuntu1~22.04 \
  LIBBZ2_DEV_VER=1.0.8-5build1 \
  LIBFFI_DEV_VER=3.4.2-4 \
  LIBSSL_DEV_VER=3.0.2-0ubuntu1.10 \
  ZLIB1G_DEV_VER=1:1.2.11.dfsg-2ubuntu9.2 \
  # Python
  PYTHON_VER=3.10.13 \
  # PyFlink
  APACHE_FLINK_VER=1.17.1
  
SHELL ["/bin/bash", "-ceuxo", "pipefail"]

RUN apt-get update -y && \
  apt-get install -y --no-install-recommends \
    build-essential=${BUILD_ESSENTIAL_VER} \
    openjdk-11-jdk-headless=${JDK_VER} \
    libbz2-dev=${LIBBZ2_DEV_VER} \
    libffi-dev=${LIBFFI_DEV_VER} \
    libssl-dev=${LIBSSL_DEV_VER} \
    zlib1g-dev=${ZLIB1G_DEV_VER} \
  && \
  wget -q "https://www.python.org/ftp/python/${PYTHON_VER}/Python-${PYTHON_VER}.tar.xz" && \
  tar -xf "Python-${PYTHON_VER}.tar.xz" && \
  cd "Python-${PYTHON_VER}" && \
  ./configure --enable-optimizations --without-tests --enable-shared && \
  make -j$(nproc) && \
  make install && \
  ldconfig /usr/local/lib && \
  cd .. && \
  rm -rf "Python-${PYTHON_VER}" "Python-${PYTHON_VER}.tar.xz" && \
  ln -s /usr/local/bin/python3 /usr/local/bin/python && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Installing OpenJDK again & setting this is required due to a bug with M1 Macs
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

RUN pip3 install --no-cache-dir apache-flink==${APACHE_FLINK_VER} && \
  pip3 cache purge

USER flink
RUN mkdir /opt/flink/usrlib