from repositories import (
    auditlog_repository
)


def log_action(

    db,

    user_id,

    action,

    entity,

    entity_id,

    old_data=None,

    new_data=None
):

    return (
        auditlog_repository
        .create_audit_log(

            db=db,

            user_id=user_id,

            action=action,

            entity=entity,

            entity_id=entity_id,

            old_data=old_data,

            new_data=new_data
        )
    )