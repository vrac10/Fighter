import pygame
class Fighter():
    def __init__(self,fighter_no,x,y,flip,data,sprite_sheet,animation_steps,round_over):
        self.round_over = round_over
        self.fighter = fighter_no
        self.size = data[0]
        self.flip = flip
        self.scale = data[1]
        self.offset = data[2]
        self.alive = True
        self.hit = False
        self.animation_list = self.load_images(sprite_sheet,animation_steps)
        self.rec = pygame.Rect((x,y,80,180))
        self.action = 0 #0: idle , 1: run , 2: jump , 3: attack1 , 4: attack2 , 5: hit, 6: death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0 
        self.jumping = False
        self.running = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.health = 100
        self.attacking = False
        

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y,animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size ,self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.scale, self.size * self.scale)))
            animation_list.append(temp_img_list)   
     
        return animation_list
        



    def move(self, screen_width, screen_height,surface , target):
        speed = 10
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()
        if self.attacking == False and self.alive == True  and self.round_over == False:
            if self.fighter == 1:
                    
                        if key[pygame.K_a]:
                            dx = -speed
                            self.running = True
                        elif key[pygame.K_d]:
                            dx = speed
                            self.running = True
                        elif key[pygame.K_w] and self.jumping == False:
                            self.vel_y = -30
                            self.jumping = True
                        elif key[pygame.K_q] or key[pygame.K_r]:
                            self.attack(surface , target)
                            if key[pygame.K_q]:
                                self.attack_type = 1
                            else:
                                self.attack_type = 2
            elif self.fighter == 2:
                    
                        if key[pygame.K_LEFT]:
                            dx = -speed
                            self.running = True
                        elif key[pygame.K_RIGHT]:
                            dx = speed
                            self.running = True
                        elif key[pygame.K_UP] and self.jumping == False:
                            self.vel_y = -30
                            self.jumping = True
                        elif key[pygame.K_RSHIFT] or key[pygame.K_QUESTION]:
                            self.attack(surface , target)
                            if key[pygame.K_q]:
                                self.attack_type = 1
                            else:
                                self.attack_type = 2

        


        if self.rec.left + dx < 0:
            dx = -self.rec.left
        elif self.rec.right + dx > screen_width:
            dx = screen_width - self.rec.right

        self.vel_y += gravity

        dy += self.vel_y

        if self.rec.bottom + dy > screen_height - 110:
            self.vel_y = 0
            dy = screen_height - 110 - self.rec.bottom
            self.jumping = False
        
        if target.rec.centerx > self.rec.centerx:
            self.flip = False
        else:
            self.flip = True
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        

        self.rec.x += dx
        self.rec.y += dy

    def update(self):

        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jumping == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)


        animaton_cl = 50

        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animaton_cl:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, surface , target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rec.centerx -(2 * self.flip * self.rec.width) , self.rec.y, 2 * self.rec.width, self.rec.height)
            if attacking_rect.colliderect(target.rec):
                target.health -= 10
                target.hit = True
        
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self,surface):
        img = pygame.transform.flip(self.image,self.flip, False)
        #pygame.draw.rect(surface,(255,0,0),self.rec)
        surface.blit(img, (self.rec.x - (self.offset[0] * self.scale), self.rec.y - (self.offset[1] * self.scale)))