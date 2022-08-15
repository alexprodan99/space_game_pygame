
class Ship():
    def __init__(self, x, y, health, bullets = []):
        self.x = x
        self.y = y
        self.health = health
        self.bullets = bullets
    
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
        
        
    def add_bullet(self, bullet):
        self.__bullets.append(bullet)
    
    def clear_bullets(self):
        self.__bullets = []