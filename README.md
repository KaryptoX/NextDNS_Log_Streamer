# NextDNS API Log Streamer
A simple Python script for collecting and exporting NextDNS logs as JSON - file or direct output to STDOUT-. Supports crontab mode or "endless" mode. Simple and optimized for the use in SIEM systems e.g. as scripted input.

## Idea
I've searched for an easy way of structured importing my NextDNS logs to the SIEM/Splunk system I use. In best case without tons of 3rd party bibs,tools or plugins. I've searched through the web and already found some interesting projects (e.g. from rhijjawi/NextDNS-API or b0o/nextdns-logs-export). Unfortunately they were either complex (required some 3rd party bibs/tools) or did not work as expected e.g. provided a non structured data format, did not use the official API or in the end were just too much for "just" exporting logs. Also the scripts did not collect historic data in case of failure e.g. when the API has issues. Therefore I decided to write a short script by my own which only uses standard Python bibs and therefore can run on any system with "default" Python installation. 
> Hint: Thy script was designed for Linux like systems, but should also work on Windows systems if the Linux commands/ file paths etc. will be changed.

## Usage
The script contains some comments which should describe the used variables in details. Anyway here a short usage guide:

Before you run the script ensure that you've set the variables according to the run mode you want to perform.

Add your API Key from NextDNS account settings here:
> apikey="APIKEY"

Add your profiles from the individual NextDNS profile pages to the list:
> profiles = ["PROFILE1","PROFILE2","..."]

Define the fetch interval; ensure that you've set the fetch interval to the same interval you've planned the cronjob e.g. if you are using cron "every minute" = 60 ; in "endless" mode the script will run in that interval too. Values below 20 might cause issues with the NextDNS API and resulting duplicates in output!
> fetch_interval = 60

Define if the script should run in crontab mode or "endless" mode:
> crontab_mode = 1

If you choose "crontab_mode = 0" the script will run endless (except cancelled by user or system) based on the interval set in "fetch_interval = XX"

Should the script export the logs to STDOUT via print or write a file?
> "write_file = 0"

Destinations where the log files will be written to
> tmp_file_path = "/tmp/"

> log_file_path = "/var/log/"

Only used if "write_file = 1"
