LOG_NAME="server.log"
DB_NAME="app.db"
PORT=8000

ROUTES={"TRANSACTION":"/transactionservice/transaction/<transaction_id>",
        "TYPES":"/transactionservice/types/<type>",
        "SUM":"/transactionservice/sum/<transaction_id>"}