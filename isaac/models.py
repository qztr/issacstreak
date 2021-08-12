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

    def __init__(self,name,twitch,channel_id):
        self.name=name
        self.current="0"
        self.best="0"
        self.twitch=twitch
        self.category=""
        self.channel_id=channel_id
        self.status = "offline"
        

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

class Recordbeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    current = db.Column(db.String(128))
    best = db.Column(db.String(128))
    twitch = db.Column(db.String(128))
    category = db.Column(db.String(128))
    channel_id = db.Column(db.String(128))
    status = db.Column(db.String(128))

    def __init__(self,name,twitch,channel_id):
        self.name=name
        self.current="0"
        self.best="0"
        self.twitch=twitch
        self.category=""
        self.channel_id=channel_id
        self.status = "offline"
        

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

class Public_update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    old_value = db.Column(db.String(128))
    new_value = db.Column(db.String(128))
    val_type = db.Column(db.String(128))
    channel_name = db.Column(db.String(128))
    is_active = db.Column(db.String(128))

    @staticmethod
    def add_update(**kwargs):
        new_update = Public_update(
            old_value=kwargs.get('old_value'),
            new_value=kwargs.get('new_value'),
            val_type=kwargs.get('val_type'),
            channel_name=kwargs.get('channel_name'))
        db.session.add(new_update)
        db.session.commit()


    def __init__(self, old_value, new_value, val_type, channel_name):
        self.old_value = old_value
        self.new_value = new_value
        self.val_type = val_type
        self.channel_name = channel_name
        self.is_active="True"