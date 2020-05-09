<br />
<p align="center">
  <img src="https://imgur.com/S2gJ8ch.png" alt="Logo" height="80">

  <p align="center">
    A real-time auctioning platform that provides a platform for sellers and prospective buyers from all over the world to interact.
    <br />
    <a href="https://github.com/SakshiUppoor/re-bag"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    View Demo
    ·
    <a href="https://github.com/SakshiUppoor/re-bag/issues">Report Bug</a>
    ·
    <a href="https://github.com/SakshiUppoor/re-bag/issues">Request Feature</a>
  </p>
</p>

## Install

Creating and activating virtual environment

    virtualenv venv
    cd Scripts
    activate

Setup & install Redis server on Windows
* [Linux](https://redis.io/topics/quickstart)
* [Mac](https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298)
* [Windows](https://www.onlinetutorialspoint.com/spring-boot/setup-install-redis-server-on-windows-10.html)

Start the Redis server 
  
Navigate back to the main folder. Installing requirements and making migrations

    pip install -r requirements.txt
    python manage.gy makemigrations
    python manage.py migrate
    python manage.py runserver

## Team
* <a href="https://github.com/SakshiUppoor"><b>Sakshi Uppoor</b></a> - Full Stack & Design
* <a href="https://github.com/SheelSanghvi"><b>Sheel Sanghvi</b></a> - Full Stack
* <a href="https://github.com/Samitkk18"><b>Samit Kapadia</b></a> - Frontend 

## About the Project
<p align="center">
<img style="margin:1em" src="https://imgur.com/KYm573Q.gif" width="100%"/>
</p>

### Pages
* Login
* Sign Up
* Home
* Shop
* Product Details
* Auction Room
* Cart
* My Products
* Add Product
* Profile

### Features

<!--##### A very interactive home page showcasing topmost ongoing and upcoming auctions and the collectibles for sale.-->

##### Real-time filtering of products based on category.

##### Real-time online bidding in auction rooms.
Auction room where all bidders bid against each other for a particular product. 
The room displays all bidders along with their latest bids, the base price, current price and details of the product being auctioned.

##### Detailed description for all products along with images.
Sellers can add multiple images for a product to showcase the product from all angles.
Live status feature to indicate whether the auction is live or not.
Tells users how much time is left for an auction to start or end.


### Built Using
* [Django](https://docs.djangoproject.com/en/2.2/) - The web framework used
* [Django Channels](https://channels.readthedocs.io/en/latest/) - Layer for websockets and background tasks
* [Django Tempus Dominus](https://pypi.org/project/django-tempus-dominus/) - Widget for the Tempus Dominus Bootstrap 4 DateTime picker
* [CozaStore](https://colorlib.com/wp/template/coza-store/) - ColorLib template
* [Unsplash](https://unsplash.com/) - Free to use, high quality photographs
* [Font Awesome](https://fontawesome.com/) - Vector icons set
* [Inkscape](https://inkscape.org/) - Design software for icons

### Built On
* [Visual Studio Code](https://code.visualstudio.com/) - Code Editor
* [Redis](https://redis.io/) - Server to run Channels
