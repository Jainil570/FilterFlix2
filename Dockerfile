# Use the official Apache Tomcat image
FROM tomcat:9.0-jdk11-corretto

# Remove the default webapps
RUN rm -rf /usr/local/tomcat/webapps/*

# Copy your WAR file into the webapps folder
# The name of the WAR file determines the URL path.
# Copying it as ROOT.war makes it accessible at the root URL (/).
COPY snapchat2.war /usr/local/tomcat/webapps/ROOT.war