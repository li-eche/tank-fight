import pygame,random,time
#框架搭建：
COLOR_RED = pygame.Color(255,0,0)
COLOR_BLACK =pygame.Color(0,0,0)
_display =pygame.display
life = 5
class BaseItem(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
class MainGame(): 
    TANK_P1 = None
    #存储所有敌方坦克
    EnemyTank_list=[]
    #要创建的敌方坦克数量
    EnemyTank_count = 5
    Bullet_list =[]
    #最初地方子弹列表
    Enemy_bullet_list =[]
    #爆炸坦克列表
    Explode_list =[]
    #墙壁列表
    Wall_list = []
    window =None
    SCREEN_HEIGHT =500
    SCREEN_WIDTH =800
    speed = None
    def _init_(self): 
        pass
    def startGame(self): 
        pygame.display.init()
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])
        self.creatMyTank()
        self.creatWalls()
        self.creatEnemyTank()
        _display.set_caption("坦克大战")
        while True:
            MainGame.window.fill(COLOR_BLACK)
            self.getEvent()
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆,点击ESC坦克重生,点击C增加难度  HP:5"%len(MainGame.EnemyTank_list)),(5,5))
            if MainGame.TANK_P1.live:
                MainGame.TANK_P1.displayTank()
            self.blitEnemyTank()
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                #判断我方坦克是否碰撞到墙壁
                MainGame.TANK_P1.hitwalls()
            self.blitEnemyBullet()
            self.blitExplode()
            self.blitBullet()
            self.blitWall()
            time.sleep(0.02) 
            _display.update()
    def creatMyTank(self):
        MainGame.TANK_P1=Tank(250,300) 
    def creatEnemyTank(self):
        top =100
        speed = 1
        for i in range(MainGame.EnemyTank_count):
            left =random.randint(1,7)
            eTank =EnemyTank(left*100,top,speed)
            MainGame.EnemyTank_list.append(eTank)
    def creatWalls(self):
        for i in range(5):
            wall= Wall(180*i,240)    
            MainGame.Wall_list.append(wall)        
    def blitWall(self):
        for wall in MainGame.Wall_list:
            wall.displayWall()
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live: 
                eTank.displayTank()
                #坦克移动方法
                eTank.randMove()
                #调用敌方坦克射击
                eBullet =eTank.shot()
                eTank.hitwalls()
                if eBullet:
                #将敌方子弹存储到敌方子弹列表中
                    MainGame.Enemy_bullet_list.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)
    #将子弹加入到窗口中
    def blitBullet(self):
        for bullet in MainGame.Bullet_list:
            if bullet.live:
                bullet.displayBullet()
                #让子弹移动
                bullet.Bulletmove()
                #调用我方子弹与敌方坦克碰撞方法
                bullet.myBullet_hit_enemyTank()
                #检测我方子弹是否穿过墙壁
                bullet.hitWall()
            else:
                MainGame.Bullet_list.remove(bullet)
    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_list:
            if eBullet.live:
                eBullet.displayBullet()
                #让子弹移动
                eBullet.Bulletmove()
                eBullet.enemyBullet_hit_enemyTank()
                eBullet.hitWall()
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)
    def blitExplode(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.Explode_list.remove(explode)
    def getEvent(self):
        eventList =pygame.event.get()
        for event in eventList:
            if event in eventList:
                if event.type == pygame.QUIT:
                    self.endGame()
                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_ESCAPE and not MainGame.TANK_P1.live:
                        self.creatMyTank()
                    if event.key == pygame.K_c:
                        self.creatEnemyTank()
                    if event.key ==pygame.K_LEFT:
                        print("坦克向左调头")
                        #改变坦克方向
                        MainGame.TANK_P1.stop = False
                        MainGame.TANK_P1.direction="L"
                        
                    elif event.key == pygame.K_RIGHT:
                        print("坦克向右调头")
                        MainGame.TANK_P1.stop = False
                        MainGame.TANK_P1.direction="R"
        
                    elif event.key == pygame.K_UP:
                        print("坦克向上调头")
                        MainGame.TANK_P1.stop = False
                        MainGame.TANK_P1.direction="U"
                        
                    elif event.key == pygame.K_DOWN:
                        print("坦克向下调头") 
                        MainGame.TANK_P1.stop = False
                        MainGame.TANK_P1.direction="D"
                        
                    elif event.key == pygame.K_SPACE:
                        print("坦克发射子弹")
                        if len(MainGame.Bullet_list)<3:
                            m = Bullet(MainGame.TANK_P1)
                            MainGame.Bullet_list.append(m)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        MainGame.TANK_P1.stop=True
                        
    def getTextSurface(self,text):
        pygame.font.init()
        #查看系统支持的字体
        # fontList =pygame.font.init()
        # print(fontList)
        font = pygame.font.SysFont("kaiti",30)  
        textSurface=font.render(text,True,COLOR_RED)
        return textSurface
    def endGame(self):
        print("谢谢使用")
        exit()
class Tank(BaseItem):
    def __init__(self,left,top):
        self.images = {
            "U":pygame.image.load("image\\p1tankU.gif"),
            "D":pygame.image.load("image\\p1tankD.gif"),
            "L":pygame.image.load("image\\p1tankL.gif"),
            "R":pygame.image.load("image\\p1tankR.gif")
        }
        self.direction ="U"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left =left
        self.rect.top =top
        self.speed=5
        self.stop =True
        self.live =True
        #新增属性，坦克移动之前的坐标
        self.oldLeft=self.rect.left
        self.oldTop=self.rect.top       
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top  = self.oldTop
    def hitwalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self,wall):
                #将坐标设置为移动之前的坐标
                self.stay()
    def move(self):
        self.oldLeft=self.rect.left
        self.oldTop=self.rect.top  
        if self.direction == "L":
            if self.rect.left> 0:
                self.rect.left -= self.speed
        elif self.direction =="R":
            if self.rect.left+ self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == "U":
            if self.rect.top> 0:
                self.rect.top -= self.speed
        elif self.direction =="D":
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top +=self.speed
    def shot(self):
        return Bullet(self)
    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image,self.rect)
        
