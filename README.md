# Creative Coding Portfolio

## TouchDesigner

Persistent lines:
The project below uses pixel and compute shaders, as I've been learning how to make connections between points persist over time. Technically brute-forcing this a bit, as I'm checking all points with all points and then throwing out lines conditionally, hence the small number of points. Find the [project file here](https://github.com/aecollier/portfolio/blob/main/stoch_aesthetic.tox). 

driveId: 1hac0CFLTPYplQfH0SegZZ6yzUpf_jWvu/preview

{% include googleDrivePlayer.html id= page.driveId %}

The project above was the first iteration of working with lines, using several pixel shaders. [Test it out here!](https://github.com/aecollier/portfolio/blob/updates/webcam_lines.tox)


## Python code - quote generator
I've got a more complex and robust web scraper in production from my work with Old Town Shops which I would be thrilled to tell you more about -- here's a little scraping exercise to show you what I've been working on in the meantime. This program either generates a random quote from goodreads based on a random positive word, or else takes user input of a recent read and uses a word from the book's description to generate a quote related to it. In the future I plan to continue developing this by adding custom Selenium error handling, as Selenium in this context is very reliant on pages loading properly and consistently. I would also like to add unit tests - first up would be ensuring consistency of output based on the same user input, as well as adding functionality to check the validity of user input. 
The files are in the [goodreads folder in my repo](https://github.com/aecollier/portfolio/tree/main/goodreads). Once downloaded, install dependencies and then run the web scraper with:
```
pip install -r requirements.txt
python3 goodreads.py
```

## D3 Squirrel Census Modeling

![image](https://user-images.githubusercontent.com/63130693/117375435-d1476d00-ae83-11eb-9c4c-916c8034225f.png)

As a bonus, this was a feature project from learning D3.js, an open-source data viz tool. I like that it shows my exploration process, even though it's a different language. Interact with it [here](https://observablehq.com/@aecollier/sqrrules), and a number of other interactive visualizations about squirrels in Central Park! 


## p5 Particle Lines
![image](https://user-images.githubusercontent.com/63130693/117043700-6dc21180-acc2-11eb-8d71-72bb223a577b.png)

This is a still from [this](https://aecollier.github.io/portfolio/live_sketches/) force simulation, where the mouse has a "gravitational" pull or repulsion on the particles, which change color based on their velocity.

Give it a try [here](https://aecollier.github.io/portfolio/live_sketches/)!



