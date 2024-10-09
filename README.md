# Nitro Rubbers - A simple 2D car racing game prototype
This project is for practicing programming with Pygame and building a road sprite with random curves.


To install Pygame:

pip install pygame


## The Road Sprite

The whole road object is drawn as a single sprite before the start of the game. It is placed so that only the bottom part (screen height) is visible and then scrolled down. This requires inverse y-coordinates.

Random curves are calculated by first drawing a virtual road without actually making any lines.
A 2D vector "drives" a route at the center of the road turning at random places defined by rules which determine random distances and angles of the curves.
At the same time coordinates of this route are registered (left and right borders of the road as x-coordinates).
If the vector is not moving straight this leaves some gaps in y-coordinates. These are filled with averages of nearest coordinates to achive smoothness.
When every coordinate is calculated the actual road is drawn by connecting both x-coordinates at every y-coordinate.

This may not be the most elegant way to draw a road, but it has some advantages:
- It does not require lots of math. It is easy to maintain constant width of the road at every curve.
- Drawing the road as sprite makes it easy to use sprite collision detection to determine if a car is outside of the road.
- By using horizontal lines the curves become smooth.

Disadvantages:
- The sprite object becomes big with long roads.
- This could affect the scrolling speed and initialization time. 




