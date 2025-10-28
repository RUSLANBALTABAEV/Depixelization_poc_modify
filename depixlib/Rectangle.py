from __future__ import annotations

class Rectangle:
    def __init__(self, startCoordinates: tuple[int,int], endCoordinates: tuple[int,int]):
        self.startCoordinates = startCoordinates
        self.endCoordinates = endCoordinates
        self.x = startCoordinates[0]
        self.y = startCoordinates[1]
        self.width = endCoordinates[0] - self.x
        self.height = endCoordinates[1] - self.y

class ColorRectange(Rectangle):
    def __init__(self, color: tuple[int,int,int], startCoordinates: tuple[int,int], endCoordinates: tuple[int,int]):
        super().__init__(startCoordinates,endCoordinates)
        self.color = color

class RectangleMatch:
    def __init__(self, x:int, y:int, data:list):
        self.x = x
        self.y = y
        self.data = data
