#Use a base image that has Python and R installed
FROM rocker/r-ver:4.2.2

# Install system dependencies for Python, R, and other necessary libraries
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    python3-tk \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    r-cran-rcpp \
    r-cran-rms \
    && apt-get clean

RUN pip3 install --upgrade pip setuptools wheel
# Install Python dependencies
RUN pip3 install numpy scipy statsmodels rpy2
# Install R packages
RUN R -e "install.packages('rpy2')"
RUN R -e "install.packages('rms')"

# Set the working directory
WORKDIR /usr/src/app

# Copy the Python and R script into the container
COPY . .

# Set the entrypoint to run the Python script
CMD ["python3", "sample_size_calc.py"]
