CURRENT_DIR = $(shell pwd)

.PHONY: all clean-dist build-pkg

all: clean-dist build-pkg clean-dist


clean-dist:
	@rm -rf dist


build-pkg:
	@poetry build
	@rm -rf services/${LAMBDA}/packages
	@docker run -v $(CURRENT_DIR):/var/task --platform=linux/amd64 public.ecr.aws/sam/build-python3.11 /bin/sh -c "pip install dist/*.whl --target services/${LAMBDA}/packages/; exit" 
	@cd services/${LAMBDA} && rm -f ${LAMBDA}_packages.zip
	@cd services/${LAMBDA}/packages && zip -r ../${LAMBDA}_packages.zip .
	@cd services/${LAMBDA} && zip ${LAMBDA}_packages.zip lambda_function.py

clean-pkg:
	@rm -rf services/${LAMBDA}/packages
	@rm -rf services/${LAMBDA}/*.zip



