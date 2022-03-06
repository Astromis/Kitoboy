from flask_table import Table, Col, LinkCol

class SocNet_t(Table):
    id = Col('Id', show=False)
    socnet_id = Col("socnet_id")
    socnet_name = Col("socnet_name")
    account_status = Col("account_status")
    suicide_rating = Col("suicide_rating")
    posts = LinkCol('Posts', 'user_posts', url_kwargs=dict(id='id'))
    edit = LinkCol("Edit", "edit_socnet", url_kwargs=dict(id='id'))
    delete = LinkCol("Delete", "delete_socnet", url_kwargs=dict(id='id'))