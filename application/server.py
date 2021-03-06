from application import flask_app, log,db
from application import params
from sqlalchemy.exc import DatabaseError

@flask_app.errorhandler(Exception)
def handle_unexpected_error(error):
    """
    Called in the case of exceptions.
    """
    log.exception("Exception while processing request.")
    try:
        log.debug("Rolling back the session.")
        db.session.rollback()
        db.session.close()
        log.debug("Rollback successful.")
    except DatabaseError:
        log.exception("Not able to close the session for db.")
    finally:
        return "Error while processing request", 500

@flask_app.after_request
def session_commit(response):
    """
    This is called by flask at the end of every request.
    """
    # For internal errors we do not want to commit.
    if response is None or response.status_code >= 400:
        db.session.close()
        return response
    try:
        log.debug("Trying to commit session.")
        db.session.commit()
        log.debug("Commit successful.")
    except DatabaseError:
        log.exception("Database error.Doing Rollback.")
        db.session.rollback()
        db.session.close()
        raise
    return response


def main():
    log.info("Starting flask server app.")
    flask_app.run(debug=True, use_reloader=False, port=params.PORT)


if __name__ == "__main__":
    main()
