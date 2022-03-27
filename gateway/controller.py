from gateway.models import Transaction
# Making transaction
def transact(sender, receiver, money):
    if sender.balance >= money:
        receiver.balance = receiver.balance + money
        sender.balance = sender.balance - money
        sender.save()
        receiver.save()
        transaction = Transaction.create(
            sender = sender,
            receiver = receiver,
            amount = money
        )
        transaction.save()
        return transaction
    return None
