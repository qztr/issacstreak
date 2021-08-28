from isaac import db

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    current = db.Column(db.String(128))
    best = db.Column(db.String(128))
    twitch = db.Column(db.String(128))
    category = db.Column(db.String(128))
    channel_id = db.Column(db.String(128))
    status = db.Column(db.String(128))
    use_bot = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self,name,twitch,channel_id):
        self.name=name
        self.current="0"
        self.best="0"
        self.twitch=twitch
        self.category=""
        self.channel_id=channel_id
        self.status = "offline"
        self.use_bot = False
        

    def to_dict(self):
        return{
            'Name':self.name,
            'current':self.current,
            'best':self.best,
            'Twitch':f'<a href="{self.twitch}" target="_blank"><img class="img-twitch" src="/static/img/twitch_{self.status}.png"></a>',

        }

    def to_dict_all(self):
        return{
            'Name':self.name,
            'current':self.current,
            'best':self.best,
            'Twitch':f'<a href="{self.twitch}" target="_blank"><img class="img-twitch" src="/static/img/twitch_{self.status}.png"></a>',
            'category':self.category,
    }
    

class Secrets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(128))
