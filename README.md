# VisAR

Visualizer for Adverse Reactions (VisAR) is a project to visualize the relationships between drugs and adverse effects. It comes with three primary visualizations: the treemap, the forcegraph, and the bar chart.

## Back End Set Up

If you wish to use different data than the included preprocessed files, skip down to preprocessing setup first

### Using Included Preprocessed Files

Launch a new Amazon EC2 Instance with the following settings:

- Amazon Linux using the default Amazon Machine Image
- t2.small
- Make sure to download a new key pair (.pem) when setting up the instance ("C:/Users/peter/Downloads/faers_kp.pem" in my case)

Go into the instance summary for your new instance, and record the Public IPv4 address (3.82.162.181 in my case)

Click connect in the upper right can corner, then connect again. This will open the terminal of your new server.

Download the files from this project to a new directory ("C:/Users/peter/Desktop/VISar" in my case)

Run the following command, replacing the location of your downloaded files, keypair location, and ip address
`scp -i "C:/Users/peter/Downloads/faers_kp.pem" -r "C:/Users/peter/Desktop/VISar/*" ec2-user@3.82.162.181:/home/ec2-user/`

Once all files have finished uploading, go to the server terminal and type the following commands:
````
sudo yum -y install python-pip
pip install pandas
pip install plotly
pip install flask
pip install flask_cors
````

Now start the tool with the command:

`python3 server.py`
*advanced users can run it in headless mode instead*:
`nohup python3 server.py &>/dev/null &

To shut down a headless script, find the process # with:
`sudo netstat -tulnp | grep :5000`

Then type:
`kill [process# from last step]`

The tool is now live at (replace 3-82-162-181 with the public IPv4): 
http://ec2-3-82-162-181.compute-1.amazonaws.com/index.html

### Preprocessing setup

This project includes preprocessed files for Q1-4 of 2022, if you want others, you can do the preprocessing yourself

Download ASCII files of all relevant quarters here:
https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html

Set up a MySQL Database, making sure to allow access from the ip of the machine that will do the preprocessing

Add tables matching the following:

````
DEMO:
primaryid	int	NO	PRI		
caseid	int	YES			
caseversion	int	YES			
i_f_code	varchar(45)	YES			
event_dt	int	YES			
mfr_dt	int	YES			
init_fda_dt	int	YES			
fda_dt	int	YES			
rept_cod	varchar(45)	YES			
auth_num	varchar(45)	YES			
mfr_num	varchar(45)	YES			
mfr_sndr	varchar(45)	YES			
lit_ref	varchar(400)	YES			
age	int	YES			
age_cod	varchar(10)	YES			
age_grp	varchar(5)	YES			
sex	varchar(1)	YES			
e_sub	varchar(1)	YES			
wt	float	YES			
wt_cod	varchar(10)	YES			
rept_dt	int	YES			
to_mfr	varchar(45)	YES			
occp_cod	varchar(15)	YES			
reporter_country	varchar(15)	YES			
occr_country	varchar(15)	YES			

DRUG:
primaryid	int	NO	PRI		
caseid	int	NO	PRI		
drug_seq	int	NO	PRI		
role_cod	varchar(5)	YES			
drugname	varchar(100)	YES	MUL		
prod_ai	varchar(100)	YES	MUL		
val_vbm	int	YES			
route	varchar(45)	YES			
dose_vbm	varchar(100)	YES			
cum_dose_chr	int	YES			
cum_dose_unit	varchar(5)	YES			
dechal	varchar(5)	YES			
rechal	varchar(5)	YES			
lot_num	varchar(100)	YES			
exp_dt	int	YES			
nda_num	int	YES			
dose_amt	int	YES			
dose_unit	varchar(5)	YES			
dose_form	varchar(45)	YES			
dose_freq	varchar(45)	YES			

INDI:
primaryid	int	NO	PRI		
caseid	int	NO	PRI		
indi_drug_seq	int	NO	PRI		
indi_pt	varchar(100)	YES			

OUTC:
primaryid	int	NO	PRI		
caseid	int	NO	PRI		
outc_cod	varchar(5)	NO	PRI		

REAC:
primaryid	int	NO	PRI		
caseid	int	NO	PRI		
pt	varchar(100)	NO	PRI		
drug_rec_act	varchar(45)	YES			

RSPR:
primaryid	int	NO	PRI		
caseid	int	YES			
rpsr_cod	varchar(5)	YES			

THER:
primaryid	int	NO	PRI	
caseid	int	NO	PRI	
dsg_drug_seq	int	NO	PRI	
start_dt	int	YES		
end_dt	text	YES		
dur	text	YES		
dur_cod	text	YES		
````

Run the following commands for every quarter you wish to upload, changing the file name to match the year/quarter and your directory
````
LOAD DATA LOCAL INFILE "C:\\Users\\peter\\Desktop\\ASCII\\DRUG22Q3.txt" INTO TABLE DRUG FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE "C:\\Users\\peter\\Desktop\\ASCII\\THER22Q3.txt" INTO TABLE THER FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE "C:\\Users\\peter\\Desktop\\ASCII\\INDI22Q3.txt" INTO TABLE INDI FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE "C:\\Users\\peter\\Desktop\\ASCII\\DEMO22Q3.txt" INTO TABLE DEMO FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE "C:\\Users\\peter\\Desktop\\ASCII\\REAC22Q3.txt" INTO TABLE REAC FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE "C:\\Users\\peter\\Desktop\\ASCII\\RPSR22Q3.txt" INTO TABLE RPSR FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE "C:\\Users\\peter\\Desktop\\ASCII\\OUTC22Q3.txt" INTO TABLE OUTC FIELDS TERMINATED BY '$' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
````

Go to config.ini in the downloaded project files

Alter all parameters to match your database

Run the following command in the directory of your project: (Will take a very long time to run, possibly days depending on the number of quarters uploaded)

`python3 preproc.py`

## Front End Setup

Ensure you have an Amazon EC2 instance running. Follow the instructions located at https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateWebServer.html to create an Apache web server (PHP and MariaDB is not required).
Upload the files in this repository to the /var/www/html folder on your EC2 instance and restart the Apache web server. When you go to the URL of your EC2 instance in any browser, you should see the home page of this project (index.html).
