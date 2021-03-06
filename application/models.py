from application import db, log


class Transactions(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, index=True)
    amount = db.Column(db.Float, default=0)
    sum_total = db.Column(db.Float, default=0)
    parent_id = db.Column(db.Integer, index=True)

    def __str__(self):
        return "Transactions(id=%s,type=%s,amount=%s,sum_total=%s,parent_id=%s)" \
               % (self.id, self.type, self.amount, self.sum_total, self.parent_id)

    def __repr__(self):
        return str(self)

    def get_dict(self):
        return {"type": self.type, "amount": self.amount,"parent_id": self.parent_id}



    @classmethod
    def get_transaction_by_type(cls, type):
        """
        Returns all the transaction of same type
        :param type: type of transaction
        :return: List of transaction
        """
        data_list = Transactions.query.filter_by(type=type).all()
        return data_list

    @classmethod
    def get_transaction(cls, id):
        """
        Returns the transaction object
        :param id: id of the transaction
        :return: Transaction object
        """
        data = Transactions.query.filter_by(id=id).first()
        return data

    @classmethod
    def walk_and_update_parents_sum(cls, transaction):
        """
        Updates all the parents of transaction with the
        amount of transaction to be added by walking up the tree
        using the parent id.
        :param transaction: transaction created
        :return: None
        """
        sum = transaction.amount
        while transaction.parent_id != transaction.id:
            transaction.sum_total = transaction.sum_total + sum
            db.session.flush()
            log.debug("Transaction updated with sum_total=%s,transaction=%s",transaction.sum_total, transaction)
            transaction = transaction.get_transaction(transaction.parent_id)
        transaction.sum_total = transaction.sum_total + sum
        db.session.flush()
        log.debug("Transaction updated with sum_total=%s,transaction=%s",transaction.sum_total, transaction)

    @classmethod
    def add_transaction(cls, id, type, amount, parent):
        """
        Adds the transaction and updates the parents.
        :param id: id of the transaction
        :param type: type of transaction
        :param amount: amount of transaction
        :param parent: parent transaction
        :return: None
        """
        log.debug("Started creating transaction")
        if Transactions.get_transaction(id):
            raise Exception("Cannot overwrite existing transaction")
        new_trans = cls(id=id, type=type, amount=amount, parent_id=parent)
        db.session.add(new_trans)
        db.session.flush()
        # Updates the parents sum_total
        Transactions.walk_and_update_parents_sum(new_trans)
        log.debug("Transaction created successfully.Transaction=%s", new_trans)
