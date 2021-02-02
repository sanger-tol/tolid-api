FROM nginx:alpine

COPY nginx/* /etc/nginx/

## Remove default nginx index page
RUN rm -rf /var/www/tolid-ui/*

COPY app/ /var/www/tolid-ui/

EXPOSE 80

ENTRYPOINT ["/etc/nginx/entrypoint.sh"]