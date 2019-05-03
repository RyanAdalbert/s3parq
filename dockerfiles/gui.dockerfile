FROM node:9.6.1

# set working directory
RUN mkdir -p /usr/src/gui 
WORKDIR /usr/src/gui

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/gui/node_modules/.bin:$PATH

# install and cache app dependencies
COPY /core/gui/public /usr/src/gui/public
COPY /core/gui/src /usr/src/gui/src
COPY /core/gui/package.json /usr/src/gui/package.json
RUN npm install
RUN npm install react-scripts@1.1.1 -g 
EXPOSE 3000

# start app
ENTRYPOINT ["npm"]
CMD ["start"]
