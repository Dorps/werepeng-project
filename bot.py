from discord.ext import commands
import discord
import asyncio
client = discord.Client()
GamePrep = False
GameStart = False
RolesGiven = False
VoteTime = False
playerlist = []
players = []
rolelist = []
werewolflist = []
masonlist = []
Voted = "No one"
@client.event
async def on_ready():
    print("running")
    await client.change_presence(status=discord.Status.online,game=discord.Game(name="gotta freaking finish this bot or i die"))
class Player:
    def __init__ (self,role,user):
        self.role = role
        self.user = user
        self.vote = 0
        self.hasVoted = False
        self.end = role
    def getRole(self):
        return self.role
 
    def getUser(self):
        return self.user

    def getEndRole(self):
        return self.end

    def setRole(self,role):
        self.role = role
        self.end = role

    def setEndRole(self,end):
        self.end = end

    def addVote(self):
        self.vote += 1
    
    def getVote(self):
        return self.vote

    def SetHasVoted(self,yes):
        self.hasVoted = yes
    
    def getHasVoted(self):
        return self.hasVoted
 

@client.event
async def on_message(message):
    global GamePrep
    global GameStart
    global playerlist
    global rolelist
    global players
    global VoteTime
    global Voted
    def roleAdd(role,num):
        for i in range(num):
            rolelist.append(role)
    def roles():
        global rolelist
        global RolesGiven
        rolelist = []
        import random
        rolestart = random.randrange(len(playerlist))
        roleAdd("Werewolf",0)
        roleAdd("Seer",0)
        roleAdd("Tanner",0)
        roleAdd("Drunk",0)
        roleAdd("Hunter",0)
        roleAdd("Robber",1)
        roleAdd("Insomniac",0)
        roleAdd("Mason",0)
        roleAdd("Minion",0)
        roleAdd("Troublemaker",1)
        for i in (range(len(playerlist)-1)):
            rolelist.append("Villager")
        print(rolelist)
    
        for i in playerlist:
            i.setRole(rolelist.pop(random.randrange(len(rolelist))))
        for i in playerlist:
            if i.getRole() == "Werewolf":
                werewolflist.append(str(i.getUser()))
        for i in playerlist:
            if i.getRole() == "Mason":
                masonlist.append(str(i.getUser()))
        RolesGiven = True
        print(rolelist)
    
    def roleSwap(a,b):
        global playerlist
        role_b = b.getEndRole()
        role_a = a.getEndRole()
        a.setEndRole(role_b)
        b.setEndRole(role_a)

    def CutNum(msgauthor):
        newnum = str(msgauthor).find('#')
        newmsg = str(msgauthor)[:newnum]
        return newmsg
        



    async def messagechannel(msg):
        em = discord.Embed(title= msg, colour=0xDEADBF)
        await client.send_message(message.channel,embed=em)

    async def messageauthor(msg):
        em = discord.Embed(title= msg, colour=0xDEADBF)
        await client.send_message(message.author,embed=em)
    
    async def messagePM(msg):
        em = discord.Embed(title= msg, colour=0xDEADBF)
        await client.send_message(i.getUser(),embed=em)

        
    
    if message.content.startswith('!ready'):
        if GamePrep == False:
            await messagechannel(('Game is prepping. Type !join to join.'))
            #await client.send_message(message.channel, 'Game is prepping.')
            GamePrep = True
            playerlist = []
            await messagechannel('%s has joined the game.' %message.author)
            player_object = Player('testrole',message.author)
            playerlist.append(player_object)
            players.append(str(player_object.getUser()))
        else:
            await messagechannel('Game has begun prepping.')
        print('Game has began.')


        
        await client.send_message(message.channel, embed=em)


    if message.content.startswith('!join'):

        if GamePrep == False:
            await messagechannel('Game has not started.')
        if GamePrep == True:
            await messagechannel('%s has joined the game.' %message.author)
            player_object = Player('testrole',message.author)
            playerlist.append(player_object)
            players.append(str(player_object.getUser()))


            
    if message.content.startswith('!players'):
        await messagechannel(str(players))
        
    if message.content.startswith('!checkrole'):
        for i in playerlist:
            if i.getUser() == message.author:
                await messageauthor('Role: %s'% i.getRole())
        else:
            await messageauthor('Can not check after game has started.')

    if message.content.startswith('!roles'):
        roles()
        await messagechannel('Roles have been shuffed.')

 


    if message.content.startswith('!start'):
        if RolesGiven == True:
            VoteTime = False
            GameStart = True
            await messagechannel('Wereguins wake up and dab up your bretheren.')
            for i in playerlist:
                if i.getRole() == "Werewolf":
                    await client.send_message(i.getUser(),'Your bretheren: %s' % werewolflist)  #Werewolf Turn
            await asyncio.sleep(1)
            await messagechannel('Seer Spy on People')               #Seer Turn
            print(players)
            #Minion Turn
            for i in playerlist:
                if i.getRole() == "Minion":
                    await messagePM('Your masters are: %s'  % werewolflist)
            #Masons Turn
            for i in playerlist:
                if i.getRole() == "Mason":
                    await client.send_message(i.getUser(),'Your Masoni: %s' % masonlist)  
            for i in playerlist:
                if i.getRole() == "Seer":
                    await messagePM('Who do you want to stalk?\n Type !seer #DiscordID \n or\n Which two cards would you like to see in the middle? Left, Middle, or Right Type !seer Left Middle or !seer Middle Right etc.' % players)

                    def check(msg):
                        return msg.content.startswith('!seer')

                    seer = await client.wait_for_message(author=i.getUser(), check=check)
                    msg_content = seer.content[len('!seer'):].strip()
                    if msg_content == 'Left Middle':
                        await messagePM(rolelist[0] + ' ' + rolelist[1])
                    if msg_content == 'Middle Right':
                        await messagePM(rolelist[1] + ' ' + rolelist[2])
                    if msg_content == 'Left Right':
                        await messagePM(rolelist[0] + ' ' + rolelist[2])
                    else:
                        for k in playerlist:
                            if CutNum(k.getUser()) == msg_content:
                                await messagePM('%s is a %s' % (k.getUser(),k.getRole()))
                                print('Seer Success')
                    print(msg_content)
            for i in playerlist:
                if i.getEndRole() == "Robber":
                    await messagePM('Who do you want to swap with?\nType !robber #DiscordID')

                    def check(msg):
                        return msg.content.startswith('!robber')
                    robber = await client.wait_for_message(author=i.getUser(), check=check)
                    msg_content = robber.content[len('!robber'):].strip()
                    for k in playerlist:
                            if CutNum(k.getUser()) == msg_content:
                                await messagePM('%s is a %s' % (k.getUser(),k.getEndRole()))
                                target1 = k
                    roleSwap(i,target1)
                    break
            
        #Troublemaker
            for i in playerlist:
                if i.getRole() == "Troublemaker":
                    await messagePM('Who is your first swap target?\nType !troublemaker1 #DiscordID')
                    def check(msg):
                        return msg.content.startswith('!troublemaker1')
                    troublemaker1 = await client.wait_for_message(author=i.getUser(), check=check)
                    swaptarget1 = troublemaker1.content[len('!troublemaker1'):].strip()
                    for k in playerlist:
                        if CutNum(k.getUser()) == swaptarget1:
                            target1 = k
                            break
                    await messagePM('Who is your second swap target?\nType !troublemaker2 #DiscordID')
                    def check(msg):
                        return msg.content.startswith('!troublemaker2')
                    troublemaker2 = await client.wait_for_message(author=i.getUser(), check=check)
                    swaptarget2 = troublemaker2.content[len('!troublemaker2'):].strip()
                    for k in playerlist:
                        if CutNum(k.getUser()) == swaptarget2:
                            target2 = k
                    roleSwap(target1,target2)
                    print('Swap Success')

        #Drunk Turn
            for i in playerlist:
                if i.getRole() == "Drunk":
                    await messagePM('Which card would you like to swap? \nType !drunk Left, Middle, or Right')

                    def check(msg):
                        return msg.content.startswith('!drunk')
                    
                    drunk = await client.wait_for_message(author=i.getUser(),check=check)
                    msg_content = drunk.content[len('!drunk'):].strip()
                    print(msg_content)
                    if msg_content == 'Left':
                        i.setEndRole(rolelist.pop(0))
                        rolelist.insert(0,"Drunk")
                        await messagePM('The left card has been swapped.')
                    if msg_content == 'Middle':
                        i.setEndRole(rolelist.pop(1))
                        rolelist.insert(1,"Drunk")
                        await messagePM('The middle card has been swapped.')
                    if msg_content == 'Right':
                        i.setEndRole(rolelist.pop(2))
                        rolelist.insert(2,"Drunk")
                        await messagePM('The right card has been swapped.') 
            await messagechannel('Drunk does drunk')

        #Insomnaic Turn
            for i in playerlist:
                if i.getRole() == "Insomniac":
                    await messagePM('Your role is %s.' % (i.getEndRole()))          
            print(rolelist)

                    
                        
                        
                        
           # await asyncio.sleep(5)
            await messagechannel('Dream dream dream dream')
            await messagechannel('Time to vote! Vote with !vote #DiscordID')
            VoteTime = True
            await asyncio.sleep(20)
            await messagechannel('Vote time is closed!')
            VoteTime = False
            num_votes = 0
            for i in playerlist:
                if i.getVote() > num_votes:
                    num_votes = i.getVote()
                    Voted = str(i.getUser())
                    deadplayer = i
            await messagechannel('%s is lynched with %s votes.' % (Voted, num_votes))
            #await asyncio.sleep(5)
            for i in playerlist:
                try:
                    if i == deadplayer:
                        
                        if i.getEndRole() == "Werewolf":
                            await messagechannel('Village people win.')
                        if i.getEndRole() == "Tanner":
                            await messagechannel('Tanner wins... u idiots.')
                        if i.getEndRole() == "Hunter":
                            await messagePM('Shoot your shot Type !hunter #DiscordID')
                            def check(msg):
                                return msg.content.startswith('!hunter')
                            hunter = await client.wait_for_message(author=i.getUser(), check=check)
                            
                            msg_content = hunter.content[len('!hunter'):].strip()
                            print(msg_content)
                            for k in playerlist:
                                if str(k.getUser()) == msg_content:
                                        await messagechannel('%s is shot.'%str(k.getUser()))
                                        if k.getEndRole() == "Werewolf":
                                            await messagechannel('Village people win.')
                                        if k.getEndRole() == "Tanner":
                                            await messagechannel('Tanner wins...')
                                        else:
                                            await messagechannel('Werewolves win.')
                                        
                                        print('Hunter Success')
                except UnboundLocalError:
                    await messagechannel('Uhhh discuss the rule book on this one')
            x = ''
            for i in playerlist:
                x = x + CutNum(i.getUser()) + ' Starting Role: %s'%(i.getRole()) + ' End Role: %s\n'%(i.getEndRole())
            await messagechannel(x)
    
        else:
            await messagechannel('No cards... dummy.')

    if message.content.startswith('!vote'):
        if VoteTime == True:
            vote = message.content[len('!vote'):].strip()
            for k in playerlist:
                if k.getUser() == message.author:
                    if k.getHasVoted() == False:
                        for i in playerlist:
                            if CutNum(i.getUser()) == vote:
                                if vote == CutNum(message.author):
                                    await messageauthor('You cannot vote yourself.')
                                else:
                        
                                    k.SetHasVoted(True)
                                    i.addVote()
                                    await client.send_message(message.channel,'```%s, your vote has been recorded.```' % str(message.author))
                                    break
                    else:
                        await messageauthor('You have already voted.')

                        


            
            
        else:
            await messagechannel('It\'s not voting time.')

    if message.content.startswith('doo'):
        GameStart = False
    



    if message.content.startswith('test'):
        print(message.author)

 
    
    if message.content.startswith('!buenos'):
        await messagechannel('*buenos dias mandy! wrrryyyyy*')

    if message.content.startswith('!art2'):
        with open('seer.png','rb') as f:
            await client.send_file(message.channel, f)

    if message.content.startswith('!art1'):
        with open('werepeng.png','rb') as f:
            await client.send_file(message.channel, f)

    if message.content.startswith('!sweat'):
            with open('sweat.gif','rb') as f:
                await client.send_file(message.channel, f)

    if message.content.startswith('!art3'):
                with open('tanner.jpg','rb') as f:
                    await client.send_file(message.channel, f)

    if message.content.startswith('!art4'):
                with open('villager.png','rb') as f:
                    await client.send_file(message.channel, f)




#@client.command()
#async def ping():
#    ping_ = client.latency
#    ping = round(ping_ * 1000)
#    await client.channel.send(f"My ping is {ping}ms")

client.run("NTI0NjcwMTUyNjkyODU4OTIw.DvslVw.SVPF9slIwOFWSMNrhvLKV5zxstE")