class MyTank(Tank):
    def _init_(self):
        pass
class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        super(EnemyTank,self).__init__(left,top)
        self.images = {
            "U":pygame.image.load("image\\enemy1U.gif"),
            "D":pygame.image.load("image\\enemy1D.gif"),
            "L":pygame.image.load("image\\enemy1L.gif"),
            "R":pygame.image.load("image\\enemy1R.gif")
            }   
        self.direction =self.randDirection()
        self.image = self.images[self.direction]
        #坦克所在的区域
        self.rect =self.image.get_rect()
        #指定坦克初始化位置 分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top
        #速度属性
        self.speed =speed
        self.stop = True
        #新增步数属性
        self.step = 20 
    def randDirection(self):
        num =random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'
    def randMove(self):
        if self.step <=0:
            self.direction=self.randDirection()
            self.step =20
        else:
            self.move()
            self.step -=1
    def shot(self):
        #随机生成100以内的数
        num=random.randint(1,1000)
        if num<20:
            return Bullet(self)
        #图片
        #
        #
class Bullet(BaseItem):
    def __init__(self,tank):
        #图片
        self.image = pygame.image.load("image\\enemymissile.gif")
        #方向(坦克方向)
        self.direction=tank.direction
        #位置
        self.rect =self.image.get_rect()
        if self.direction == "U":
            self.rect.left =tank.rect.left + tank.rect.width/2 -self.rect.width/2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction =="D":
            self.rect.left =tank.rect.left + tank.rect.width/2 -self.rect.width/2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction =="L":
            self.rect.left = tank.rect.left
            self.rect.top =  self.rect.top = tank.rect.top + tank.rect.height/2 -self.rect.height/2
        elif self.direction =="R":
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height/2 -self.rect.height/2
        self.speed =7
        #用来控制子弹是否碰撞
        self.live =True
    def Bulletmove(self):
        if self.direction == "L":
            if self.rect.left> 0:
                self.rect.left -= self.speed
            else:
                self.live =False
        elif self.direction =="R":
            if self.rect.left+ self.rect.width < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live =False
        elif self.direction == "U":
            if self.rect.top> 0:
                self.rect.top -= self.speed
            else:
                self.live =False
        elif self.direction =="D":
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top +=self.speed
            else:
                self.live =False
    def displayBullet(self):
        #将图片加载到窗口
        MainGame.window.blit(self.image,self.rect)
    def myBullet_hit_enemyTank(self):
        #循环遍历敌方坦克列表，判断是否发生碰撞
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank,self):
                #修改敌方坦克和我方子弹的状态
                explode=Explode(eTank)
                MainGame.Explode_list.append(explode)
                eTank.live=False
                self.live=False
    def enemyBullet_hit_enemyTank(self):
        if MainGame.TANK_P1 and MainGame.TANK_P1.live:
            if pygame.sprite.collide_rect(MainGame.TANK_P1,self):
                # 产生爆炸对象
                explode = Explode(MainGame.TANK_P1)
                # 将爆炸对象添加到爆炸列表中
                MainGame.Explode_list.append(explode)
                # 修改敌方子弹与我方坦克的状态
                self.live = False
                MainGame.TANK_P1.live = False
    def hitWall(self):
        #循环遍历墙壁列表
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self,wall):
                #修改子弹的生存状态，让子弹消失
                self.live=False
                    #墙壁的生命值减小
class Explode():
    def __init__(self,tank):
        #爆炸的位置由当前子弹打中的坦克位置决定
        self.rect=tank.rect
        self.images=[
            pygame.image.load('image/blast0.gif'),
            pygame.image.load('image/blast1.gif'),
            pygame.image.load('image/blast2.gif'),
            pygame.image.load('image/blast3.gif'),
            pygame.image.load('image/blast4.gif'),
        ]
        self.step=0
        self.image=self.images[self.step]
        #是否活着
        self.live=True

    #展示爆炸效果的方法
    def displayExplode(self):
        if self.step<len(self.images):
            #根据索引获取爆炸对象
            self.image=self.images[self.step]
            self.step+=1
            #添加到主窗口
            MainGame.window.blit(self.image,self.rect)
        else:
            #修改活着的状态
            self.live=False
            self.step=0
class Wall(BaseItem):
    def __init__(self,left,top):
        #加载墙壁图片
        self.image=pygame.image.load('image/steels.gif')
        #获取墙壁的区域
        self.rect=self.image.get_rect()
        #设置位置left、top
        self.rect.left=left
        self.rect.top=top
        #是否存活
        self.live=True
        #设置生命值 no use
        self.hp=3
    #展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image,self.rect)
class music():
    def __init__(self,filename):
        self.filename=filename
        #初始化音乐混合器
        pygame.mixer.init()
        #加载音乐
        pygame.mixer.music.load(self.filename)
    #播放音乐
    def play(self):
        pygame.mixer.music.play()
if __name__=='__main__':
    MainGame().startGame()   
    
    