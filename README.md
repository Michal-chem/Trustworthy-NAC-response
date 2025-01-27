# Sample Size Calculator - Dockerized

This project provides a **Sample Size Calculator** in a Docker container. The Docker image includes all necessary dependencies and can be easily run on any Linux-based system.

## Requirements

To use this Docker image, ensure that you have installed the following:

- **Docker**: Docker must be installed and running on your machine.
- **X11**: If you want to run graphical interfaces (e.g., Tkinter), make sure your system supports X11 for GUI forwarding.

## Getting Started

### 1. Clone the Repository

Start by cloning the repository to your local machine:

git clone https://github.com/your-username/sample-size-calculator.git

### 2. Build the Docker Image

docker build -t sample-size-calculator .

### 3. Run the Docker Container

docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -it --rm sample-size-calculator

### 4. Accessing the Sample Size Calculator

After running the above command, the container should start, and you should be able to interact with the Sample Size Calculator application.
The application has a GUI that appears on your host machine (due to X11 forwarding).

### 5. Troubleshooting
- X11 issues: If you encounter issues with the X11 display, make sure your system has the necessary X11 libraries installed and that you're running a compatible Linux system.
- Permissions: You may need to configure permissions for accessing the X11 socket. On some systems, you might need to allow access by running xhost +local:docker before starting the container.

### 6. License

This project is licensed under the MIT License - see the LICENSE file for details.

## 7. Authors and Contributors

- **Michał Kosno** - Creator and maintainer
- **Dimitri Kessler** - Creator
- **Maciej Bobowicz** - Contributor
- **Smriti Joshi** - Contributor
