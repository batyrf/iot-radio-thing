import awsiothelper, vlcplayer, json
import os, time, pathlib

def cmdHandler(player, cmd, arg):
    if cmd == 'volup':
        player.volUp()
    elif cmd == 'voldown':
        player.volDown()
    elif cmd == 'stop':
        player.stop()
    elif cmd == 'play':
        player.play(arg)

def customCallback(client, userdata, message):
    msg = message.payload.decode("utf-8")
    try:
        d = json.loads(msg)
    except json.decoder.JSONDecodeError:
        print('not json:'+msg)
        return

    if not (('cmd' in d) and ('id' in d)):
        print('cmd or id not found\n')
        return
    cmd = d['cmd']
    id = str(d['id'])
    url=d['url']
    cmdHandler(player, cmd, url)
    print('id:'+id+"; cmd:"+cmd)

def getConf():
    home=str(pathlib.Path.home())
    path=home+'/.radioconf'
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    conf = {}
    try:
        conf = json.loads(open('conf.json').read())
        if 'rootCAPath' in conf and 'certificatePath' in conf and 'privateKeyPath' in conf:
            return conf
    except Exception as e:
        print(e)

    print('Enter required values:')
    conf["rootCAPath"] = input('rootCAPath: ')
    conf["certificatePath"] = input('certificatePath: ')
    conf["privateKeyPath"] = input('privateKeyPath: ')
    open('conf.json','w').write(json.dumps(conf))
    return conf

if __name__=="__main__":
    conf = getConf()    
    helper = awsiothelper.helper(customCallback, e='data.iot.us-east-2.amazonaws.com', r=conf['rootCAPath'], c=conf['certificatePath'], k=conf['privateKeyPath'])
    player = vlcplayer.player()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt as e:
        print("Stopping...")


