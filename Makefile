PROJECT="core"
DEPLOYMENT_ENVIRONMENT?=dev

all : build install publish

build :
	@echo "Building ${PROJECT}.....";

install : build
	@echo "Installing ${PROJECT}.....";

publish : install
	@echo "Publishing ${PROJECT}.....";
