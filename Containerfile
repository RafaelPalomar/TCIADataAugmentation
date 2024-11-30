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

#Download and  install NBIA download client
RUN curl -LO https://github.com/CBIIT/NBIA-TCIA/releases/download/DR-4_4_3-TCIA-20240916-1/nbia-data-retriever_4.4.3-1_amd64.deb && \
    dpkg -x nbia-data-retriever_4.4.3-1_amd64.deb /opt
