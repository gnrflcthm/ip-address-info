# **IP Address Information**

## An application for getting the information from a device's public IPv4 Address. Makes use of **[ipapi](https://ipapi.co/)** for retrieving IP Address information. Returns information on the IP Addresses' GeoLocation Data. 
&nbsp; 
# **Basic Usage**

## **Installling Dependencies**
```
pip install -r requirements.txt
```

## **Fetching IP Address Data**
```
python main.py <public-ip-address>
```
#### Note: **If no IP Address is specified, makes use of the device's public IP Address**

## **Using Executable File**
Assuming the ./bin directory is added to your PATH environment variable or you are in the ./bin directory:
```
  ipaddrinfo <public-ip-address>
```
#### Note: **If no IP Address is specified, makes use of the device's public IP Address**
