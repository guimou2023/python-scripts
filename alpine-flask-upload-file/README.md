# Base [Alpine OS](https://hub.docker.com/_/alpine/) and [Python Flask](http://flask.pocoo.org/) (with Python 2.7) to upload file！


---
You have to build your own image wtich the Dockerfile.
```
docker build -t Registry:5000/images/alpine-flask-upload-app .
```

This image is used to run flask upload file applications. To start a container use

```
docker run --name flask-upload-app --restart=always \
	-p 80:911 \
	-v /local/uploads:/root \
	[-v /path/to/app/:/app \]
	-d Registry:5000/images/alpine-flask-upload-app -d
```

`-v /path/to/app/:/app` - with this can specifies the path to the folder containing a file named app.py, which should be your main application（By default, you don't have to use it, because the Dockerfile has already defined.)

`-p 80:911` - the image exposes port 911, in this example it is mapped to port 80 on the host

---
## Installing additional python or flask packages
This image comes with a basic set of python packages and the basic flask and python-pip installation.

If you need any non-default python or flask packages, the container will install them on its first run using python pip and a requirements.txt file. Save a requirements.txt file in the root folder of your app, which is mounted to the /app folder of the container. The format of the file is described in the [pip documentation](https://pip.readthedocs.org/en/1.1/requirements.html#requirements-file-format). After that you can create a new container with the above docker command. The entrypoint script will take care of the package installation listed in the requirements file.

If an additional package is needed during runtime of the container it can be installed with following command.

```
docker exec YOUR_CONTAINER_ID/NAME /bin/bash -c "pip install package-name"
```

---
## Installing additional Alpine packages
Sometimes, additional python or flask packages need to build some dependecies. Additional Alpine packages can be installed into the container using a requirements file similar to the python requirements file. Listed packages will be installed on the first run of the container.

You need to save a file named requirements_image.txt into the root folder of your app, which is mounted to the /app folder of the container. Just write the packages separated with space or a new line into the file. 


---
## Internals
The flask application is started using a UWSGI socket.

Nginx is used to map the socket to port 80 within the image. This image does not offer any SSL capability, please use a [nginx proxy](https://github.com/jwilder/nginx-proxy) for this. Nginx will deliver static content (e.g. CSS or JS Files) directly without going through flask or uwsgi.

### Log messages
Logs can be displayed using `docker logs -f CONTAINER_ID/NAME`

---
## Debug mode

Debug mode means the container doesn't use uwsgi and nginx but starts the flask app with a simple `python app.py`. So you can make use of the build-in flask development webserver and the automated reload system after editing the application.

To start a container in debug mode use:

```
docker run --name flask-upload-app --restart=always \
	-p 80:911 \
	-v /path/to/app/:/app \
	-d Registry:5000/images/alpine-flask-upload-app -d
```

Your app.py file must have a section similiar to the following example to start the app within the debug mode.

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=911, debug=True)
```

To get the command line output of your app use `docker logs -f CONTAINER_ID/NAME`.
