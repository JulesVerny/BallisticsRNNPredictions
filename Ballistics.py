# ======================================================================
from __future__ import division
import math
import sys
import os
import datetime
import random
import pygame
from operator import itemgetter
import numpy as np 
##################################
# General Helper functions (START)
##################################

#RGB colors for our paddle and ball
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
# =============================================================================================================================
def load_image_convert_alpha(filename):
    """Load an image with the given filename from the images directory"""
    return pygame.image.load(os.path.join('images', filename)).convert_alpha()

def draw_centered(surface1, surface2, position):
    """Draw surface1 onto surface2 with center at position"""
    rect = surface1.get_rect()
    rect = rect.move(position[0]-rect.width//2, position[1]-rect.height//2)
    surface2.blit(surface1, rect)


def rotate_center(image, rect, angle):
        """rotate the given image around its center & return an image & rect"""
        rotate_image = pygame.transform.rotate(image, angle)
        rotate_rect = rotate_image.get_rect(center=rect.center)
        return rotate_image,rotate_rect

def distance(p, q):
    """Helper function to calculate distance between 2 points"""
    return math.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)

# =================================================================================================
class GameObject(object):
    """All game objects have a position and an image"""
    def __init__(self, position, image, speed=0):
        # max speed should be 6.5
        self.image = image
        self.position = list(position[:])
        self.speed = speed
        
    def draw_on(self, screen):
        draw_centered(self.image, screen, self.position)

    def draw_image_on(self,image,screen):
        draw_centered(image, screen, self.position)	
				
    def size(self):
        return max(self.image.get_height(), self.image.get_width())

    def radius(self):
        return self.image.get_width()/2

# ===========================================================================================
class CityScape(GameObject):
    def __init__(self, position):
        """initializing an CityScape object given it's position"""
        super(CityScape, self).__init__(position,load_image_convert_alpha('Cityscape2.png'))
        
 
    def draw_on(self, screen):
        """Draw theCityScape screen"""  
        draw_centered(self.image, screen, self.position)
# ===========================================================================================
class Launcher(GameObject):
    def __init__(self, position):
        """initializing an Launcher object given it's position"""
        super(Launcher, self).__init__(position,load_image_convert_alpha('Launcher.png'))
        
    def draw_on(self, screen):
        """Draw theCityScape screen"""  
        draw_centered(self.image, screen, self.position)
		
# ===========================================================================================
class Predictor(GameObject):
    def __init__(self, position):
        """initializing an Launcher object given it's position"""
        super(Predictor, self).__init__(position,load_image_convert_alpha('PredPointer.png'))
        
    def draw_on(self, screen):
        """Draw theCityScape screen"""  
        draw_centered(self.image, screen, self.position)	
    def UpdatePosition(self,PredDistance):
        self.position[0] = PredDistance	
# ===========================================================================================
class HistoryBlip(GameObject):
    def __init__(self, position):
        """initializing an Blip object given it's position"""
        super(HistoryBlip, self).__init__(position,load_image_convert_alpha('WhiteBlip.png'))
        
    def draw_on(self, screen):
        """Draw theCityScape screen"""       
        draw_centered(self.image, screen, self.position)
		
    def draw_image_on(self,image,screen):
        draw_centered(image, screen, self.position)	
		
# ===========================================================================================

class Missile(GameObject):
    def __init__(self, position):
        """initializing an Missile object given it's position"""
        super(Missile, self).__init__(position,load_image_convert_alpha('missile.png'))
        
        self.direction = [0, -1]
        self.angle = 45
        self.XVel = 0.0
        self.YVel = 0.0
		
        self.FiringAngle = 45
        self.LaunchAcceleration = 35.0
        self.LaunchPeriod = 25
        self.TotalDistance = 0
							
    def draw_on(self, screen):
        """Draw the Missile on the screen"""  
        new_image, rect = rotate_center(self.image,self.image.get_rect(), -self.angle)
        draw_centered(new_image, screen, self.position)

    # ===========================================================================================
    def BallisticCalculations(self,GameTime):
        #  Attempt to Develop the Missile Ballistics
        if(GameTime>self.LaunchPeriod):
            # End of the Launch Acceleration
            self.LaunchAcceleration = 0.0		 
		
        XAccleration = self.LaunchAcceleration * math.sin(math.radians(self.FiringAngle))	
        YAccleration = self.LaunchAcceleration * math.cos(math.radians(self.FiringAngle)) - 10.0    #  Approx Due to Gravity	

		# Simplified Velocity Integration Update   - inlcudes drag
        self.XVel = self.XVel + 0.025 * XAccleration - 0.0005 * self.XVel*self.XVel
        self.YVel = self.YVel + 0.025 * YAccleration - 0.0005 * self.YVel*self.YVel

        # Calculate Missile Display Orinetation from Velocities Direction 		
        directionRadians = math.atan2(self.XVel,self.YVel)
        self.angle = math.degrees(directionRadians)
			
		# Now Integrate the Positions
        self.position[0] = self.position[0] + self.XVel
        self.position[1] = self.position[1] - self.YVel
		
		# Implement some Position limits
        if(self.position[0] < 5):
             self.position[0] = 5		
        #if(self.position[1] < 10):
        #     self.position[1] = 10			
        if(self.position[0] > 1175):
             self.position[0] = 1175	
        if(self.position[1] > 585):
             self.position[1] = 585	
   
