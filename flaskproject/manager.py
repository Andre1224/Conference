#encoding:utf8
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from new import app
from extension import db
from models import User,Question,Comment

# python manager.py db init

# python manager.py db migrate
# python manager.py db upgrade


manager = Manager(app)

#绑定app和db
migrate = Migrate(app,db)

#添加迁移脚本到manager
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()