# plant-control-website

Simple project for class. I decided to make my own website instead of displaying data on poor LCD display.
Rpi configured to be the server and of course sensors reader.

Project made with:
 - RaspberryPi 2, 
 - stuff like sensors, wires, water pump and LED as a bulb substitute,
 - Python (Flask, jsonify), 
 - HTML, 
 - CSS,
 - JavaScript (AJAX).

/* Images, style.css, script.js should be in "static" directory, index.html should be in "templates" directory and then "static", "templates" 
and app.py should be in one directory also. */

The goal for this project is to make another, one of thousands on the internet, self watering plant. 
Not ready yet. Button with bulb image is responsible for "light" for the plant. Button with a drop is
responsible for watering. Last watering is shown in the section above buttons. The goal is to make light
and pump turning to mode "on" when the sunlight and soil humidity drops below designated level despite ability turning 
them on with those buttons.

![](https://github.com/rafalBaron/plant-control-website/blob/main/plant.gif)

Tried to make it a bit responsive, some problems occurred but I will fix them of course in the future.

![](https://github.com/rafalBaron/plant-control-website/blob/main/plant2.gif)

Final version given straight to the Professor

![](https://github.com/rafalBaron/plant-control-website/blob/main/resp.png) ![](https://github.com/rafalBaron/plant-control-website/blob/main/resp2.png)
