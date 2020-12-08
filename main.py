from flask import render_template
import connexion
import random
from config import connex_app, app
from valid import gen_token

#people're telling that two instances causes stupid crashes
#app = connexion.App(__name__, specification_dir='./')


connex_app.add_api('swagger2.yml')

random.seed()

@connex_app.route('/')
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.logger.info(str(gen_token()))

    connex_app.run(host='0.0.0.0', port=8080, debug=True)