#=============================================================================================
# Main Game  Class
#=============================================================================================
class BallisticGame(object):

    # defining and initializing game states
    READY, LAUNCHING, LAUNCHCOMPLETE, FLYING, LANDED = range(5)
 
    # defining custom events
    REFRESH, START, RESTART = range(pygame.USEREVENT, pygame.USEREVENT+3)
	
    def __init__(self):
        """Initialize a new game"""
        pygame.init()

        # set up a 1200 x 600 window
        self.width = 1200
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.WhiteBlipImage = load_image_convert_alpha('WhiteBlip.png')		
        self.RedBlipImage = load_image_convert_alpha('RedBlip.png')			
        # use a black background
        self.bg_color = 0, 0, 0

        # get the default system font (with different sizes of 100, 50, 25)
        self.big_font = pygame.font.SysFont(None, 100)
        self.medium_font = pygame.font.SysFont(None, 50)
        self.small_font = pygame.font.SysFont(None, 25)
        # and make the game over text using the big font just loaded
 
        # Setup a timer to refresh the display FPS times per second
        self.FPS = 30
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        self.ReStart()
        self.draw()
   # =====================================================================================================================================
    def ReStart(self):
        """This function is called in the beginning aand upon Restarts """

        # Start the game
        self.Missile = Missile((15, 560))
    
        self.City = CityScape((690,560))
        self.Launcher = Launcher((5,560))
        self.Predictor = Predictor((0,540))
	
        self.HistoryBlips = []	
	
        # set the state to PLAYING
        self.state = BallisticGame.FLYING
        self.GameTime =0
        self.LaunchTime = 0
        self.SummaryString = ""
        self.PredictedString = ""
        self.DisplayPred = False
        self.PredictedY = 0		
	
   # =====================================================================================================================================
    def ReadGameEventsKey(self):
        rtnkey = 'null'	 
		
        events = pygame.event.get()

        for event in events:
            if(event.type == pygame.KEYDOWN):		
               if event.key== pygame.K_q:
                   rtnkey = 'quit'
               if event.key == pygame.K_SPACE:
                   rtnkey = 'fire'
               if event.key == pygame.K_UP:
                   rtnkey = 'up'
               if event.key == pygame.K_DOWN:
                   rtnkey = 'down'
        pygame.event.clear()  
        return rtnkey          
				
    # =====================================================================================================================================
    def SimulateFiring(self, FiringAngle):
       
        self.ReStart()
        self.Missile.FiringAngle = FiringAngle
        self.Missile.Angle = FiringAngle	
		
        RunXY = []
		
		# Run a Simulation loop
        while (self.state == BallisticGame.FLYING):   
                
            self.Missile.BallisticCalculations(self.GameTime-self.LaunchTime)
				
            RunXY.append(((self.Missile.position[0]-10), (570-self.Missile.position[1]))) 				
				
			# Check Landed State	
            if((self.Missile.position[1] > 570) and (self.state == BallisticGame.FLYING)) :
                self.state = BallisticGame.LANDED
                self.SummaryString = "Launch Angle: " + str(90-self.Missile.FiringAngle) + "  Distance: " + str(int(self.Missile.position[0])) + "  Flying Time: " + str(self.GameTime-self.LaunchTime)
           
			# Add a History Blip
            if self.GameTime % 3 == 0:
               NewBlip = HistoryBlip(self.Missile.position)			
               self.HistoryBlips.append(NewBlip)
               # print("Blip: [" + str(int(NewBlip.position[0])) + " , " + str(int(NewBlip.position[1])) + "]")
			   
            # draw everything			
            self.draw()	
            self.GameTime = self.GameTime + 1
		# =========================	
        return (90-FiringAngle), self.Missile.position[0], RunXY	
    # =====================================================================================================================================
    def SimulateLaunchPhase(self, FiringAngle):
       
        self.ReStart()
        self.Missile.FiringAngle = FiringAngle
        self.Missile.Angle = FiringAngle	
        self.state = BallisticGame.LAUNCHING
		
        LaunchXY = []
		
		# Run a Ballistics Simulation loop
        while ((self.state == BallisticGame.LAUNCHING) and (self.GameTime < 20)):   
                
            self.Missile.BallisticCalculations(self.GameTime-self.LaunchTime)

            LaunchXY.append(((self.Missile.position[0]-10), (570-self.Missile.position[1]))) 		
			
			# Check Landed State	
            if((self.Missile.position[1] > 570) and (self.state == BallisticGame.LAUNCHING)) :
                self.state = BallisticGame.LANDED
                self.SummaryString = "Launch Angle: " + str(90-self.Missile.FiringAngle) + "  Distance: " + str(int(self.Missile.position[0])) + "  Flying Time: " + str(self.GameTime-self.LaunchTime)
           
			# Add a History Blip
            if self.GameTime % 3 == 0:
               NewBlip = HistoryBlip(self.Missile.position)			
               self.HistoryBlips.append(NewBlip)
			   
            # draw everything			
            self.draw()	
            self.GameTime = self.GameTime + 1
		# =========================	
        if(self.state == BallisticGame.LAUNCHING):
            self.state = BallisticGame.LAUNCHCOMPLETE		
        return self.state, LaunchXY		
	# =====================================================================================================================================
    def SimulateApproachPhase(self,):
        
		# Continue Ballistics Simulation loop
        self.state = BallisticGame.FLYING
			   
        while (self.state == BallisticGame.FLYING):   
                
            self.Missile.BallisticCalculations(self.GameTime-self.LaunchTime)
				
			# Check Landed State	
            if((self.Missile.position[1] > 570) and (self.state == BallisticGame.FLYING)) :
                self.state = BallisticGame.LANDED
                self.SummaryString = "Launch Angle: " + str(int(90-self.Missile.FiringAngle)) + "  Distance: " + str(int(self.Missile.position[0])) + "  Flying Time: " + str(self.GameTime-self.LaunchTime)
           
			# Add a History Blip
            if self.GameTime % 3 == 0:
               NewBlip = HistoryBlip(self.Missile.position)			
               self.HistoryBlips.append(NewBlip)
			   
            # draw everything			
            self.draw()	
            self.GameTime = self.GameTime + 1
		# =========================		
        return self.state
		
		# =====================================================================================================================================
    def PlacePred(self, PredictedDistance):
        self.DisplayPred = True
        self.Predictor.UpdatePosition(PredictedDistance)
        self.PredictedString = " Predicted Distance: " + str(int(PredictedDistance))	    
        self.draw()	
    # =====================================================================================================================================
    def draw(self):
        """Update the display"""
        # everything we draw now is to a buffer that is not displayed
        self.screen.fill(self.bg_color)
		
		# Draw Floor
        FloorRect = pygame.Rect(5, 580, 1200, 10)
        pygame.draw.rect(self.screen, BLACK, FloorRect)
		
		# Draw the CityScape  and Launcher
        self.City.draw_on(self.screen)
        self.Launcher.draw_on(self.screen)
		
        # draw the Missile
        self.Missile.draw_on(self.screen)
  		
        # Draw the Blips
        if len(self.HistoryBlips) >  0:
            for i in range (0,len(self.HistoryBlips)):	
                if(i < 6 ):
                    self.HistoryBlips[i].draw_image_on(self.WhiteBlipImage,self.screen)
                else:
                    self.HistoryBlips[i].draw_image_on(self.RedBlipImage,self.screen)				

        # Draw the Preditor
        if(self.DisplayPred):
            self.Predictor.draw_on(self.screen) 
            PredictionText = self.small_font.render(self.PredictedString,True, (255, 255, 255))
            if(self.Predictor.position[0]> 1100):
               draw_centered(PredictionText, self.screen,((self.Predictor.position[0]-125),500))						
            else:
               draw_centered(PredictionText, self.screen,((self.Predictor.position[0]-25),500))			
 
        if(self.state == BallisticGame.LANDED):
            SummaryText = self.small_font.render(self.SummaryString,True, (255, 255, 255))
            draw_centered(SummaryText, self.screen,(550,50))
 				
        # PyGame flip buffers so that everything we have drawn gets displayed
        pygame.display.flip()

# ================================================================================================
    def Closedown(self):
        pygame.quit()

# ========================================================================================================
