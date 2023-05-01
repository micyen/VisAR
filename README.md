# VisAR

Visualizer for Adverse Reactions (VisAR) is a project to visualize the relationships between drugs and adverse effects. It comes with three primary visualizations: the treemap, the forcegraph, and the bar chart.

## Setup

Ensure you have an Amazon EC2 instance running. Follow the instructions located at https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateWebServer.html to create an Apache web server (PHP and MariaDB is not required).
Upload the files in this repository to the /var/www/html folder on your EC2 instance and restart the Apache web server. When you go to the URL of your EC2 instance in any browser, you should see the home page of this project (index.html).
