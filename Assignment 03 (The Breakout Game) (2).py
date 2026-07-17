""" 
Name : Muhammad Haswwb Ul Hassan
COMP111AFA25_Programming II Section A
Assignment : 3 (The Breakout Game)
Date : November 30, 2025
"""
#Breif introduction of Program
"""The colored rectangles in the top part of the screen are bricks,
and the slightly larger rectangle at the bottom is the paddle. 
The paddle is in a fixed position in the vertical dimension, 
but moves back and forth across the screen along with left and Right key 
as insttructed by Sir through messages 
"""
####################
# Import libraries #
####################
import pygame      # pygame library 
import random      #  import random for ball directions 

pygame.init()   # inatalize pygame 

##################################################
# inatalizing all the variables using in game    #
# setting caption or title adn making screen     #
##################################################

screen_width = 800  # screen width 
screen_height = 600   # screen height 
screen = pygame.display.set_mode((screen_width, screen_height))   # use library function to make scren 
pygame.display.set_caption("The Breakout game")  # for setting the title "The Breakout Game"
paddle_w = 100   # padddle width 
paddle_h = 20    # paddle height 
ball_r = 10      # ball radius 
brick_w = 75     # bricks width 
brick_h = 20     # bricks height 
rows = 5           # no. of brick rows
cols = 10          # no. of brick columns 
white = (255,255,255)      # white colour for background 
black = (0,0,0)            # black color for paddle and ball 
# making list of brick colors using pygam method
colors = [pygame.Color("red"), pygame.Color("orange"), pygame.Color("yellow"), 
                  pygame.Color("green"), pygame.Color("blue")]

############################
# paddle class for player  # 
############################
class Paddle:
    def __init__(self):
        x = (screen_width - paddle_w)//2  # calculate x postion to center paddle along x - axis
        y = screen_height - paddle_h - 10    # postion paddle near bottom 10 pixel up
        self.rect = pygame.Rect(x,y,paddle_w,paddle_h)    # create rectangle object giving x , y positon and paddle height and width
    
    # method to move paddle left and right 
    def move(self, dir):
        if dir == "left":   # if moving left, decrease x position 
            self.rect.x -= 10
        if dir == "right":  # if moving rifht increase x position 
            self.rect.x += 10
        if self.rect.x < 0:        # condition to prevent paddle from going off left edge of screen
            self.rect.x = 0 
        if self.rect.x > screen_width - paddle_w:       # condtiont to from going off right edge of screen
            self.rect.x = screen_width - paddle_w
    
    # method to draw paddle surface on screen 
    def draw(self):
        pygame.draw.rect(screen, black, self.rect)  # filled paddle with black color 

################################
# Ball Class for boncing ball  #
################################       
class Ball:
    def __init__(self):
        d = ball_r*2    # ball radius 
        x = screen_width//2   # ball starting at horizonatal center of screen 
        y = screen_height//2  # ball strting at vertical center of screen 
        self.rect = pygame.Rect(x,y,d,d)      # rectangle object for ball collosion detection 
        self.speed_x = random.choice([-4,4])       # random horizontal speed 
        self.speed_y = -4                          # vertical or upward speed 
    
    # method to update ball positon basend on speed  
    def move(self):
        self.rect.x += self.speed_x     # Move ball horizontally by speed_x
        self.rect.y += self.speed_y     # Move ball vertically by speed_y
        
    # Method to draw ball on screen    
    def draw(self):
        pygame.draw.circle(screen, black, self.rect.center, ball_r)   # Draw filled circle at center position with radius ball_r
        
####################################
# Brick Class for braking bricks   #
####################################
class Brick:
    def __init__(self,x,y,color):
        self.rect = pygame.Rect(x,y,brick_w,brick_h)  # Create rectangle for brick at given position with brick height and width
        self.color = color     # store brick color
        self.active = True     # flag to check if the brick is active 
        
    # method to draw bick on screen  
    def draw(self):
        if self.active:       # only darw brick if its still active 
            pygame.draw.rect(screen, self.color, self.rect)

