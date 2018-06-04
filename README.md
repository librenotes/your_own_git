# Migrate To Your Own Git Server: 30 Mins - 1 Euro:
#### Is it worth it to sell your data for just a f*!*ing 1 Euro/Month?
##### NO.

As you know github is sold to MS. If you don't want to use it anymore for various reasons, this repo will help you to create your own git server and migrate your repositories from github under 30 mins with a 1 Euro VPS provider. At the end of this, you will have an Let's Encrypt SSL Certified git service which runs with Nginx Web Server, Go Language and based on [Gitea](https://gitea.io/en-US/). 

## Prerequirements:
- Own a VPS, We don't recommend you [arubacloud](https://www.arubacloud.com/) but it is the cheapest VPS(1 Euro/Month), but some process like creating and initializing your VPS sometimes takes over 30 mins, no problem during the running state. 
- Choose your favorite GNU/Linux distrubition, this documentation explain concept over Ubuntu 16.04 because of it's simplicity.(Does not mean that Ubuntu is our favourite distribution).
- A database server : We prefer Postgresql in this step.
- Optional: Own a domain.

### Setup:

- Connect your VPS over SSH and than `sudo apt update && sudo apt upgrade`.
- Create a user, let's call it 'git', `sudo adduser git` than `sudo adduser git sudo`.  
- Change to that user, `sudo - git`
- After update and upgrade complete, install postgresql with following command `sudo apt-get install postgresql postgresql-contrib` 
- After postgresql installation done, install nginx server with following command `sudo apt-get install nginx` 
- We are almost done, know lets download the binary for Gitea run the following command `wget -O gitea https://dl.gitea.io/gitea/1.3.2/gitea-1.3.2-linux-amd64` **and be sure that you are in** `/home/git` directory.
- After download opperation, give permission to it: `chmod +x gitea` 
- After this step, lets make necessity configuration in Nginx, `sudo nano /etc/nginx/sites-available/gitserver` and paste the following lines with editing `<ip_or_domain>`(domain adress or public ip adress) 


```
server {
    listen 80;
    server_name <ip_or_domain>;
    location / {
        proxy_pass <ip_or_domain>:3000;
    }
}
```

- Make a link for sites-enabled directory, to activate vhost file, run following command :`sudo ln -s /etc/nginx/sites-available/gitserver  /etc/nginx/sites-enabled/`
- Now we are almost done with nginx configuration, check if you have any syntax error with following command `sudo nginx -t`.
- Let's create a service for Gitea, run following command: `sudo nano /etc/systemd/system/gitea.service` paste the following configuration:

```
[Unit]
Description=Gitea
After=syslog.target
After=network.target

[Service]
Type=simple
User=git
WorkingDirectory=/home/git/
ExecStart=/home/git/./gitea web
Restart=always

[Install]
WantedBy=multi-user.target
```

- After saving the configuration you can restart nginx first, `sudo systemctl restart nginx` than enable your gitea service by following command: `sudo systemctl enable gitea.service` and finally `sudo systemctl start gitea.service`. 
- Final configuration for postgresql: create postgres user and db for the system. For creating a new postgresql user,  run `sudo -u postgres psql -c "CREATE USER <yourpostgresusername> WITH PASSWORD '<yourpass>';"` 
- Than run the following command: `sudo -i -u postgres`
- Create a db `createdb -O <yourpostgresusername> <yourdbname>`
- `exit`

##### That's all with PG, don't forget your: `<yourpostgresusername> <yourdbname> <yourpass>`


### Create Secure Connection With Let's Encrypt:

- Run the following command : `sudo add-apt-repository ppa:certbot/certbot`
- Update again : `sudo apt-get update`
- Install cert-bot: `sudo apt-get install python-certbot-nginx`
- Create a certifiate: `sudo certbot --nginx -d <your_domain_or_ip>`  
- Accept answers, than at the end it will ask for:


```
Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
-------------------------------------------------------------------------------
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
-------------------------------------------------------------------------------
Select the appropriate number [1-2] then [enter] (press 'c' to cancel):

```

- In this case, we generally select 2. But it is your choice.

### Gitea web config part

- Now go to your domain or `your_ip:3000` over a web browser. It will redirect you to your git server installation page, select **Postgresql as Database Type in Database Settings**, enter necessity informations `<yourpostgresusername> <yourdbname> <yourpass>`.
- Don't forget to change **Application URL in General Application Settings**, set it to your domain or `your_ip:3000`.
- And create admin user if you wish, you can also change server and services settings according to your necessity. After all configuration finish, press Install Gitea Button, you will probably see a 404 page. Go to your root domain, that's it. **You have a SSL certified, fast and cheap git server which runs like a charm.**

#### You can also make changes on configuration: 

- Open app.ini file:

```
sudo nano /home/git/custom/conf/app.ini 
```

- After you are done with changes:

```
 sudo systemctl restart gitea.service 
```

#### Bonus 0: Your git service has an API! Checkout `<yourip:3000_or_yourdomain>/api/swagger`

#### Bonus 1: You can use migrater.py to migrate your project into your new git server! 

## Donate and Help Us

### As Librenotes team we are developing free as in freedom note taking application, checkout [Librenotes](https://github.com/librenotes/web), any help is appreciated!

```
BTC > qzuej7qa36tkqpzuyz265068s7exymn4dq8h6ha9ep

ETH > 0xBCa591260D9b0d25eD87dc9B4330980DA44DbB18
```

