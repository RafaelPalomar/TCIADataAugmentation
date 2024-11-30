FROM debian:bookworm

# Set labels to provide metadata about the container, indicating its purpose as a devcontainer for 3D Slicer development
LABEL org.opencontainers.image.title="TCIA Data Augmentation Container" \
      org.opencontainers.image.description="A toolbox container for data augmentation of TCAI data for deep-learning purposes." \
      maintainer="Rafael Palomar (rafael.palomar@ous-research.no)"

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Copy the 'extra-packages' file containing the list of packages to be installed
COPY extra-packages /

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends $(grep -v '^#' /extra-packages) && \
    # Clean up to reduce the image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY pip-packages /
RUN grep -v '^#' /pip-packages | xargs pip install --break-system-packages
RUN rm /pip-packages

#Download and  install NBIA download client
RUN curl -LO https://github.com/CBIIT/NBIA-TCIA/releases/download/DR-4_4_3-TCIA-20240916-1/nbia-data-retriever_4.4.3-1_amd64.deb && \
    dpkg -x nbia-data-retriever_4.4.3-1_amd64.deb /opt

#Download and install 3D Slicer
RUN curl -L https://download.slicer.org/bitstream/6748030776aed8e333421336 | tar xz -C /opt

#Download Slicer-SOFA
RUN gdown 15cghLNvNzXGc7FdcJP6NDjNbZEeck4C2 -O 33130-linux-amd64-Sofa-git365fd33-2024-11-24.tar

# Make Extensions directory and install Slicer-SOFA
COPY scripts/slicer_install_Slicer-SOFA.py /
RUN xvfb-run --auto-servernum --server-args='-screen 0 1024x768x24' \
    /opt/Slicer-5.7.0-2024-11-27-linux-amd64/Slicer --no-main-window --launcher-no-splash --python-script /slicer_install_Slicer-SOFA.py
RUN rm /slicer_install_Slicer-SOFA.py
