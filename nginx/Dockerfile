FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY flask_tickets.conf /etc/nginx/conf.d/

CMD ["nginx", "-g", "daemon off;"]
