import pygame
SHIP_WIDTH = 55
SHIP_HEIGHT = 40

class Ship():
    def __init__(self, x, y, health, bullets = []):
        self.x = x
        self.y = y
        self.health = health
        self.bullets = bullets
        self.bounding_box = pygame.Rect(self.x, self.y, SHIP_WIDTH, SHIP_HEIGHT)
    
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, val):
        self.__x = val
        
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, val):
        self.__y = val
    
    
    @property
    def health(self):
        return self.__health
    
    @health.setter
    def health(self, val):
        self.__health = val
        
    @property
    def bullets(self):
        return self.__bullets
    
    @bullets.setter
    def bullets(self, val):
        self.__bullets = val
        
    @property
    def bounding_box(self):
        self.__bounding_box.x = self.x
        self.__bounding_box.y = self.y
        return self.__bounding_box
    
    @bounding_box.setter
    def bounding_box(self, val):
        self.__bounding_box = val
    
    def add_bullet(self, bullet):
        self.__bullets.append(bullet)
    
    def remove_bullet(self, bullet):
        self.__bullets.remove(bullet)

    def clear_bullets(self):
        self.__bullets = []
    