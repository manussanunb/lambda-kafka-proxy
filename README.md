# lambda-kafka-proxy

This repo shows the example development of lambda function sending message to Kafka in python.

### Features

- Inherit lambda **monorepo** concept where multiple lambda functions shared common packages
- Demonstrate how to build **custom module**
- Build lambda package as zip file for uploading

### Pre-requisite
- python 3.11
- poetry
- docker

### File structure
```
├── lambda_package
│   ├── custom_module_one
│   │   ├── __init__.py
│   │   ├── module_one.py
│   ├── custom_module_two
│   │   ├── __init__.py
│   │   ├── module_two.py
├── services
│   ├── service_one
│   │   ├── lambda_function.py
│   ├── service_two
│   │   ├── lambda_function.py
│   ├── index.html
├── etc.
```
**lambda_package** is where you develop your own custom modules

**services** is where you write lambda functions. I use the default lambda setup which the file name must be `lambda_function.py` with the method named `lambda_handler`

### Usage
This repo uses `poetry` to manage dependencies and build packages.

Run below command to get the zip file for uploading to lambda
```
make build-pkg LAMBDA={SERVICE_FOLDER}
```
This command will generate zip file inside the `SERVICE_FOLDER`.

### Behind the scene
`poetry build` will build the package only in `lambda_package` folder. If you change the folder name, please change accordingly in `pyproject.toml`.

```
packages = [{include = "*", from="lambda_package"}]
```

Lambda runs on Amazon Linux x86_64. You may encounter import error if you build package on Apple Silicon. To ensure this will not happen, this repo use build package on lambda docker official image with specific platform.
```
docker run -v $(CURRENT_DIR):/var/task --platform=linux/amd64 public.ecr.aws/sam/build-python3.11 /bin/sh -c "pip install dist/*.whl --target services/${LAMBDA}/packages/; exit"
```
You can find full steps on building package in Makefile

### Setup for lambda and kafka
- Need to setup lambda VPC same as Kafka VPC
- Environment variables for kafka authen

---

### Resources
- [Python AWS Lambda Monorepo](https://github.com/bombillazo/python-lambda-monorepo?tab=readme-ov-file)
- Lambda python dependencies [Link1](https://nesin.io/blog/aws-lambda-layer-python-dependencies) [Link2](https://www.linkedin.com/pulse/how-create-confluent-python-lambda-layer-braeden-quirante)