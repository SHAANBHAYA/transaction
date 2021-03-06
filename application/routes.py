from application import flask_app,models,params
from flask import request

@flask_app.route(params.ROUTES["TRANSACTION"],methods=['PUT'])
def process_transaction_put(transaction_id):
    amount=request.json.get("amount")
    type = request.json.get("type")
    if not all([amount,type]):
        return "Error",500

    parent_id = int(request.json.get("parent_id",transaction_id))
    transaction_id = int(transaction_id)
    models.Transactions.add_transaction(transaction_id,type,amount,parent_id)
    return { "status": "ok" }

@flask_app.route(params.ROUTES["TRANSACTION"],methods=['GET'])
def process_transaction_get(transaction_id):
    transaction_id = int(transaction_id)
    object = models.Transactions.get_transaction(transaction_id)
    if object:
        return object.get_dict()
    else:
        return {},404

@flask_app.route(params.ROUTES["TYPES"],methods=['GET'])
def process_transaction_types(type):
    obj_list = models.Transactions.get_transaction_by_type(type)
    ret=[]
    if obj_list:
        for obj in obj_list:
            ret.append(obj.id)
        return {"transaction_ids":ret}
    else:
        return {},404

@flask_app.route(params.ROUTES["SUM"],methods=['GET'])
def process_transaction_sum(transaction_id):
    transaction_id = int(transaction_id)
    obj=models.Transactions.get_transaction(transaction_id)
    if obj :
        return {"sum":obj.sum_total}
    else:
        return {},404