#########################################
# main game class to manage game logic  #
######################################### 
class main:
    def __init__(self):
        self.paddle = Paddle()  # create paddle object 
        self.ball = Ball()    # create ball object 
        self.lives = 3        # player has 3 lives
        self.bricks = []    # list for storing bricks objects 
        self.game_won = False     # flag to check if palyer won 
        pad = 5   # space between bricks 
        total_brick_width = cols * brick_w + (cols - 1) * pad      # total width needed for all bricks and gaps
        offset_x = (screen_width - total_brick_width) // 2         # calculate starting x position to center bricks 
        offset_y = 35                                              # starting y position for top row of bricks

        # create new bricks and add to list 
        for r in range(rows):
            for c in range(cols):
                x = c*(brick_w + pad) + offset_x
                y = r*(brick_h + pad) + offset_y
                col = colors[r % len(colors)]
                brick = Brick(x,y,col)
                self.bricks.append(brick)
    
    # method to show remaining lives on screen            
    def draw_lives(self):
        font = pygame.font.SysFont(None, 32)     # use default font size 32 
        text = font.render("Lives: "+str(self.lives), True, black)     
        screen.blit(text,(10,10))    # draw text at top left corner 
    
    # main game 
    def run(self):
        clock = pygame.time.Clock()   # clock object 
        run = True         # flag for game running 
        while run:
            for e in pygame.event.get():     # check all events 
                if e.type == pygame.QUIT:       # if player press X exit game loop 
                    run = False                 # change flag to false 
            
            # if player hasnt won  
            if not self.game_won:
                keys = pygame.key.get_pressed()    
                if keys[pygame.K_LEFT]:          # if ledt key pressed move paddle left 
                    self.paddle.move("left")
                if keys[pygame.K_RIGHT]:
                    self.paddle.move("right")    # if right key is pressed move paddle right 
                    
                # update ball position 
                self.ball.move()
                
                # check if ball hits left or right wall
                if self.ball.rect.left <= 0 or self.ball.rect.right >= screen_width:
                    self.ball.speed_x *= -1      # reverse horizontally
                    
                # check if ball hits top wal    
                if self.ball.rect.top <= 0:
                    self.ball.speed_y *= -1      # reverse down 
                
                # check if ball collides with paddle
                if self.ball.rect.colliderect(self.paddle.rect):
                    self.ball.speed_y *= -1                          # reverse vertical direction
                    self.ball.rect.bottom = self.paddle.rect.top     # place the ball just above paddle
                    
                # check collision with each brick   
                for b in self.bricks: 
                    if b.active and self.ball.rect.colliderect(b.rect):        # If brick is active and ball collides with it 
                        b.active = False       # deactivate brick 
                        self.ball.speed_y *= -1        # bounce 
                        break   # only process 1 brick colliosion in 1 FPS or frame 
                
                # check win codition 
                active_count = sum(1 for b in self.bricks if b.active)
                if active_count == 0:  # if active bricks are 0 
                    self.game_won = True    # set game won flag to true
                
                if self.ball.rect.top > screen_height: # check if goes below the screen 
                    self.lives -= 1
                    if self.lives == 0:    # if no more life 
                        f = pygame.font.SysFont(None, 48)
                        go = f.render("Game Over", True, black)      # game over 
                        screen.blit(go,(screen_width//2 - 100, screen_height//2))  # draw game over in center 
                        pygame.display.flip() 
                        pygame.time.wait(2000)      # as instructed close automatically set to 2 seconds 
                        run = False
                    else:
                        self.ball = Ball()    # if lives left create new ball 
            
            screen.fill(white)        # clear scrren by filling with white color 
            self.draw_lives()         # draw live counter 
            self.paddle.draw()        # draw paddle 
            self.ball.draw()          # draw ball 
            for b in self.bricks:
                b.draw()             # draw all bricks 
            
            if self.game_won:          # if player won 
                f = pygame.font.SysFont(None, 80)
                win = f.render("YOU WIN!", True, (0,200,0))         # render " YOU WIN! " in green color 
                rect = win.get_rect(center = (screen_width//2, screen_height//2))       # display inn center 
                screen.blit(win, rect)
            
            pygame.display.flip()     # update display 
            
            if self.game_won:    # if player won display won and then automatically set to 3 seconds end as instructed
                pygame.time.wait(3000)
                run = False
            
            clock.tick(60) # 60 FPS 
if __name__ == "__main__":
    main().run()
    pygame.quit() # quit pygame when game end